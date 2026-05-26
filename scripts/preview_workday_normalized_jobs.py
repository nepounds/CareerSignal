from __future__ import annotations

import argparse
from pprint import pprint

from careersignal.collectors.workday import (
    NORMALIZED_JOB_FIELDS,
    fetch_and_normalize_workday_jobs,
    validate_normalized_job_shape,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview normalized Workday jobs without touching the main CareerSignal pipeline."
    )

    parser.add_argument(
        "--api-url",
        required=True,
        help="Workday CXS API jobs URL from the Step 12A proof of concept.",
    )

    parser.add_argument(
        "--company-name",
        required=True,
        help="Company name to place into normalized job dictionaries.",
    )

    parser.add_argument(
        "--job-url-base",
        required=False,
        default=None,
        help="Public Workday career site base URL used to build clean job links.",
    )

    parser.add_argument(
        "--search-text",
        required=False,
        default="",
        help="Optional Workday search text.",
    )

    parser.add_argument(
        "--limit",
        required=False,
        type=int,
        default=10,
        help="Number of Workday jobs to preview.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    normalized_jobs = fetch_and_normalize_workday_jobs(
        api_url=args.api_url,
        company_name=args.company_name,
        job_url_base=args.job_url_base,
        search_text=args.search_text,
        limit=args.limit,
    )

    print()
    print("Normalized Workday Preview")
    print("=" * 60)
    print(f"Company: {args.company_name}")
    print(f"Jobs returned: {len(normalized_jobs)}")
    print()

    if not normalized_jobs:
        print("No jobs returned.")
        return

    print("Official normalized fields:")
    for field_name in NORMALIZED_JOB_FIELDS:
        print(f"- {field_name}")

    print()
    print("Preview jobs:")
    print("=" * 60)

    for index, job in enumerate(normalized_jobs, start=1):
        validate_normalized_job_shape(job)

        print()
        print(f"Job #{index}")
        print("-" * 60)
        pprint(job, sort_dicts=False)

    print()
    print("Shape check passed.")
    print("Every normalized Workday job has the official CareerSignal fields.")


if __name__ == "__main__":
    main()