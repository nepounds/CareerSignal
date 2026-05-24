"""
Test script for the CareerSignal job normalizer.

Run this from the project root with:

python scripts/test_job_normalizer.py
"""

from careersignal.job_normalizer import normalize_jobs, validate_normalized_job


def main():
    raw_greenhouse_jobs = [
        {
            "id": 12345,
            "title": "Accounting Intern",
            "location": {"name": "Remote, United States"},
            "departments": [{"name": "Finance"}],
            "absolute_url": "https://example.com/jobs/12345",
            "updated_at": "2026-05-24T12:00:00-04:00",
        },
        {
            "id": 67890,
            "title": "Financial Analyst",
            "location": {"name": "Raleigh, NC"},
            "departments": [{"name": "Accounting"}],
            "absolute_url": "https://example.com/jobs/67890",
            "updated_at": "2026-05-23T09:30:00-04:00",
        },
    ]

    normalized_jobs = normalize_jobs(
        raw_jobs=raw_greenhouse_jobs,
        company_name="Example Company",
        source_ats="greenhouse",
    )

    print("Normalized jobs:")
    print()

    for job in normalized_jobs:
        print(job)
        print()

        is_valid = validate_normalized_job(job)

        if not is_valid:
            raise ValueError("A normalized job is missing one or more required fields.")

    print(f"Success. Normalized {len(normalized_jobs)} jobs.")


if __name__ == "__main__":
    main()