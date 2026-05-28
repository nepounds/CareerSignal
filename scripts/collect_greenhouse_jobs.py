"""
Greenhouse and Workday ATS Collector and Daily CareerSignal Runner

Reads config/company_config.csv, pulls jobs from supported ATS sources,
filters them, normalizes the jobs, saves them to SQLite, detects new jobs,
and builds the daily email report.

Run from the project root:

    python scripts/collect_greenhouse_jobs.py --preview

To actually send the email:

    python scripts/collect_greenhouse_jobs.py --send
"""

from __future__ import annotations

import argparse
import csv
import logging
import time
import traceback
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests

from careersignal.collectors.workday import fetch_and_normalize_workday_jobs
from careersignal.database import (
    get_jobs_first_seen_in_last_24_hours,
    insert_or_update_jobs,
)
from careersignal.email_report import build_and_send_daily_report
from careersignal.logging_config import setup_logging
from careersignal.match_scoring import score_job


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "company_config.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "greenhouse_jobs.csv"


@dataclass
class CompanyConfig:
    company: str
    ats_type: str
    career_url: str
    workday_api_url: str
    job_url_base: str
    target_locations: list[str]
    keywords: list[str]
    job_title_keywords: list[str]
    excluded_keywords: list[str]
    is_active: bool


@dataclass
class JobPosting:
    company: str
    title: str
    location: str
    job_url: str
    external_job_id: str
    ats_type: str


def is_truthy(value: str | None) -> bool:
    """
    Converts common yes/no style values into True or False.
    """

    if value is None:
        return False

    return value.strip().lower() in {"true", "yes", "y", "1"}


def split_semicolon_keywords(value: str | None) -> list[str]:
    """
    Splits a semicolon-separated field into a clean lowercase list.
    """

    if not value:
        return []

    return [
        item.strip().lower()
        for item in value.split(";")
        if item.strip()
    ]


def load_company_config(config_path: Path) -> list[CompanyConfig]:
    """
    Loads company settings from config/company_config.csv.
    """

    companies: list[CompanyConfig] = []

    with config_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            company_config = CompanyConfig(
                company=row.get("company", "").strip(),
                ats_type=row.get("ats_type", "").strip().lower(),
                career_url=row.get("career_url", "").strip(),
                workday_api_url=row.get("workday_api_url", "").strip(),
                job_url_base=row.get("job_url_base", "").strip(),
                target_locations=split_semicolon_keywords(row.get("target_location")),
                keywords=split_semicolon_keywords(row.get("keywords")),
                job_title_keywords=split_semicolon_keywords(
                    row.get("job_title_keywords")
                ),
                excluded_keywords=split_semicolon_keywords(
                    row.get("excluded_keywords")
                ),
                is_active=is_truthy(row.get("is_active")),
            )

            companies.append(company_config)

    return companies


def get_greenhouse_board_token(career_url: str) -> str:
    """
    Example:
        https://boards.greenhouse.io/gitlab

    Becomes:
        gitlab
    """

    parsed_url = urlparse(career_url)
    path_parts = parsed_url.path.strip("/").split("/")

    if not path_parts or not path_parts[0]:
        raise ValueError(f"Could not find board token in URL: {career_url}")

    return path_parts[0]


def get_with_retries(
    url: str,
    timeout: int = 20,
    max_retries: int = 3,
    retry_delay: int = 2,
) -> requests.Response:
    """
    Makes a GET request with timeout and retry handling.

    This helps with temporary failures like:
    - slow websites
    - temporary network issues
    - temporary 500/502/503/504 errors
    """

    logger = logging.getLogger("careersignal")
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Request attempt {attempt}/{max_retries}: {url}")

            response = requests.get(url, timeout=timeout)

            if response.status_code in {500, 502, 503, 504}:
                raise requests.exceptions.HTTPError(
                    f"Temporary server error: {response.status_code}"
                )

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as error:
            last_error = error

            logger.warning(
                f"Request failed on attempt {attempt}/{max_retries}: {url} | {error}"
            )

            if attempt < max_retries:
                time.sleep(retry_delay)

    raise last_error


