from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
DATABASE_PATH = PROJECT_ROOT / "data" / "careersignal.db"
EXPORTS_DIR = PROJECT_ROOT / "exports"
DEFAULT_EXPORT_PATH = EXPORTS_DIR / "careersignal_export.xlsx"


if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from careersignal.application_tracker import fetch_applications  # noqa: E402
from careersignal.match_scoring import score_job  # noqa: E402


APPLICATION_EXPORT_COLUMNS = [
    "application_id",
    "date_applied",
    "company_name",
    "job_title",
    "job_url",
    "source",
    "status",
    "first_response_date",
    "interview_date",
    "final_response_date",
    "notes",
    "created_at",
    "updated_at",
]

NEGATIVE_OUTCOME_STATUSES = {"rejected", "ghosted"}
ACTIVE_STATUSES = {"applied"}
INTERVIEW_STATUSES = {"interview"}
ACCEPTED_STATUSES = {"accepted"}
REJECTED_STATUSES = {"rejected"}
GHOSTED_STATUSES = {"ghosted"}


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
    """
    result = connection.execute(query, (table_name,)).fetchone()
    return result is not None


def get_existing_table_name(
    connection: sqlite3.Connection,
    possible_table_names: list[str],
) -> str | None:
    for table_name in possible_table_names:
        if table_exists(connection, table_name):
            return table_name

    return None


def read_table(connection: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, connection)


def extract_match_score(scoring_result: Any) -> float | None:
    """
    Handles a few possible score_job return styles safely.

    Expected best case:
    - score_job(job) returns a number

    Also supported:
    - score_job(job) returns {"match_score": 85}
    """

    if scoring_result is None:
        return None

    if isinstance(scoring_result, (int, float)):
        return float(scoring_result)

    if isinstance(scoring_result, dict):
        possible_keys = ["match_score", "score", "total_score"]

        for key in possible_keys:
            if key in scoring_result:
                try:
                    return float(scoring_result[key])
                except (TypeError, ValueError):
                    return None

    return None


def add_match_scores(jobs_df: pd.DataFrame) -> pd.DataFrame:
    if jobs_df.empty:
        jobs_df["match_score"] = pd.Series(dtype="float")
        return jobs_df

    scored_jobs_df = jobs_df.copy()

    scores = []

    for _, row in scored_jobs_df.iterrows():
        job = row.to_dict()

        try:
            scoring_result = score_job(job)
            match_score = extract_match_score(scoring_result)
        except Exception as error:
            print(
                f"Warning: Could not score job "
                f"'{job.get('title', 'Unknown')}'. Error: {error}"
            )
            match_score = None

        scores.append(match_score)

    scored_jobs_df["match_score"] = scores

    return scored_jobs_df


def sort_jobs(jobs_df: pd.DataFrame) -> pd.DataFrame:
    if jobs_df.empty:
        return jobs_df

    sort_columns = []

    if "match_score" in jobs_df.columns:
        sort_columns.append("match_score")

    if "first_seen_date" in jobs_df.columns:
        sort_columns.append("first_seen_date")

    if not sort_columns:
        return jobs_df

    ascending_values = []

    for column in sort_columns:
        if column == "match_score":
            ascending_values.append(False)
        else:
            ascending_values.append(False)

    return jobs_df.sort_values(
        by=sort_columns,
        ascending=ascending_values,
        na_position="last",
    )


def get_new_jobs(jobs_df: pd.DataFrame) -> pd.DataFrame:
    if jobs_df.empty:
        return jobs_df.copy()

    if "first_seen_date" not in jobs_df.columns:
        return pd.DataFrame(columns=jobs_df.columns)

    new_jobs_df = jobs_df.copy()

    new_jobs_df["first_seen_date_parsed"] = pd.to_datetime(
        new_jobs_df["first_seen_date"],
        errors="coerce",
        utc=True,
    )

    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(hours=24)

    new_jobs_df = new_jobs_df[
        new_jobs_df["first_seen_date_parsed"] >= cutoff
    ].copy()

    new_jobs_df = new_jobs_df.drop(columns=["first_seen_date_parsed"])

    return sort_jobs(new_jobs_df)


def get_high_match_jobs(jobs_df: pd.DataFrame, minimum_score: float) -> pd.DataFrame:
    if jobs_df.empty:
        return jobs_df.copy()

    if "match_score" not in jobs_df.columns:
        return pd.DataFrame(columns=jobs_df.columns)

    high_match_jobs_df = jobs_df[
        jobs_df["match_score"].fillna(0) >= minimum_score
    ].copy()

    return sort_jobs(high_match_jobs_df)


def build_company_summary(jobs_df: pd.DataFrame) -> pd.DataFrame:
    if jobs_df.empty:
        return pd.DataFrame(
            columns=[
                "company_name",
                "total_jobs",
                "high_match_jobs",
                "best_match_score",
                "average_match_score",
            ]
        )

    if "company_name" not in jobs_df.columns:
        return pd.DataFrame()

    summary_df = jobs_df.copy()

    if "match_score" not in summary_df.columns:
        summary_df["match_score"] = None

    company_summary_df = (
        summary_df.groupby("company_name", dropna=False)
        .agg(
            total_jobs=("title", "count"),
            high_match_jobs=(
                "match_score",
                lambda scores: (scores.fillna(0) >= 70).sum(),
            ),
            best_match_score=("match_score", "max"),
            average_match_score=("match_score", "mean"),
        )
        .reset_index()
    )

    company_summary_df = company_summary_df.sort_values(
        by=["high_match_jobs", "best_match_score", "total_jobs"],
        ascending=[False, False, False],
        na_position="last",
    )

    return company_summary_df


def parse_date_safely(value: Any) -> date | None:
    """
    Convert a stored date value to a date object, or return None.
    """

    if not value:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None


def calculate_days_since_applied(date_applied: Any) -> int | None:
    """
    Calculate days since date_applied without changing database records.
    """

    parsed_date = parse_date_safely(date_applied)

    if parsed_date is None:
        return None

    return (date.today() - parsed_date).days


def get_aging_bucket(days_since_applied: int | None, status: str) -> str:
    """
    Return an aging bucket for reporting only.

    This function does not update the database.
    """

    if status != "applied":
        return "responded / closed"

    if days_since_applied is None:
        return "missing or invalid application date"

    if days_since_applied <= 14:
        return "active / normal waiting period"

    if days_since_applied <= 30:
        return "rejection danger zone"

    if days_since_applied <= 60:
        return "ghosting danger zone"

    return "ghosted candidate / should be reviewed"


def build_applications_dataframe() -> pd.DataFrame:
    """
    Build the row-level Applications export sheet.
    """

    applications = fetch_applications()

    if not applications:
        return pd.DataFrame(columns=APPLICATION_EXPORT_COLUMNS)

    applications_df = pd.DataFrame(applications)

    for column in APPLICATION_EXPORT_COLUMNS:
        if column not in applications_df.columns:
            applications_df[column] = ""

    return applications_df[APPLICATION_EXPORT_COLUMNS]


def build_application_summary_dataframe(
    applications_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build overall Application Tracker summary totals.
    """

    if applications_df.empty:
        summary_rows = [
            ("total_applications", 0),
            ("active_applications", 0),
            ("interviews", 0),
            ("acceptances", 0),
            ("formal_rejections", 0),
            ("ghostings", 0),
            ("negative_outcomes", 0),
        ]
    else:
        statuses = applications_df["status"].fillna("").str.lower()

        summary_rows = [
            ("total_applications", len(applications_df)),
            ("active_applications", statuses.isin(ACTIVE_STATUSES).sum()),
            ("interviews", statuses.isin(INTERVIEW_STATUSES).sum()),
            ("acceptances", statuses.isin(ACCEPTED_STATUSES).sum()),
            ("formal_rejections", statuses.isin(REJECTED_STATUSES).sum()),
            ("ghostings", statuses.isin(GHOSTED_STATUSES).sum()),
            ("negative_outcomes", statuses.isin(NEGATIVE_OUTCOME_STATUSES).sum()),
        ]

    return pd.DataFrame(summary_rows, columns=["metric", "value"])


