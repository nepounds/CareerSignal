from careersignal.match_scoring import score_job


sample_jobs = [
    {
        "title": "Staff Accountant",
        "location": "Raleigh, NC",
        "department": "Accounting",
        "description": (
            "Prepare journal entries, reconciliations, and month-end reports. "
            "Excel experience preferred. 1-3 years of experience preferred."
        ),
    },
    {
        "title": "Financial Analyst",
        "location": "Remote, United States",
        "department": "Finance",
        "description": "Build reports using Excel, SQL, and Power BI. Bachelor's degree preferred.",
    },
    {
        "title": "Business Analyst",
        "location": "Hybrid - Durham, NC",
        "department": "Operations",
        "description": "Analyze business processes, reporting metrics, dashboards, and workflow improvements.",
    },
    {
        "title": "Operations Analyst",
        "location": "Clayton, NC",
        "department": "Operations",
        "description": "Support operations reporting, Excel tracking, KPIs, compliance, and process improvement.",
    },
    {
        "title": "Compliance Analyst",
        "location": "Raleigh, NC",
        "department": "Compliance",
        "description": "Review regulatory documentation, internal controls, and quality control processes.",
    },
    {
        "title": "Reporting Analyst",
        "location": "Remote - North Carolina",
        "department": "Data",
        "description": "Create dashboards and reports using Excel, SQL, and Power BI.",
    },
    {
        "title": "Plant Supervisor",
        "location": "Smithfield, NC",
        "department": "Manufacturing",
        "description": "Supervise plant operations, quality control, production schedules, and safety processes.",
    },
    {
        "title": "Water Treatment Supervisor",
        "location": "Goldsboro, NC",
        "department": "Utilities",
        "description": "Oversee water operations, compliance, reporting, and plant staff.",
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
        "title": "Software Engineer",
        "location": "Raleigh, NC",
        "department": "Technology",
        "description": "Build software products using Python and cloud tools.",
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
        print(f"Department: {job['department']}")
        print(f"Score: {result['match_score']}")
        print(f"Notes: {result['match_notes']}")

        assert 0 <= result["match_score"] <= 100
        assert "match_notes" in result
        assert isinstance(result["match_notes"], str)


if __name__ == "__main__":
    main()