def fetch_greenhouse_jobs(company_config: CompanyConfig) -> list[JobPosting]:
    """
    Pulls jobs from the Greenhouse public job board API.
    """

    board_token = get_greenhouse_board_token(company_config.career_url)
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    response = get_with_retries(api_url)

    data = response.json()
    raw_jobs = data.get("jobs", [])

    jobs: list[JobPosting] = []

    for raw_job in raw_jobs:
        location_data = raw_job.get("location") or {}

        job = JobPosting(
            company=company_config.company,
            title=raw_job.get("title", ""),
            location=location_data.get("name", ""),
            job_url=raw_job.get("absolute_url", ""),
            external_job_id=str(raw_job.get("id", "")),
            ats_type="greenhouse",
        )

        jobs.append(job)

    return jobs


def text_contains_any_keyword(text: str, keywords: list[str]) -> bool:
    """
    Checks whether any keyword appears in a text field.
    """

    text_lower = text.lower()

    return any(keyword in text_lower for keyword in keywords)


def greenhouse_job_matches_filters(
    job: JobPosting,
    company_config: CompanyConfig,
) -> bool:
    """
    Applies title/location/exclusion filters to a Greenhouse JobPosting.
    """

    title_lower = job.title.lower()
    location_lower = job.location.lower()

    if company_config.job_title_keywords:
        title_has_keyword = any(
            keyword in title_lower
            for keyword in company_config.job_title_keywords
        )

        if not title_has_keyword:
            return False

    if company_config.excluded_keywords:
        title_has_excluded_keyword = any(
            keyword in title_lower
            for keyword in company_config.excluded_keywords
        )

        if title_has_excluded_keyword:
            return False

    if not company_config.target_locations:
        return True

    return any(
        target_location in location_lower
        for target_location in company_config.target_locations
    )


def normalized_job_matches_filters(
    job: dict,
    company_config: CompanyConfig,
) -> bool:
    """
    Applies title/location/exclusion filters to a normalized job dictionary.
    """

    title = str(job.get("title") or "")
    location = str(job.get("location") or "")
    department = str(job.get("department") or "")

    title_lower = title.lower()
    location_lower = location.lower()
    searchable_text = f"{title} {department}".lower()

    if company_config.job_title_keywords:
        title_has_keyword = any(
            keyword in title_lower
            for keyword in company_config.job_title_keywords
        )

        if not title_has_keyword:
            return False

    if company_config.keywords:
        text_has_keyword = any(
            keyword in searchable_text
            for keyword in company_config.keywords
        )

        if not text_has_keyword:
            return False

    if company_config.excluded_keywords:
        title_has_excluded_keyword = any(
            keyword in title_lower
            for keyword in company_config.excluded_keywords
        )

        if title_has_excluded_keyword:
            return False

    if not company_config.target_locations:
        return True

    return any(
        target_location in location_lower
        for target_location in company_config.target_locations
    )


