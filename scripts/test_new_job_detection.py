from datetime import date

from careersignal.database import (
    insert_or_update_jobs,
    get_jobs_first_seen_in_last_24_hours,
    print_job_summary,
)


def main():
    today = date.today().isoformat()

    sample_jobs = [
        {
            "company_name": "Example Company",
            "source_ats": "greenhouse",
            "external_job_id": "12345",
            "title": "Accounting Intern",
            "location": "Remote, United States",
            "department": "Finance",
            "job_url": "https://example.com/jobs/12345",
            "posted_date": "2026-05-24T12:00:00-04:00",
            "date_collected": today,
        },
        {
            "company_name": "Example Company",
            "source_ats": "greenhouse",
            "external_job_id": "67890",
            "title": "Financial Analyst",
            "location": "Raleigh, NC",
            "department": "Accounting",
            "job_url": "https://example.com/jobs/67890",
            "posted_date": "2026-05-24T12:00:00-04:00",
            "date_collected": today,
        },
        {
            "company_name": "Example Company",
            "source_ats": "greenhouse",
            "external_job_id": "99999",
            "title": "New Staff Accountant",
            "location": "Charlotte, NC",
            "department": "Accounting",
            "job_url": "https://example.com/jobs/99999",
            "posted_date": "2026-05-24T12:00:00-04:00",
            "date_collected": today,
        },
    ]

    summary = insert_or_update_jobs(sample_jobs)
    print_job_summary(summary)

    recent_jobs = get_jobs_first_seen_in_last_24_hours()

    print()
    print("Jobs first seen in the last 24 hours:")
    print("-------------------------------------")

    for job in recent_jobs:
        company_name, title, location, department, job_url, first_seen_date, last_seen_date = job

        print(f"- {company_name} | {title} | {location}")
        print(f"  First seen: {first_seen_date}")
        print(f"  Last seen:  {last_seen_date}")
        print(f"  URL:        {job_url}")


if __name__ == "__main__":
    main()