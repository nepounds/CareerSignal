from careersignal.match_scoring import score_job


sample_jobs = [
    {
        "title": "Staff Accountant",
        "location": "Raleigh, NC",
        "department": "Accounting",
        "description": "Prepare journal entries, reconciliations, and month-end reports. Excel experience preferred.",
    },
    {
        "title": "Financial Analyst",
        "location": "Remote, United States",
        "department": "Finance",
        "description": "Build reports using Excel, SQL, and Power BI.",
    },
    {
        "title": "Senior Manager, Tax",
        "location": "Raleigh, NC",
        "department": "Tax",
        "description": "CPA required. Minimum of 7 years of public accounting experience required.",
    },
    {
        "title": "Director of Finance",
        "location": "Charlotte, NC",
        "department": "Finance",
        "description": "People management and leadership experience required.",
    },
    {
        "title": "Accounting Associate",
        "location": "Hybrid - Durham, NC",
        "department": "Accounting",
        "description": "Entry-level role supporting accounts payable, accounts receivable, and reconciliations.",
    },
]


def main():
    for job in sample_jobs:
        result = score_job(job)

        print("=" * 80)
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"Score: {result['match_score']}")
        print(f"Notes: {result['match_notes']}")


if __name__ == "__main__":
    main()