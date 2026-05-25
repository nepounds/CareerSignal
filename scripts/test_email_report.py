import argparse

from careersignal.email_report import build_and_send_daily_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Test CareerSignal daily email report.")

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the email preview without sending.",
    )

    parser.add_argument(
        "--send",
        action="store_true",
        help="Send a real test email.",
    )

    args = parser.parse_args()

    if not args.preview and not args.send:
        print("Choose one mode:")
        print("  python scripts/test_email_report.py --preview")
        print("  python scripts/test_email_report.py --send")
        return

    if args.preview and args.send:
        print("Choose only one mode: --preview or --send")
        return

    sample_summary = {
        "companies_checked": 3,
        "jobs_found": 25,
        "jobs_inserted": 2,
        "jobs_updated": 23,
        "new_jobs": 2,
    }

    sample_new_jobs = [
        {
            "company_name": "Example Company",
            "title": "Accounting Intern",
            "location": "Remote, United States",
            "job_url": "https://example.com/jobs/12345",
        },
        {
            "company_name": "Another Company",
            "title": "Financial Analyst",
            "location": "Raleigh, NC",
            "job_url": "https://example.com/jobs/67890",
        },
    ]

    sample_failed_sources = []

    test_mode = args.preview

    build_and_send_daily_report(
        summary=sample_summary,
        new_jobs=sample_new_jobs,
        failed_sources=sample_failed_sources,
        test_mode=test_mode,
    )


if __name__ == "__main__":
    main()