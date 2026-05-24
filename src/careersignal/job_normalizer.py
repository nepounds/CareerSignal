"""
Job normalizer for CareerSignal.

This file converts raw ATS job data into one standard job dictionary format.
"""

from datetime import date
from typing import Any


STANDARD_JOB_FIELDS = [
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


def clean_text(value: Any) -> str:
    """
    Converts a value to clean text.

    Examples:
    None -> ""
    "  Accounting Intern  " -> "Accounting Intern"
    123 -> "123"
    """
    if value is None:
        return ""

    return str(value).strip()


def normalize_greenhouse_job(raw_job: dict, company_name: str) -> dict:
    """
    Converts one raw Greenhouse job into the CareerSignal standard job format.
    """

    location = ""

    raw_location = raw_job.get("location")
    if isinstance(raw_location, dict):
        location = clean_text(raw_location.get("name"))
    else:
        location = clean_text(raw_location)

    department = ""

    raw_departments = raw_job.get("departments")
    if isinstance(raw_departments, list) and len(raw_departments) > 0:
        first_department = raw_departments[0]

        if isinstance(first_department, dict):
            department = clean_text(first_department.get("name"))
        else:
            department = clean_text(first_department)

    normalized_job = {
        "company_name": clean_text(company_name),
        "source_ats": "greenhouse",
        "external_job_id": clean_text(raw_job.get("id")),
        "title": clean_text(raw_job.get("title")),
        "location": location,
        "department": department,
        "job_url": clean_text(raw_job.get("absolute_url")),
        "posted_date": clean_text(raw_job.get("updated_at")),
        "date_collected": date.today().isoformat(),
    }

    return normalized_job


def normalize_jobs(raw_jobs: list[dict], company_name: str, source_ats: str) -> list[dict]:
    """
    Normalizes a list of raw jobs.
    """

    normalized_jobs = []

    for raw_job in raw_jobs:
        if source_ats == "greenhouse":
            normalized_job = normalize_greenhouse_job(raw_job, company_name)
        else:
            raise ValueError(f"Unsupported ATS source: {source_ats}")

        normalized_jobs.append(normalized_job)

    return normalized_jobs


def validate_normalized_job(job: dict) -> bool:
    """
    Checks whether a job dictionary has all required standard fields.
    """

    for field in STANDARD_JOB_FIELDS:
        if field not in job:
            return False

    return True