"""
Greenhouse ATS Collector and Daily CareerSignal Runner

Reads config/company_config.csv, pulls Greenhouse jobs, filters them,
normalizes the jobs, saves them to SQLite, detects new jobs, and builds
the daily email report.

Run from the project root:

    python scripts/collect_greenhouse_jobs.py --preview

To actually send the email:

    python scripts/collect_greenhouse_jobs.py --send
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests

from careersignal.database import (
    get_jobs_first_seen_in_last_24_hours,
    insert_or_update_jobs,
)
from careersignal.email_report import build_and_send_daily_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "company_config.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "greenhouse_jobs.csv"


@dataclass
class CompanyConfig:
    company: str
    ats_type: str
    career_url: str
    target_location: str
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
    Splits a semicolon-separated keyword field into a clean lowercase list.
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
                target_location=row.get("target_location", "").strip().lower(),
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


def fetch_greenhouse_jobs(company_config: CompanyConfig) -> list[JobPosting]:
    """
    Pulls jobs from the Greenhouse public job board API.
    """

    board_token = get_greenhouse_board_token(company_config.career_url)
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    response = requests.get(api_url, timeout=20)
    response.raise_for_status()

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


def job_matches_filters(job: JobPosting, company_config: CompanyConfig) -> bool:
    """
    Applies basic title/location/exclusion filters from the config file.
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

    if not company_config.target_location:
        return True

    if company_config.target_location == "remote":
        return "remote" in location_lower

    return company_config.target_location in location_lower


def collect_greenhouse_jobs(
    companies: list[CompanyConfig],
) -> tuple[list[JobPosting], list[dict]]:
    """
    Collects matching Greenhouse jobs from all active Greenhouse companies.

    Returns:
        matching_jobs: List of matching JobPosting objects.
        failed_sources: List of failed company/source dictionaries for reporting.
    """

    matching_jobs: list[JobPosting] = []
    failed_sources: list[dict] = []

    for company_config in companies:
        if not company_config.is_active:
            continue

        if company_config.ats_type != "greenhouse":
            continue

        print(f"Collecting Greenhouse jobs for {company_config.company}...")

        try:
            all_jobs = fetch_greenhouse_jobs(company_config)

            filtered_jobs = [
                job
                for job in all_jobs
                if job_matches_filters(job, company_config)
            ]

            matching_jobs.extend(filtered_jobs)

            print(f"Found {len(all_jobs)} total jobs.")
            print(f"Kept {len(filtered_jobs)} matching jobs.")

            if all_jobs:
                print()
                print("Sample jobs before filtering:")
                for job in all_jobs[:5]:
                    print(f"- {job.title} | {job.location}")
                print()

        except requests.HTTPError as error:
            reason = f"HTTP error: {error}"
            print(f"{reason} for {company_config.company}")

            failed_sources.append(
                {
                    "company_name": company_config.company,
                    "reason": reason,
                }
            )

        except requests.RequestException as error:
            reason = f"Request error: {error}"
            print(f"{reason} for {company_config.company}")

            failed_sources.append(
                {
                    "company_name": company_config.company,
                    "reason": reason,
                }
            )

        except ValueError as error:
            reason = f"Setup error: {error}"
            print(f"{reason} for {company_config.company}")

            failed_sources.append(
                {
                    "company_name": company_config.company,
                    "reason": reason,
                }
            )

    return matching_jobs, failed_sources


def normalize_job_posting(job: JobPosting) -> dict:
    """
    Converts a JobPosting object into the normalized dictionary format
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
    Converts all collected JobPosting objects into normalized dictionaries.
    """

    return [
        normalize_job_posting(job)
        for job in jobs
    ]


def save_jobs_to_csv(jobs: list[JobPosting], output_path: Path) -> None:
    """
    Saves collected jobs to CSV as a simple debug/export file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "company",
        "title",
        "location",
        "job_url",
        "external_job_id",
        "ats_type",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            writer.writerow(
                {
                    "company": job.company,
                    "title": job.title,
                    "location": job.location,
                    "job_url": job.job_url,
                    "external_job_id": job.external_job_id,
                    "ats_type": job.ats_type,
                }
            )

    print(f"Saved {len(jobs)} jobs to {output_path}")


def shorten(value: str, max_length: int) -> str:
    """
    Shortens long text for terminal table display.
    """

    if len(value) <= max_length:
        return value

    return value[: max_length - 3] + "..."


def print_jobs_table(jobs: list[JobPosting]) -> None:
    """
    Prints matching jobs in a clean terminal table.
    """

    if not jobs:
        print()
        print("No matching Greenhouse jobs found.")
        return

    headers = ["Company", "Title", "Location", "Job ID", "URL"]

    rows = [
        [
            shorten(job.company, 18),
            shorten(job.title, 45),
            shorten(job.location, 28),
            shorten(job.external_job_id, 14),
            shorten(job.job_url, 60),
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
    print(f"Total matching Greenhouse jobs found: {len(jobs)}")


def count_active_greenhouse_companies(companies: list[CompanyConfig]) -> int:
    """
    Counts active Greenhouse companies from the config.
    """

    return sum(
        1
        for company in companies
        if company.is_active and company.ats_type == "greenhouse"
    )


def parse_args() -> argparse.Namespace:
    """
    Reads command-line mode.
    """

    parser = argparse.ArgumentParser(
        description="Collect Greenhouse jobs and send CareerSignal report."
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
    args = parse_args()

    companies = load_company_config(CONFIG_PATH)

    jobs, failed_sources = collect_greenhouse_jobs(companies)

    print_jobs_table(jobs)
    save_jobs_to_csv(jobs, OUTPUT_PATH)

    normalized_jobs = normalize_job_postings(jobs)

    summary = insert_or_update_jobs(normalized_jobs)

    new_jobs = get_jobs_first_seen_in_last_24_hours()

    email_summary = {
        "companies_checked": count_active_greenhouse_companies(companies),
        "jobs_found": summary["jobs_found"],
        "jobs_inserted": summary["jobs_inserted"],
        "jobs_updated": summary["jobs_updated"],
        "new_jobs": len(new_jobs),
    }

    build_and_send_daily_report(
        summary=email_summary,
        new_jobs=new_jobs,
        failed_sources=failed_sources,
        test_mode=args.preview,
    )


if __name__ == "__main__":
    main()