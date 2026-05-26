"""
Step 12A - Workday Proof of Concept

Goal:
- Test one Workday career site by itself.
- Do not touch the database.
- Do not send emails.
- Do not export Excel.
- Do not update Power BI.
- Do not integrate with the main CareerSignal runner yet.

This script:
1. Takes a Workday career URL.
2. Extracts the tenant, server, and site name.
3. Builds the Workday jobs endpoint.
4. Fetches job postings with pagination.
5. Prints a clean preview of the jobs found.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import requests


# A small Workday test case.
# You can replace this with another Workday career URL later.
DEFAULT_WORKDAY_URL = "https://signetjewelers.wd1.myworkdayjobs.com/SignetCorporateCareers"


@dataclass
class WorkdaySite:
    """
    Holds the important pieces of a Workday career site URL.

    Example:
    https://signetjewelers.wd1.myworkdayjobs.com/SignetCorporateCareers

    tenant = signetjewelers
    server = wd1
    site = SignetCorporateCareers
    """

    original_url: str
    tenant: str
    server: str
    site: str

    @property
    def base_url(self) -> str:
        return f"https://{self.tenant}.{self.server}.myworkdayjobs.com"

    @property
    def careers_url(self) -> str:
        return f"{self.base_url}/{self.site}"

    @property
    def jobs_endpoint(self) -> str:
        return f"{self.base_url}/wday/cxs/{self.tenant}/{self.site}/jobs"


def parse_workday_url(workday_url: str) -> WorkdaySite:
    """
    Extract tenant, server, and site name from a Workday career URL.

    Supports URLs like:
    - https://signetjewelers.wd1.myworkdayjobs.com/SignetCorporateCareers
    - https://target.wd5.myworkdayjobs.com/targetcareers
    - https://workday.wd5.myworkdayjobs.com/Workday

    Some Workday URLs include a language path like:
    - https://example.wd1.myworkdayjobs.com/en-US/External

    For those, this function skips the language section and uses the next path
    piece as the site name.
    """

    parsed_url = urlparse(workday_url)

    hostname = parsed_url.hostname
    if not hostname:
        raise ValueError(f"Could not read hostname from URL: {workday_url}")

    hostname_parts = hostname.split(".")

    if len(hostname_parts) < 4:
        raise ValueError(
            "This does not look like a standard myworkdayjobs.com URL. "
            f"Received hostname: {hostname}"
        )

    tenant = hostname_parts[0]
    server = hostname_parts[1]

    if server.startswith("wd") is False:
        raise ValueError(
            "Could not identify the Workday server. "
            f"Expected something like wd1, wd3, or wd5. Received: {server}"
        )

    path_parts = [part for part in parsed_url.path.split("/") if part]

    if not path_parts:
        raise ValueError(
            "Could not identify the Workday site name from the URL path. "
            f"Received URL: {workday_url}"
        )

    # Some URLs are like /en-US/SiteName.
    # If the first path part looks like a language code, skip it.
    if len(path_parts) >= 2 and "-" in path_parts[0]:
        site = path_parts[1]
    else:
        site = path_parts[0]

    return WorkdaySite(
        original_url=workday_url,
        tenant=tenant,
        server=server,
        site=site,
    )


def make_headers(site: WorkdaySite) -> dict[str, str]:
    """
    Build request headers.

    The User-Agent and Referer help the request look like normal browser traffic.
    This is not hacking anything. It is just requesting the public job data that
    the public career page uses.
    """

    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "en-US",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": site.careers_url,
    }


def fetch_workday_page(
    site: WorkdaySite,
    offset: int,
    limit: int,
    timeout_seconds: int = 30,
) -> dict[str, Any]:
    """
    Fetch one page of Workday jobs.

    Workday usually expects a POST request, not a GET request.

    offset:
        Where this page starts.

    limit:
        How many jobs to request in this page.
    """

    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": offset,
        "searchText": "",
    }

    response = requests.post(
        site.jobs_endpoint,
        headers=make_headers(site),
        json=payload,
        timeout=timeout_seconds,
    )

    response.raise_for_status()

    return response.json()


def get_job_location(job_posting: dict[str, Any]) -> str:
    """
    Pull a readable location from a Workday job posting.

    Different Workday sites expose location data slightly differently.
    This function tries the common fields in a safe order.
    """

    locations_text = job_posting.get("locationsText")
    if locations_text:
        return str(locations_text)

    locations = job_posting.get("locations")
    if isinstance(locations, list) and locations:
        location_names = []

        for location in locations:
            if isinstance(location, dict):
                location_name = location.get("name") or location.get("descriptor")
                if location_name:
                    location_names.append(str(location_name))
            elif isinstance(location, str):
                location_names.append(location)

        if location_names:
            return "; ".join(location_names)

    return "Not listed"


def get_external_job_id(job_posting: dict[str, Any]) -> str:
    """
    Try to find the external job ID.

    Workday often stores this in bulletFields.
    Examples may look like:
    - R-12345
    - JR-12345
    - REQ12345

    If no obvious ID exists, this returns Not listed.
    """

    bullet_fields = job_posting.get("bulletFields", [])

    if isinstance(bullet_fields, list):
        for field in bullet_fields:
            field_text = str(field).strip()

            if field_text.startswith(("R-", "JR", "JR-", "REQ", "REQ-")):
                return field_text

    job_id = job_posting.get("id")
    if job_id:
        return str(job_id)

    return "Not listed"


def build_job_url(site: WorkdaySite, job_posting: dict[str, Any]) -> str:
    """
    Build a clickable Workday job URL.

    Workday usually provides externalPath.
    Example:
    /job/Some-Location/Some-Job-Title_R12345

    Full URL:
    https://tenant.wd1.myworkdayjobs.com/SiteName/job/Some-Location/Some-Job-Title_R12345
    """

    external_url = job_posting.get("externalUrl")
    if external_url:
        return str(external_url)

    external_path = job_posting.get("externalPath")
    if external_path:
        external_path = str(external_path)

        if external_path.startswith("http"):
            return external_path

        if external_path.startswith("/"):
            return f"{site.careers_url}{external_path}"

        return f"{site.careers_url}/{external_path}"

    return "Not listed"


def simplify_job(site: WorkdaySite, job_posting: dict[str, Any]) -> dict[str, str]:
    """
    Convert the raw Workday posting into a simple preview dictionary.

    This is NOT the official CareerSignal normalized job shape yet.
    That comes in Step 12B.
    """

    return {
        "title": str(job_posting.get("title") or "Untitled"),
        "location": get_job_location(job_posting),
        "job_url": build_job_url(site, job_posting),
        "external_job_id": get_external_job_id(job_posting),
    }


def fetch_all_workday_jobs(
    site: WorkdaySite,
    limit: int = 20,
    max_pages: int = 5,
    sleep_seconds: float = 0.5,
) -> list[dict[str, str]]:
    """
    Fetch Workday jobs with pagination.

    This keeps a max_pages limit on purpose.
    Some Workday companies have thousands of jobs.
    For Step 12A, we only need proof that the connector works.
    """

    all_jobs: list[dict[str, str]] = []
    offset = 0

    for page_number in range(1, max_pages + 1):
        print(f"Fetching page {page_number} with offset {offset}...")

        page_data = fetch_workday_page(
            site=site,
            offset=offset,
            limit=limit,
        )

        total = page_data.get("total")
        raw_jobs = page_data.get("jobPostings", [])

        if not isinstance(raw_jobs, list):
            raise ValueError(
                "Expected Workday response field 'jobPostings' to be a list. "
                f"Received: {type(raw_jobs)}"
            )

        print(f"Page returned {len(raw_jobs)} jobs. Total reported by Workday: {total}")

        for raw_job in raw_jobs:
            if isinstance(raw_job, dict):
                all_jobs.append(simplify_job(site, raw_job))

        if not raw_jobs:
            break

        offset += limit

        if isinstance(total, int) and offset >= total:
            break

        time.sleep(sleep_seconds)

    return all_jobs


def print_site_details(site: WorkdaySite) -> None:
    """
    Print the parsed Workday site information.
    """

    print("\nWorkday site details")
    print("--------------------")
    print(f"Original URL:  {site.original_url}")
    print(f"Tenant:        {site.tenant}")
    print(f"Server:        {site.server}")
    print(f"Site name:     {site.site}")
    print(f"Careers URL:   {site.careers_url}")
    print(f"Jobs endpoint: {site.jobs_endpoint}")


def print_jobs(jobs: list[dict[str, str]]) -> None:
    """
    Print a clean list of fetched jobs.
    """

    print("\nJobs found")
    print("----------")

    if not jobs:
        print("No jobs found.")
        return

    for index, job in enumerate(jobs, start=1):
        print(f"\n{index}. {job['title']}")
        print(f"   Location:        {job['location']}")
        print(f"   External Job ID: {job['external_job_id']}")
        print(f"   URL:             {job['job_url']}")


def print_debug_response(site: WorkdaySite) -> None:
    """
    Fetch one page and print the raw JSON response.

    Use this when the endpoint works but the fields are not what we expected.
    """

    page_data = fetch_workday_page(
        site=site,
        offset=0,
        limit=1,
    )

    print(json.dumps(page_data, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preview jobs from one Workday career site."
    )

    parser.add_argument(
        "--url",
        default=DEFAULT_WORKDAY_URL,
        help="Workday career URL to test.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of jobs to request per page.",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=2,
        help="Maximum number of pages to fetch.",
    )

    parser.add_argument(
        "--debug-json",
        action="store_true",
        help="Print raw JSON for the first Workday result page.",
    )

    args = parser.parse_args()

    try:
        site = parse_workday_url(args.url)
        print_site_details(site)

        if args.debug_json:
            print_debug_response(site)
            return

        jobs = fetch_all_workday_jobs(
            site=site,
            limit=args.limit,
            max_pages=args.max_pages,
        )

        print_jobs(jobs)

        print("\nSummary")
        print("-------")
        print(f"Total jobs printed: {len(jobs)}")

    except requests.exceptions.HTTPError as error:
        print("\nHTTP error while calling Workday.")
        print("---------------------------------")
        print(f"Error: {error}")

        if error.response is not None:
            print(f"Status code: {error.response.status_code}")
            print(f"Response text preview: {error.response.text[:1000]}")

        print("\nCommon causes:")
        print("- The tenant, server, or site name was parsed incorrectly.")
        print("- The company uses a different Workday URL format.")
        print("- The Workday site blocks this endpoint.")
        print("- The URL is not actually a Workday myworkdayjobs.com URL.")

    except requests.exceptions.RequestException as error:
        print("\nRequest error while calling Workday.")
        print("------------------------------------")
        print(f"Error: {error}")

        print("\nCommon causes:")
        print("- Internet connection issue.")
        print("- Workday endpoint timed out.")
        print("- The site refused the connection.")

    except ValueError as error:
        print("\nWorkday parsing or response error.")
        print("----------------------------------")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()