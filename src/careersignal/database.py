import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from careersignal.match_scoring import score_job


DATABASE_PATH = Path("data/careersignal.db")


def get_connection(db_path=DATABASE_PATH):
    """
    Opens a connection to the SQLite database.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection


def get_current_timestamp():
    """
    Returns the current UTC timestamp as a clean ISO string.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def column_exists(cursor, table_name, column_name):
    """
    Checks whether a column already exists in a SQLite table.
    """
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        if column["name"] == column_name:
            return True

    return False


def add_column_if_missing(cursor, table_name, column_name, column_definition):
    """
    Adds a column only if it does not already exist.
    """
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )


def initialize_database(db_path=DATABASE_PATH):
    """
    Creates the database tables and required columns.

    Supports:
    - job storage
    - new job detection
    - match scoring
    - run logging
    """

    with get_connection(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                source_ats TEXT NOT NULL,
                external_job_id TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT,
                department TEXT,
                job_url TEXT,
                posted_date TEXT,
                first_seen_date TEXT NOT NULL,
                last_seen_date TEXT NOT NULL,
                date_collected TEXT,
                match_score INTEGER DEFAULT 0,
                match_notes TEXT
            );
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_job
            ON jobs (company_name, source_ats, external_job_id);
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS run_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TEXT NOT NULL,
                source_ats TEXT,
                company_name TEXT,
                jobs_found INTEGER DEFAULT 0,
                jobs_inserted INTEGER DEFAULT 0,
                jobs_updated INTEGER DEFAULT 0,
                run_status TEXT,
                notes TEXT
            );
            """
        )

        # Keeps older databases compatible after Step 8.
        add_column_if_missing(cursor, "jobs", "match_score", "INTEGER DEFAULT 0")
        add_column_if_missing(cursor, "jobs", "match_notes", "TEXT")

        connection.commit()


def insert_or_update_jobs(jobs, db_path=DATABASE_PATH):
    """
    Inserts new jobs and updates existing jobs.

    Existing jobs:
    - refreshed title/location/department/job_url/posted_date/date_collected
    - updated last_seen_date
    - updated match_score
    - updated match_notes

    New jobs:
    - inserted with first_seen_date
    - inserted with last_seen_date
    - inserted with match_score
    - inserted with match_notes
    """

    initialize_database(db_path)

    now = get_current_timestamp()

    jobs_found = len(jobs)
    jobs_inserted = 0
    jobs_updated = 0
    new_jobs = []

    with get_connection(db_path) as connection:
        cursor = connection.cursor()

        for job in jobs:
            score_result = score_job(job)

            job["match_score"] = score_result["match_score"]
            job["match_notes"] = score_result["match_notes"]

            company_name = job["company_name"]
            source_ats = job["source_ats"]
            external_job_id = job["external_job_id"]

            cursor.execute(
                """
                SELECT id
                FROM jobs
                WHERE company_name = ?
                  AND source_ats = ?
                  AND external_job_id = ?;
                """,
                (company_name, source_ats, external_job_id),
            )

            existing_job = cursor.fetchone()

            if existing_job:
                cursor.execute(
                    """
                    UPDATE jobs
                    SET
                        title = ?,
                        location = ?,
                        department = ?,
                        job_url = ?,
                        posted_date = ?,
                        last_seen_date = ?,
                        date_collected = ?,
                        match_score = ?,
                        match_notes = ?
                    WHERE company_name = ?
                      AND source_ats = ?
                      AND external_job_id = ?;
                    """,
                    (
                        job.get("title"),
                        job.get("location"),
                        job.get("department"),
                        job.get("job_url"),
                        job.get("posted_date"),
                        now,
                        job.get("date_collected"),
                        job.get("match_score"),
                        job.get("match_notes"),
                        company_name,
                        source_ats,
                        external_job_id,
                    ),
                )

                jobs_updated += 1

            else:
                cursor.execute(
                    """
                    INSERT INTO jobs (
                        company_name,
                        source_ats,
                        external_job_id,
                        title,
                        location,
                        department,
                        job_url,
                        posted_date,
                        first_seen_date,
                        last_seen_date,
                        date_collected,
                        match_score,
                        match_notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        company_name,
                        source_ats,
                        external_job_id,
                        job.get("title"),
                        job.get("location"),
                        job.get("department"),
                        job.get("job_url"),
                        job.get("posted_date"),
                        now,
                        now,
                        job.get("date_collected"),
                        job.get("match_score"),
                        job.get("match_notes"),
                    ),
                )

                jobs_inserted += 1
                new_jobs.append(job)

        connection.commit()

    summary = {
        "jobs_found": jobs_found,
        "jobs_inserted": jobs_inserted,
        "jobs_updated": jobs_updated,
        "new_jobs": new_jobs,
    }

    insert_run_log(
        source_ats="mixed",
        company_name="mixed",
        jobs_found=jobs_found,
        jobs_inserted=jobs_inserted,
        jobs_updated=jobs_updated,
        run_status="success",
        db_path=db_path,
    )

    return summary


