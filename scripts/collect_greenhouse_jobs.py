"""
Step 3: Greenhouse ATS Collector

Reads config/company_config.csv, pulls Greenhouse jobs, filters them,
and prints matching jobs in a clean table.

Run from the project root:

    python scripts/collect_greenhouse_jobs.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "company_config.csv"


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
    if value is None:
        return False

    return value.strip().lower() in {"true", "yes", "y", "1"}


def split_semicolon_keywords(value: str | None) -> list[str]:
    if not value:
        return []

    return [
        item.strip().lower()
        for item in value.split(";")
        if item.strip()
    ]


def load_company_config(config_path: Path) -> list[CompanyConfig]:
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
    title_lower = job.title.lower()
    location_lower = job.location.lower()

    # If job_title_keywords are listed, at least one must appear in the title.
    if company_config.job_title_keywords:
        title_has_keyword = any(
            keyword in title_lower
            for keyword in company_config.job_title_keywords
        )

        if not title_has_keyword:
            return False

    # If excluded_keywords are listed, none may appear in the title.
    if company_config.excluded_keywords:
        title_has_excluded_keyword = any(
            keyword in title_lower
            for keyword in company_config.excluded_keywords
        )

        if title_has_excluded_keyword:
            return False

    # Location filter. Blank target_location means accept any location.
    if not company_config.target_location:
        return True

    if company_config.target_location == "remote":
        return "remote" in location_lower

    return company_config.target_location in location_lower


def collect_greenhouse_jobs(companies: list[CompanyConfig]) -> list[JobPosting]:
    matching_jobs: list[JobPosting] = []

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
            print(f"HTTP error for {company_config.company}: {error}")

        except requests.RequestException as error:
            print(f"Request error for {company_config.company}: {error}")

        except ValueError as error:
            print(f"Setup error for {company_config.company}: {error}")

    return matching_jobs


def shorten(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value

    return value[: max_length - 3] + "..."


def print_jobs_table(jobs: list[JobPosting]) -> None:
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


def main() -> None:
    companies = load_company_config(CONFIG_PATH)
    jobs = collect_greenhouse_jobs(companies)
    print_jobs_table(jobs)


if __name__ == "__main__":
    main()