def collect_greenhouse_jobs(
    companies: list[CompanyConfig],
) -> tuple[list[JobPosting], list[dict]]:
    """
    Collects matching Greenhouse jobs from all active Greenhouse companies.

    Returns:
        matching_jobs: List of matching JobPosting objects.
        failed_sources: List of failed company/source dictionaries for reporting.
    """

    logger = logging.getLogger("careersignal")

    matching_jobs: list[JobPosting] = []
    failed_sources: list[dict] = []

    for company_config in companies:
        if not company_config.is_active:
            continue

        if company_config.ats_type != "greenhouse":
            continue

        print(f"Collecting Greenhouse jobs for {company_config.company}...")
        logger.info(f"Collecting Greenhouse jobs for {company_config.company}")

        try:
            all_jobs = fetch_greenhouse_jobs(company_config)

            filtered_jobs = [
                job
                for job in all_jobs
                if greenhouse_job_matches_filters(job, company_config)
            ]

            matching_jobs.extend(filtered_jobs)

            print(f"Found {len(all_jobs)} total jobs.")
            print(f"Kept {len(filtered_jobs)} matching jobs.")

            logger.info(
                f"{company_config.company}: found {len(all_jobs)} total jobs, "
                f"kept {len(filtered_jobs)} matching jobs"
            )

            if all_jobs:
                print()
                print("Sample Greenhouse jobs before filtering:")
                for job in all_jobs[:5]:
                    print(f"- {job.title} | {job.location}")
                print()

        except requests.HTTPError as error:
            failed_sources.append(
                build_failed_source(company_config, f"HTTP error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except requests.RequestException as error:
            failed_sources.append(
                build_failed_source(company_config, f"Request error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except ValueError as error:
            failed_sources.append(
                build_failed_source(company_config, f"Setup error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except Exception as error:
            failed_sources.append(
                build_failed_source(company_config, f"Unexpected error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

    return matching_jobs, failed_sources


def get_workday_api_url(company_config: CompanyConfig) -> str:
    """
    Gets the Workday CXS API URL for a company.

    Preferred:
        workday_api_url column

    Fallback:
        career_url, but only if it already looks like a Workday CXS API URL.
    """

    if company_config.workday_api_url:
        return company_config.workday_api_url

    if "/wday/cxs/" in company_config.career_url:
        return company_config.career_url

    raise ValueError(
        "Missing Workday API URL. Add a workday_api_url value to "
        "config/company_config.csv. Public career pages are not enough."
    )


def collect_workday_jobs(
    companies: list[CompanyConfig],
) -> tuple[list[dict], list[dict]]:
    """
    Collects matching Workday jobs from all active Workday companies.

    Workday jobs are already normalized by src/careersignal/collectors/workday.py.
    """

    logger = logging.getLogger("careersignal")

    matching_jobs: list[dict] = []
    failed_sources: list[dict] = []

    for company_config in companies:
        if not company_config.is_active:
            continue

        if company_config.ats_type != "workday":
            continue

        print(f"Collecting Workday jobs for {company_config.company}...")
        logger.info(f"Collecting Workday jobs for {company_config.company}")

        try:
            api_url = get_workday_api_url(company_config)

            all_jobs = fetch_and_normalize_workday_jobs(
                api_url=api_url,
                company_name=company_config.company,
                job_url_base=company_config.job_url_base or company_config.career_url,
                search_text="",
                limit=20,
                offset=0,
            )

            filtered_jobs = [
                job
                for job in all_jobs
                if normalized_job_matches_filters(job, company_config)
            ]

            matching_jobs.extend(filtered_jobs)

            print(f"Found {len(all_jobs)} total jobs.")
            print(f"Kept {len(filtered_jobs)} matching jobs.")

            logger.info(
                f"{company_config.company}: found {len(all_jobs)} total jobs, "
                f"kept {len(filtered_jobs)} matching jobs"
            )

            if all_jobs:
                print()
                print("Sample Workday jobs before filtering:")
                for job in all_jobs[:5]:
                    print(
                        f"- {job.get('title', '')} | "
                        f"{job.get('location', '')}"
                    )
                print()

        except requests.HTTPError as error:
            failed_sources.append(
                build_failed_source(company_config, f"HTTP error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except requests.RequestException as error:
            failed_sources.append(
                build_failed_source(company_config, f"Request error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except ValueError as error:
            failed_sources.append(
                build_failed_source(company_config, f"Setup error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

        except Exception as error:
            failed_sources.append(
                build_failed_source(company_config, f"Unexpected error: {error}")
            )
            log_collection_error(logger, company_config, error)
            continue

    return matching_jobs, failed_sources


def build_failed_source(company_config: CompanyConfig, reason: str) -> dict:
    """
    Builds one failed source dictionary for the email report.
    """

    print(f"{reason} for {company_config.company}")
    print("Continuing to next company...")

    return {
        "company_name": company_config.company,
        "source_ats": company_config.ats_type,
        "reason": reason,
        "error": reason,
    }


def log_collection_error(
    logger: logging.Logger,
    company_config: CompanyConfig,
    error: Exception,
) -> None:
    """
    Writes collection errors to the log file.
    """

    logger.error(f"Collection failed for {company_config.company}: {error}")
    logger.error(traceback.format_exc())


def normalize_job_posting(job: JobPosting) -> dict:
    """
    Converts a Greenhouse JobPosting object into the normalized dictionary format
    expected by database.py.
    """

    return {
        "company_name": job.company,
        "source_ats": job.ats_type,
        "external_job_id": job.external_job_id,
        "title": job.title,
        "location": job.location,
        "department": "",
        "job_url": job.job_url,
        "posted_date": "",
        "date_collected": date.today().isoformat(),
    }


def normalize_job_postings(jobs: list[JobPosting]) -> list[dict]:
    """
    Converts all collected Greenhouse JobPosting objects into normalized dictionaries.
    """

    return [
        normalize_job_posting(job)
        for job in jobs
    ]


def score_normalized_jobs(jobs: list[dict]) -> None:
    """
    Runs match scoring for every normalized job.

    This keeps scoring behavior centralized in src/careersignal/match_scoring.py.

    Important:
        This function calls score_job(job), but it does not add new fields to the
        official normalized job dictionary. The official project state says the
        database input shape should stay limited to the approved normalized fields.
    """

    logger = logging.getLogger("careersignal")

    for job in jobs:
        try:
            score_job(job)
        except Exception as error:
            logger.warning(
                f"Could not score job "
                f"{job.get('company_name', '')} | {job.get('title', '')}: {error}"
            )


def save_jobs_to_csv(jobs: list[dict], output_path: Path) -> None:
    """
    Saves collected normalized jobs to CSV as a simple debug/export file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "company_name",
        "source_ats",
        "external_job_id",
        "title",
        "location",
        "department",
        "job_url",
        "posted_date",
        "date_collected",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            writer.writerow(
                {
                    "company_name": job.get("company_name", ""),
                    "source_ats": job.get("source_ats", ""),
                    "external_job_id": job.get("external_job_id", ""),
                    "title": job.get("title", ""),
                    "location": job.get("location", ""),
                    "department": job.get("department", ""),
                    "job_url": job.get("job_url", ""),
                    "posted_date": job.get("posted_date", ""),
                    "date_collected": job.get("date_collected", ""),
                }
            )

    print(f"Saved {len(jobs)} jobs to {output_path}")


def shorten(value: str | None, max_length: int) -> str:
    """
    Shortens long text for terminal table display.
    """

    clean_value = str(value or "")

    if len(clean_value) <= max_length:
        return clean_value

    return clean_value[: max_length - 3] + "..."


def print_jobs_table(jobs: list[dict]) -> None:
    """
    Prints matching normalized jobs in a clean terminal table.
    """

    if not jobs:
        print()
        print("No matching supported ATS jobs found.")
        return

    headers = ["Company", "ATS", "Title", "Location", "Job ID", "URL"]

    rows = [
        [
            shorten(job.get("company_name"), 18),
            shorten(job.get("source_ats"), 10),
            shorten(job.get("title"), 45),
            shorten(job.get("location"), 28),
            shorten(job.get("external_job_id"), 14),
            shorten(job.get("job_url"), 60),
        ]
        for job in jobs
    ]

    column_widths = [
        max(len(row[index]) for row in rows + [headers])
        for index in range(len(headers))
    ]

    def format_row(row: list[str]) -> str:
        return " | ".join(
            value.ljust(column_widths[index])
            for index, value in enumerate(row)
        )

    separator = "-+-".join("-" * width for width in column_widths)

    print()
    print(format_row(headers))
    print(separator)

    for row in rows:
        print(format_row(row))

    print()
    print(f"Total matching supported ATS jobs found: {len(jobs)}")


def count_active_supported_companies(companies: list[CompanyConfig]) -> int:
    """
    Counts active companies using supported ATS types.
    """

    supported_ats_types = {"greenhouse", "workday"}

    return sum(
        1
        for company in companies
        if company.is_active and company.ats_type in supported_ats_types
    )


def parse_args() -> argparse.Namespace:
    """
    Reads command-line mode.
    """

    parser = argparse.ArgumentParser(
        description="Collect supported ATS jobs and send CareerSignal report."
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "--preview",
        action="store_true",
        help="Print the email preview instead of sending it.",
    )

    mode_group.add_argument(
        "--send",
        action="store_true",
        help="Send the email report using .env email settings.",
    )

    return parser.parse_args()


def main() -> None:
    logger = setup_logging()

    args = parse_args()

    logger.info("=" * 80)
    logger.info("CareerSignal supported ATS run started")
    logger.info(f"Mode: {'preview' if args.preview else 'send'}")

    try:
        companies = load_company_config(CONFIG_PATH)
    except Exception:
        logger.error("Failed to load company config.")
        logger.error(traceback.format_exc())
        print("ERROR: Could not load company config. Check logs/careersignal.log")
        return

    greenhouse_jobs, greenhouse_failed_sources = collect_greenhouse_jobs(companies)
    normalized_greenhouse_jobs = normalize_job_postings(greenhouse_jobs)

    workday_jobs, workday_failed_sources = collect_workday_jobs(companies)

    normalized_jobs = normalized_greenhouse_jobs + workday_jobs
    failed_sources = greenhouse_failed_sources + workday_failed_sources

    score_normalized_jobs(normalized_jobs)

    print_jobs_table(normalized_jobs)
    save_jobs_to_csv(normalized_jobs, OUTPUT_PATH)

    try:
        summary = insert_or_update_jobs(normalized_jobs)
    except Exception:
        logger.error("Database insert/update failed.")
        logger.error(traceback.format_exc())
        print("ERROR: Database insert/update failed. Check logs/careersignal.log")
        return

    try:
        new_jobs = get_jobs_first_seen_in_last_24_hours()
    except Exception:
        logger.error("Failed to get new jobs from database.")
        logger.error(traceback.format_exc())
        print("WARNING: Could not retrieve new jobs. Continuing with empty new_jobs list.")
        new_jobs = []

    email_summary = {
        "companies_checked": count_active_supported_companies(companies),
        "jobs_found": summary["jobs_found"],
        "jobs_inserted": summary["jobs_inserted"],
        "jobs_updated": summary["jobs_updated"],
        "new_jobs": len(new_jobs),
        "failed_sources": len(failed_sources),
    }

    try:
        build_and_send_daily_report(
            summary=email_summary,
            new_jobs=new_jobs,
            failed_sources=failed_sources,
            test_mode=args.preview,
        )
    except Exception:
        logger.error("Failed to build/send daily email report.")
        logger.error(traceback.format_exc())
        print("WARNING: Run completed, but email report failed.")

    logger.info("CareerSignal supported ATS run finished")
    logger.info(f"Email summary: {email_summary}")
    logger.info(f"Failed sources: {failed_sources}")

    print()
    print("CareerSignal run complete.")
    print("-" * 40)
    print(f"Mode: {'Preview' if args.preview else 'Send'}")
    print(f"Companies checked: {email_summary['companies_checked']}")
    print(f"Jobs found: {email_summary['jobs_found']}")
    print(f"Jobs inserted: {email_summary['jobs_inserted']}")
    print(f"Jobs updated: {email_summary['jobs_updated']}")
    print(f"New jobs in last 24 hours: {email_summary['new_jobs']}")
    print(f"Failed sources: {email_summary['failed_sources']}")

    if failed_sources:
        print()
        print("Failed sources:")
        for failed_source in failed_sources:
            print(
                f"- {failed_source['company_name']} "
                f"({failed_source['source_ats']}): "
                f"{failed_source['reason']}"
            )

    print()
    print("Log file: logs/careersignal.log")


if __name__ == "__main__":
    main()