def build_company_application_summary_dataframe(
    applications_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build company-level Application Tracker summary totals.
    """

    columns = [
        "company_name",
        "total_applications",
        "active_applications",
        "interviews",
        "acceptances",
        "formal_rejections",
        "ghostings",
        "negative_outcomes",
    ]

    if applications_df.empty:
        return pd.DataFrame(columns=columns)

    summary_df = applications_df.copy()
    summary_df["status"] = summary_df["status"].fillna("").str.lower()

    grouped_rows = []

    for company_name, company_rows in summary_df.groupby(
        "company_name",
        dropna=False,
    ):
        statuses = company_rows["status"]

        grouped_rows.append(
            {
                "company_name": company_name,
                "total_applications": len(company_rows),
                "active_applications": statuses.isin(ACTIVE_STATUSES).sum(),
                "interviews": statuses.isin(INTERVIEW_STATUSES).sum(),
                "acceptances": statuses.isin(ACCEPTED_STATUSES).sum(),
                "formal_rejections": statuses.isin(REJECTED_STATUSES).sum(),
                "ghostings": statuses.isin(GHOSTED_STATUSES).sum(),
                "negative_outcomes": statuses.isin(
                    NEGATIVE_OUTCOME_STATUSES
                ).sum(),
            }
        )

    return pd.DataFrame(grouped_rows, columns=columns).sort_values(
        by=["total_applications", "company_name"],
        ascending=[False, True],
    )


def build_application_aging_dataframe(
    applications_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build aging bucket report without changing application statuses.
    """

    columns = [
        "application_id",
        "company_name",
        "job_title",
        "date_applied",
        "status",
        "days_since_applied",
        "aging_bucket",
    ]

    if applications_df.empty:
        return pd.DataFrame(columns=columns)

    aging_df = applications_df.copy()

    aging_df["status"] = aging_df["status"].fillna("").str.lower()

    aging_df["days_since_applied"] = aging_df["date_applied"].apply(
        calculate_days_since_applied
    )

    aging_df["aging_bucket"] = aging_df.apply(
        lambda row: get_aging_bucket(
            row["days_since_applied"],
            row["status"],
        ),
        axis=1,
    )

    return aging_df[columns].sort_values(
        by=["days_since_applied", "company_name"],
        ascending=[False, True],
        na_position="last",
    )


def clean_sheet_name(sheet_name: str) -> str:
    """
    Excel sheet names cannot be longer than 31 characters.
    """

    return sheet_name[:31]


def write_sheet(
    writer: pd.ExcelWriter,
    sheet_name: str,
    dataframe: pd.DataFrame,
) -> None:
    safe_sheet_name = clean_sheet_name(sheet_name)

    dataframe.to_excel(
        writer,
        sheet_name=safe_sheet_name,
        index=False,
    )

    worksheet = writer.sheets[safe_sheet_name]

    worksheet.freeze_panes = "A2"

    for column_cells in worksheet.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter

        for cell in column_cells:
            cell_value = cell.value

            if cell_value is None:
                continue

            max_length = max(max_length, len(str(cell_value)))

        adjusted_width = min(max_length + 2, 60)
        worksheet.column_dimensions[column_letter].width = adjusted_width


def write_application_tracker_sheets(writer: pd.ExcelWriter) -> None:
    """
    Write Application Tracker sheets into the existing CareerSignal export workbook.
    """

    applications_df = build_applications_dataframe()

    application_summary_df = build_application_summary_dataframe(
        applications_df
    )

    company_application_summary_df = build_company_application_summary_dataframe(
        applications_df
    )

    application_aging_df = build_application_aging_dataframe(
        applications_df
    )

    write_sheet(writer, "Applications", applications_df)
    write_sheet(writer, "Application Summary", application_summary_df)
    write_sheet(
        writer,
        "Company Application Summary",
        company_application_summary_df,
    )
    write_sheet(writer, "Application Aging", application_aging_df)


def export_to_excel(
    database_path: Path = DATABASE_PATH,
    export_path: Path = DEFAULT_EXPORT_PATH,
    minimum_match_score: float = 70,
) -> Path:
    if not database_path.exists():
        raise FileNotFoundError(
            f"Database not found: {database_path}. "
            "Run the collector first, then try the export again."
        )

    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        if not table_exists(connection, "jobs"):
            raise RuntimeError("Could not find a 'jobs' table in the database.")

        all_jobs_df = read_table(connection, "jobs")
        all_jobs_df = add_match_scores(all_jobs_df)
        all_jobs_df = sort_jobs(all_jobs_df)

        new_jobs_df = get_new_jobs(all_jobs_df)

        high_match_jobs_df = get_high_match_jobs(
            all_jobs_df,
            minimum_score=minimum_match_score,
        )

        company_summary_df = build_company_summary(all_jobs_df)

        daily_runs_table_name = get_existing_table_name(
            connection,
            ["daily_runs", "run_logs"],
        )

        failed_sources_table_name = get_existing_table_name(
            connection,
            ["failed_sources", "source_failures"],
        )

        daily_runs_df = (
            read_table(connection, daily_runs_table_name)
            if daily_runs_table_name
            else pd.DataFrame()
        )

        failed_sources_df = (
            read_table(connection, failed_sources_table_name)
            if failed_sources_table_name
            else pd.DataFrame()
        )

    with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
        write_sheet(writer, "New Jobs", new_jobs_df)
        write_sheet(writer, "All Jobs", all_jobs_df)
        write_sheet(writer, "High Match Jobs", high_match_jobs_df)
        write_sheet(writer, "Company Summary", company_summary_df)

        if not daily_runs_df.empty:
            write_sheet(writer, "Daily Runs", daily_runs_df)

        if not failed_sources_df.empty:
            write_sheet(writer, "Failed Sources", failed_sources_df)

        write_application_tracker_sheets(writer)

    return export_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export CareerSignal SQLite data to an Excel workbook."
    )

    parser.add_argument(
        "--output",
        default=str(DEFAULT_EXPORT_PATH),
        help="Path for the Excel export file.",
    )

    parser.add_argument(
        "--minimum-match-score",
        type=float,
        default=70,
        help="Minimum match score for the High Match Jobs sheet.",
    )

    args = parser.parse_args()

    export_path = export_to_excel(
        database_path=DATABASE_PATH,
        export_path=Path(args.output),
        minimum_match_score=args.minimum_match_score,
    )

    print("Excel export complete.")
    print(f"Export file: {export_path}")


if __name__ == "__main__":
    main()