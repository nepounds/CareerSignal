"""
Terminal summary reporting for the CareerSignal Application Tracker.

Step 17E only adds manual terminal reporting.
It does not modify the daily job alert email, Excel export, Power BI, or database schema.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from careersignal.application_tracker import fetch_applications  # noqa: E402


ACTIVE_STATUSES = {"applied"}
INTERVIEW_STATUSES = {"interview"}
ACCEPTED_STATUSES = {"accepted"}
REJECTED_STATUSES = {"rejected"}
GHOSTED_STATUSES = {"ghosted"}
NEGATIVE_OUTCOME_STATUSES = {"rejected", "ghosted"}

NO_RESPONSE_STATUSES = {"applied"}


AGING_BUCKETS = {
    "normal_waiting_period": "0-14 days: active / normal waiting period",
    "rejection_danger_zone": "15-30 days: rejection danger zone",
    "ghosting_danger_zone": "31-60 days: ghosting danger zone",
    "ghosted_by_age": "61+ days: should be considered ghosted if still marked applied",
}


def parse_iso_date(value: str) -> date:
    """
    Parse a YYYY-MM-DD date string.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{value}'. Use YYYY-MM-DD."
        ) from exc


def get_application_date(application: dict[str, Any]) -> date | None:
    """
    Return the parsed date_applied value for an application.
    """
    raw_date = application.get("date_applied")

    if not raw_date:
        return None

    if isinstance(raw_date, date):
        return raw_date

    try:
        return datetime.strptime(str(raw_date), "%Y-%m-%d").date()
    except ValueError:
        return None


def calculate_application_age_days(
    application: dict[str, Any],
    as_of_date: date,
) -> int | None:
    """
    Calculate how many days old an application is.
    """
    applied_date = get_application_date(application)

    if applied_date is None:
        return None

    return (as_of_date - applied_date).days


def get_aging_bucket(
    application: dict[str, Any],
    as_of_date: date,
) -> str | None:
    """
    Place an application into an aging bucket.

    Aging buckets only apply to applications that are still marked applied.
    """
    status = str(application.get("status", "")).strip().lower()

    if status not in NO_RESPONSE_STATUSES:
        return None

    age_days = calculate_application_age_days(application, as_of_date)

    if age_days is None:
        return None

    if age_days <= 14:
        return "normal_waiting_period"

    if 15 <= age_days <= 30:
        return "rejection_danger_zone"

    if 31 <= age_days <= 60:
        return "ghosting_danger_zone"

    return "ghosted_by_age"


def filter_applications_by_company(
    applications: list[dict[str, Any]],
    company_name: str | None,
) -> list[dict[str, Any]]:
    """
    Filter applications by company name if a company filter was provided.
    """
    if not company_name:
        return applications

    normalized_filter = company_name.strip().lower()

    return [
        application
        for application in applications
        if str(application.get("company_name", "")).strip().lower()
        == normalized_filter
    ]


def count_by_company(
    applications: list[dict[str, Any]],
    allowed_statuses: set[str] | None = None,
) -> Counter[str]:
    """
    Count applications by company.

    If allowed_statuses is provided, only applications with one of those statuses
    are counted.
    """
    company_counts: Counter[str] = Counter()

    for application in applications:
        status = str(application.get("status", "")).strip().lower()

        if allowed_statuses is not None and status not in allowed_statuses:
            continue

        company_name = str(application.get("company_name", "")).strip()

        if not company_name:
            company_name = "(Missing company name)"

        company_counts[company_name] += 1

    return company_counts


def build_summary(
    applications: list[dict[str, Any]],
    as_of_date: date,
) -> dict[str, Any]:
    """
    Build all report totals from application records.
    """
    status_counts: Counter[str] = Counter(
        str(application.get("status", "")).strip().lower()
        for application in applications
    )

    aging_counts: Counter[str] = Counter()
    aging_lists: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)

    for application in applications:
        bucket = get_aging_bucket(application, as_of_date)

        if bucket is None:
            continue

        aging_counts[bucket] += 1
        aging_lists[bucket].append(application)

    summary = {
        "total_applications": len(applications),
        "active_applications": status_counts["applied"],
        "interviews": status_counts["interview"],
        "acceptances": status_counts["accepted"],
        "formal_rejections": status_counts["rejected"],
        "ghostings": status_counts["ghosted"],
        "negative_outcomes": (
            status_counts["rejected"] + status_counts["ghosted"]
        ),
        "status_counts": status_counts,
        "totals_by_company": count_by_company(applications),
        "interviews_by_company": count_by_company(
            applications,
            INTERVIEW_STATUSES,
        ),
        "rejections_by_company": count_by_company(
            applications,
            REJECTED_STATUSES,
        ),
        "ghostings_by_company": count_by_company(
            applications,
            GHOSTED_STATUSES,
        ),
        "acceptances_by_company": count_by_company(
            applications,
            ACCEPTED_STATUSES,
        ),
        "aging_counts": aging_counts,
        "aging_lists": aging_lists,
    }

    return summary


