from careersignal.database import (
    initialize_database,
    insert_or_update_jobs,
    get_all_jobs,
)


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
        "date_collected": "2026-05-24",
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
        "date_collected": "2026-05-24",
    },
]


def main():
    initialize_database()

    summary = insert_or_update_jobs(sample_jobs)

    jobs = get_all_jobs()

    print("Database test complete.")
    print()
    print("Insert summary:")
    print(summary)
    print()
    print("Stored jobs:")

    for job in jobs:
        print(
            f"- {job['company_name']} | "
            f"{job['title']} | "
            f"{job['location']} | "
            f"{job['match_score']}/100 | "
            f"{job['job_url']}"
        )


if __name__ == "__main__":
    main()