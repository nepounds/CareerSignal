from careersignal.database import get_connection, fetch_all_jobs


def main():
    with get_connection() as connection:
        jobs = fetch_all_jobs(connection)

        if not jobs:
            print("No jobs found in the database yet.")
            return

        print(f"Found {len(jobs)} jobs:")
        print()

        for job in jobs:
            print(f"Company: {job['company_name']}")
            print(f"Title: {job['title']}")
            print(f"Location: {job['location']}")
            print(f"Department: {job['department']}")
            print(f"URL: {job['job_url']}")
            print(f"First seen: {job['first_seen_date']}")
            print(f"Last seen: {job['last_seen_date']}")
            print("-" * 50)


if __name__ == "__main__":
    main()