def print_section(title: str) -> None:
    """
    Print a clean section heading.
    """
    print()
    print(title)
    print("-" * len(title))


def print_counter(counter: Counter[str], empty_message: str) -> None:
    """
    Print a Counter in descending count order.
    """
    if not counter:
        print(empty_message)
        return

    for name, count in counter.most_common():
        print(f"{name}: {count}")


def format_application_line(
    application: dict[str, Any],
    as_of_date: date,
) -> str:
    """
    Format one application row for terminal output.
    """
    application_id = application.get("application_id", "")
    company_name = application.get("company_name", "")
    job_title = application.get("job_title", "")
    status = application.get("status", "")
    date_applied = application.get("date_applied", "")

    age_days = calculate_application_age_days(application, as_of_date)
    age_text = "unknown age" if age_days is None else f"{age_days} days old"

    return (
        f"ID {application_id} | {company_name} | {job_title} | "
        f"{status} | applied {date_applied} | {age_text}"
    )


def print_application_list(
    title: str,
    applications: list[dict[str, Any]],
    as_of_date: date,
    empty_message: str,
) -> None:
    """
    Print a list of applications.
    """
    print_section(title)

    if not applications:
        print(empty_message)
        return

    sorted_applications = sorted(
        applications,
        key=lambda application: (
            get_application_date(application) or date.min,
            str(application.get("company_name", "")),
            str(application.get("job_title", "")),
        ),
    )

    for application in sorted_applications:
        print(format_application_line(application, as_of_date))


def print_report(
    applications: list[dict[str, Any]],
    as_of_date: date,
    show_all: bool,
    company_filter: str | None,
) -> None:
    """
    Print the full Application Tracker report.
    """
    summary = build_summary(applications, as_of_date)

    print()
    print("CareerSignal Application Tracker Report")
    print("=======================================")
    print(f"As of: {as_of_date.isoformat()}")

    if company_filter:
        print(f"Company filter: {company_filter}")

    print_section("Overall Totals")
    print(f"Total applications: {summary['total_applications']}")
    print(f"Active applications: {summary['active_applications']}")
    print(f"Interviews: {summary['interviews']}")
    print(f"Acceptances: {summary['acceptances']}")

    print_section("Outcome Totals")
    print(f"Formal rejections: {summary['formal_rejections']}")
    print(f"Ghostings: {summary['ghostings']}")
    print(
        "Negative outcomes: "
        f"{summary['negative_outcomes']} "
        "(formal rejections + ghostings)"
    )

    print_section("Totals by Company")
    print_counter(
        summary["totals_by_company"],
        "No company totals to show.",
    )

    print_section("Interviews by Company")
    print_counter(
        summary["interviews_by_company"],
        "No interviews to show.",
    )

    print_section("Rejections by Company")
    print_counter(
        summary["rejections_by_company"],
        "No rejections to show.",
    )

    print_section("Ghostings by Company")
    print_counter(
        summary["ghostings_by_company"],
        "No ghostings to show.",
    )

    print_section("Acceptances by Company")
    print_counter(
        summary["acceptances_by_company"],
        "No acceptances to show.",
    )

    print_section("Application Aging Buckets")
    for bucket_key, bucket_label in AGING_BUCKETS.items():
        print(f"{bucket_label}: {summary['aging_counts'][bucket_key]}")

    print_application_list(
        "Applications in Rejection Danger Zone",
        summary["aging_lists"]["rejection_danger_zone"],
        as_of_date,
        "No applications are currently in the rejection danger zone.",
    )

    print_application_list(
        "Applications in Ghosting Danger Zone",
        summary["aging_lists"]["ghosting_danger_zone"],
        as_of_date,
        "No applications are currently in the ghosting danger zone.",
    )

    print_application_list(
        "Applications 61+ Days Old Still Marked Applied",
        summary["aging_lists"]["ghosted_by_age"],
        as_of_date,
        "No applications are currently 61+ days old and still marked applied.",
    )

    if show_all:
        print_application_list(
            "All Applications",
            applications,
            as_of_date,
            "No applications to show.",
        )


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Print a terminal summary report for Application Tracker records."
    )

    parser.add_argument(
        "--show-all",
        action="store_true",
        help="List all applications after the summary sections.",
    )

    parser.add_argument(
        "--company",
        help="Only report applications for one exact company name.",
    )

    parser.add_argument(
        "--as-of",
        type=parse_iso_date,
        default=date.today(),
        help="Use a fixed report date for aging logic. Format: YYYY-MM-DD.",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the Application Tracker report.
    """
    args = parse_args()

    applications = fetch_applications()
    applications = filter_applications_by_company(applications, args.company)

    print_report(
        applications=applications,
        as_of_date=args.as_of,
        show_all=args.show_all,
        company_filter=args.company,
    )


if __name__ == "__main__":
    main()