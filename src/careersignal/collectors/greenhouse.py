"""
Greenhouse collector for CareerSignal.

This module contains reusable Greenhouse API collection logic.
The main runner in scripts/collect_greenhouse_jobs.py handles config loading,
filtering, database writes, email reporting, and run orchestration.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import date
from urllib.parse import urlparse

import requests


@dataclass
class GreenhouseJobPosting:
    company: str
    title: str
    location: str
    job_url: str
    external_job_id: str
    ats_type: str = "greenhouse"


def get_greenhouse_board_token(career_url: str) -> str:
    """
    Extracts the Greenhouse board token from a Greenhouse job board URL.

    Examples:
        https://boards.greenhouse.io/gitlab -> gitlab
        https://job-boards.greenhouse.io/pendo -> pendo
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

    if last_error is None:
        raise RuntimeError(f"Request failed for unknown reason: {url}")

    raise last_error


def fetch_greenhouse_jobs(
    career_url: str,
    company_name: str,
) -> list[GreenhouseJobPosting]:
    """
    Pulls jobs from the Greenhouse public job board API.
    """

    board_token = get_greenhouse_board_token(career_url)
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    response = get_with_retries(api_url)

    data = response.json()
    raw_jobs = data.get("jobs", [])

    jobs: list[GreenhouseJobPosting] = []

    for raw_job in raw_jobs:
        location_data = raw_job.get("location") or {}

        job = GreenhouseJobPosting(
            company=company_name,
            title=raw_job.get("title", ""),
            location=location_data.get("name", ""),
            job_url=raw_job.get("absolute_url", ""),
            external_job_id=str(raw_job.get("id", "")),
        )

        jobs.append(job)

    return jobs


def normalize_greenhouse_job(job: GreenhouseJobPosting) -> dict:
    """
    Converts a Greenhouse job object into the normalized dictionary format
    expected by CareerSignal database and reporting logic.
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


def normalize_greenhouse_jobs(jobs: list[GreenhouseJobPosting]) -> list[dict]:
    """
    Converts all collected Greenhouse job objects into normalized dictionaries.
    """

    return [normalize_greenhouse_job(job) for job in jobs]