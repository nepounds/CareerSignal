from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urljoin

import requests


NORMALIZED_JOB_FIELDS = [
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


def fetch_workday_raw_jobs(
    api_url: str,
    search_text: str = "",
    limit: int = 20,
    offset: int = 0,
    timeout_seconds: int = 30,
) -> list[dict[str, Any]]:
    """
    Fetch raw jobs from a Workday CXS API endpoint.

    This only fetches raw Workday results.
    It does not save jobs, score jobs, email jobs, or export jobs.
    """

    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": offset,
        "searchText": search_text,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "CareerSignal/1.0",
    }

    response = requests.post(
        api_url,
        json=payload,
        headers=headers,
        timeout=timeout_seconds,
    )

    response.raise_for_status()

    data = response.json()
    raw_jobs = data.get("jobPostings", [])

    if not isinstance(raw_jobs, list):
        return []

    return raw_jobs


def fetch_and_normalize_workday_jobs(
    api_url: str,
    company_name: str,
    job_url_base: str | None = None,
    search_text: str = "",
    limit: int = 20,
    offset: int = 0,
) -> list[dict[str, str | None]]:
    """
    Fetch raw Workday jobs and return normalized CareerSignal job dictionaries.
    """

    raw_jobs = fetch_workday_raw_jobs(
        api_url=api_url,
        search_text=search_text,
        limit=limit,
        offset=offset,
    )

    return normalize_workday_jobs(
        raw_jobs=raw_jobs,
        company_name=company_name,
        job_url_base=job_url_base,
    )


def normalize_workday_jobs(
    raw_jobs: list[dict[str, Any]],
    company_name: str,
    job_url_base: str | None = None,
) -> list[dict[str, str | None]]:
    """
    Normalize a list of raw Workday jobs.
    """

    normalized_jobs = []

    for raw_job in raw_jobs:
        normalized_job = normalize_workday_job(
            raw_job=raw_job,
            company_name=company_name,
            job_url_base=job_url_base,
        )

        normalized_jobs.append(normalized_job)

    return normalized_jobs


def normalize_workday_job(
    raw_job: dict[str, Any],
    company_name: str,
    job_url_base: str | None = None,
) -> dict[str, str | None]:
    """
    Convert one raw Workday job into CareerSignal's official normalized shape.
    """

    normalized_job = {
        "company_name": company_name or "",
        "source_ats": "workday",
        "external_job_id": extract_workday_external_job_id(raw_job),
        "title": extract_workday_title(raw_job),
        "location": extract_workday_location(raw_job),
        "department": extract_workday_department(raw_job),
        "job_url": build_workday_job_url(raw_job, job_url_base),
        "posted_date": extract_workday_posted_date(raw_job),
        "date_collected": date.today().isoformat(),
    }

    validate_normalized_job_shape(normalized_job)

    return normalized_job


def extract_workday_external_job_id(raw_job: dict[str, Any]) -> str:
    """
    Extract the most stable Workday job ID available.
    """

    possible_id_fields = [
        "jobReqId",
        "reqId",
        "requisitionId",
        "id",
    ]

    for field_name in possible_id_fields:
        value = raw_job.get(field_name)

        if value:
            return str(value).strip()

    external_path = raw_job.get("externalPath")

    if external_path:
        return str(external_path).strip().strip("/")

    return ""


def extract_workday_title(raw_job: dict[str, Any]) -> str:
    """
    Extract the job title.
    """

    title = raw_job.get("title")

    if title:
        return str(title).strip()

    return ""


def extract_workday_location(raw_job: dict[str, Any]) -> str:
    """
    Extract a clean location string.
    """

    locations_text = raw_job.get("locationsText")

    if locations_text:
        return str(locations_text).strip()

    locations = raw_job.get("locations")

    if isinstance(locations, list):
        location_names = []

        for location in locations:
            if isinstance(location, dict):
                name = location.get("displayName") or location.get("name")

                if name:
                    location_names.append(str(name).strip())

            elif location:
                location_names.append(str(location).strip())

        return "; ".join(location_names)

    location = raw_job.get("location")

    if location:
        return str(location).strip()

    return ""


def extract_workday_department(raw_job: dict[str, Any]) -> str:
    """
    Extract department-like information if Workday provides it.
    """

    possible_department_fields = [
        "department",
        "jobFamily",
        "jobFamilyGroup",
        "businessUnit",
    ]

    for field_name in possible_department_fields:
        value = raw_job.get(field_name)

        if isinstance(value, dict):
            display_value = value.get("displayName") or value.get("name")

            if display_value:
                return str(display_value).strip()

        if value:
            return str(value).strip()

    return ""


def extract_workday_posted_date(raw_job: dict[str, Any]) -> str | None:
    """
    Extract posted date if available.

    Returns None when Workday does not provide a posted date.
    """

    possible_date_fields = [
        "postedOn",
        "postedDate",
        "startDate",
    ]

    for field_name in possible_date_fields:
        value = raw_job.get(field_name)

        if value:
            return str(value).strip()

    return None


def build_workday_job_url(
    raw_job: dict[str, Any],
    job_url_base: str | None = None,
) -> str:
    """
    Build a public job URL when possible.
    """

    possible_url_fields = [
        "jobUrl",
        "url",
        "externalUrl",
    ]

    for field_name in possible_url_fields:
        value = raw_job.get(field_name)

        if value:
            return str(value).strip()

    external_path = raw_job.get("externalPath")

    if external_path and job_url_base:
        clean_external_path = str(external_path).strip().lstrip("/")
        return urljoin(job_url_base.rstrip("/") + "/", clean_external_path)

    return ""


def validate_normalized_job_shape(job: dict[str, Any]) -> None:
    """
    Confirm the job has exactly the official CareerSignal normalized fields.
    """

    expected_fields = set(NORMALIZED_JOB_FIELDS)
    actual_fields = set(job.keys())

    missing_fields = expected_fields - actual_fields
    extra_fields = actual_fields - expected_fields

    if missing_fields or extra_fields:
        raise ValueError(
            "Normalized Workday job does not match official CareerSignal shape. "
            f"Missing fields: {sorted(missing_fields)}. "
            f"Extra fields: {sorted(extra_fields)}."
        )