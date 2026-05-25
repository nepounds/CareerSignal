from careersignal.database import (
    get_connection,
    create_tables,
    insert_normalized_jobs,
    insert_run_log,
    fetch_all_jobs,
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
    with get_connection() as connection:
        create_tables(connection)

        summary = insert_normalized_jobs(connection, sample_jobs)

        insert_run_log(
            connection=connection,
            source_ats="greenhouse",
            company_name="Example Company",
            jobs_found=summary["jobs_found"],
            jobs_inserted=summary["jobs_inserted"],
            jobs_updated=summary["jobs_updated"],
            run_status="success",
        )

        jobs = fetch_all_jobs(connection)

        print("Database test complete.")
        print()
        print("Insert summary:")
        print(summary)
        print()
        print("Stored jobs:")

        for job in jobs:
            print(
                f"- {job['company_name']} | {job['title']} | "
                f"{job['location']} | {job['job_url']}"
            )


if __name__ == "__main__":
    main()