import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATABASE_PATH = Path("data/careersignal.db")


def get_connection(db_path=DATABASE_PATH):
    """
    Opens a connection to the SQLite database.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def initialize_database(db_path=DATABASE_PATH):
    """
    Creates the jobs table if it does not already exist.
    Also makes sure we have the columns needed for new job detection.
    """

    with get_connection(db_path) as conn:
        cursor = conn.cursor()

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
                date_collected TEXT
            );
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_job
            ON jobs (company_name, source_ats, external_job_id);
            """
        )

        conn.commit()


def get_current_timestamp():
    """
    Returns the current UTC timestamp as a clean ISO string.

    Example:
    2026-05-24T18:42:11+00:00
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def insert_or_update_jobs(jobs, db_path=DATABASE_PATH):
    """
    Inserts new jobs and updates existing jobs.

    Existing jobs:
    - last_seen_date gets updated

    New jobs:
    - first_seen_date gets set
    - last_seen_date gets set

    Returns a summary dictionary.
    """

    initialize_database(db_path)

    now = get_current_timestamp()

    jobs_found = len(jobs)
    jobs_inserted = 0
    jobs_updated = 0
    new_jobs = []

    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        for job in jobs:
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
                    SET title = ?,
                        location = ?,
                        department = ?,
                        job_url = ?,
                        posted_date = ?,
                        last_seen_date = ?,
                        date_collected = ?
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
                        date_collected
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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
                    ),
                )

                jobs_inserted += 1
                new_jobs.append(job)

        conn.commit()

    return {
        "jobs_found": jobs_found,
        "jobs_inserted": jobs_inserted,
        "jobs_updated": jobs_updated,
        "new_jobs": new_jobs,
    }


def get_jobs_first_seen_in_last_24_hours(db_path=DATABASE_PATH):
    """
    Returns jobs where first_seen_date is within the last 24 hours.
    """

    initialize_database(db_path)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    cutoff_string = cutoff.replace(microsecond=0).isoformat()

    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                company_name,
                title,
                location,
                department,
                job_url,
                first_seen_date,
                last_seen_date
            FROM jobs
            WHERE first_seen_date >= ?
            ORDER BY first_seen_date DESC;
            """,
            (cutoff_string,),
        )

        rows = cursor.fetchall()

    return rows


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
            print(f"- {job['company_name']} | {job['title']} | {job.get('location', 'No location')}")
            print(f"  {job.get('job_url', 'No URL')}")
    else:
        print()
        print("No new jobs found.")