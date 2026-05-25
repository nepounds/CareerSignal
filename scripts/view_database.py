from careersignal.database import get_all_jobs


def main():
    jobs = get_all_jobs()

    print("Stored jobs:")
    print("------------")

    for job in jobs:
        print(
            f"- {job['company_name']} | "
            f"{job['title']} | "
            f"{job['location']} | "
            f"{job.get('match_score', 0)}/100 | "
            f"{job['job_url']}"
        )

        match_notes = job.get("match_notes")

        if match_notes:
            print(f"  Why: {match_notes}")

        print()


if __name__ == "__main__":
    main()