def insert_run_log(
    source_ats=None,
    company_name=None,
    jobs_found=0,
    jobs_inserted=0,
    jobs_updated=0,
    run_status="success",
    notes=None,
    db_path=DATABASE_PATH,
):
    """
    Inserts a run log row.
    """

    initialize_database(db_path)

    run_timestamp = get_current_timestamp()

    with get_connection(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO run_log (
                run_timestamp,
                source_ats,
                company_name,
                jobs_found,
                jobs_inserted,
                jobs_updated,
                run_status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                run_timestamp,
                source_ats,
                company_name,
                jobs_found,
                jobs_inserted,
                jobs_updated,
                run_status,
                notes,
            ),
        )

        connection.commit()


def get_jobs_first_seen_in_last_24_hours(db_path=DATABASE_PATH):
    """
    Returns jobs where first_seen_date is within the last 24 hours.
    Results are sorted by match score first.
    """

    initialize_database(db_path)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    cutoff_string = cutoff.replace(microsecond=0).isoformat()

    with get_connection(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                company_name,
                source_ats,
                external_job_id,
                title,
                location,
                department,
                job_url,
                posted_date,
                first_seen_date,
                last_seen_date,
                date_collected,
                match_score,
                match_notes
            FROM jobs
            WHERE first_seen_date >= ?
            ORDER BY match_score DESC, first_seen_date DESC;
            """,
            (cutoff_string,),
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def get_all_jobs(db_path=DATABASE_PATH):
    """
    Returns all stored jobs, sorted by match score.
    Useful for testing and DB checks.
    """

    initialize_database(db_path)

    with get_connection(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                company_name,
                source_ats,
                external_job_id,
                title,
                location,
                department,
                job_url,
                posted_date,
                first_seen_date,
                last_seen_date,
                date_collected,
                match_score,
                match_notes
            FROM jobs
            ORDER BY match_score DESC, last_seen_date DESC;
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def print_job_summary(summary):
    """
    Prints a clean summary of the database update.
    """

    print()
    print("Job detection summary:")
    print("----------------------")
    print(f"Jobs found:    {summary['jobs_found']}")
    print(f"Jobs inserted: {summary['jobs_inserted']}")
    print(f"Jobs updated:  {summary['jobs_updated']}")
    print(f"New jobs:      {len(summary['new_jobs'])}")

    if summary["new_jobs"]:
        print()
        print("New jobs found:")
        print("---------------")

        for job in summary["new_jobs"]:
            print(
                f"- {job['company_name']} | "
                f"{job['title']} | "
                f"{job.get('location', 'No location')} | "
                f"{job.get('match_score', 0)}/100"
            )
            print(f"  Why: {job.get('match_notes', 'No match notes')}")
            print(f"  {job.get('job_url', 'No URL')}")
    else:
        print()
        print("No new jobs found.")