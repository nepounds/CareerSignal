import sqlite3
from pathlib import Path
from typing import Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "careersignal.db"


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Opens a connection to the SQLite database.

    If no database path is provided, it uses:
    data/careersignal.db
    """
    DATA_DIR.mkdir(exist_ok=True)

    if db_path is None:
        db_path = DATABASE_PATH

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    """
    Creates the CareerSignal database tables if they do not already exist.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL UNIQUE,
            source_ats TEXT NOT NULL,
            careers_url TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            date_added TEXT NOT NULL DEFAULT CURRENT_DATE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_postings (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            source_ats TEXT NOT NULL,
            external_job_id TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            department TEXT,
            job_url TEXT,
            posted_date TEXT,
            date_collected TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            first_seen_date TEXT NOT NULL DEFAULT CURRENT_DATE,
            last_seen_date TEXT NOT NULL DEFAULT CURRENT_DATE,

            FOREIGN KEY (company_id) REFERENCES companies(company_id),

            UNIQUE (source_ats, external_job_id)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS run_logs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT NOT NULL DEFAULT CURRENT_DATE,
            source_ats TEXT NOT NULL,
            company_name TEXT,
            jobs_found INTEGER NOT NULL DEFAULT 0,
            jobs_inserted INTEGER NOT NULL DEFAULT 0,
            jobs_updated INTEGER NOT NULL DEFAULT 0,
            run_status TEXT NOT NULL,
            error_message TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    connection.commit()


def initialize_database(db_path: Optional[Path] = None) -> None:
    """
    Opens the database and creates all tables.
    """

    with get_connection(db_path) as connection:
        create_tables(connection)


def get_or_create_company(
    connection: sqlite3.Connection,
    company_name: str,
    source_ats: str,
    careers_url: Optional[str] = None,
) -> int:
    """
    Finds a company by name.

    If the company does not exist yet, it inserts it.

    Returns the company_id.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT company_id
        FROM companies
        WHERE company_name = ?;
        """,
        (company_name,),
    )

    existing_company = cursor.fetchone()

    if existing_company:
        return existing_company["company_id"]

    cursor.execute(
        """
        INSERT INTO companies (
            company_name,
            source_ats,
            careers_url
        )
        VALUES (?, ?, ?);
        """,
        (company_name, source_ats, careers_url),
    )

    connection.commit()

    return cursor.lastrowid


def insert_or_update_job(
    connection: sqlite3.Connection,
    normalized_job: Dict,
) -> str:
    """
    Inserts a normalized job posting into the database.

    If the job already exists, it updates the job details and last_seen_date.

    Returns:
    - "inserted"
    - "updated"
    """

    company_id = get_or_create_company(
        connection=connection,
        company_name=normalized_job["company_name"],
        source_ats=normalized_job["source_ats"],
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT job_id
        FROM job_postings
        WHERE source_ats = ?
          AND external_job_id = ?;
        """,
        (
            normalized_job["source_ats"],
            normalized_job["external_job_id"],
        ),
    )

    existing_job = cursor.fetchone()

    if existing_job:
        cursor.execute(
            """
            UPDATE job_postings
            SET
                company_id = ?,
                title = ?,
                location = ?,
                department = ?,
                job_url = ?,
                posted_date = ?,
                date_collected = ?,
                last_seen_date = CURRENT_DATE,
                is_active = 1
            WHERE source_ats = ?
              AND external_job_id = ?;
            """,
            (
                company_id,
                normalized_job["title"],
                normalized_job.get("location"),
                normalized_job.get("department"),
                normalized_job.get("job_url"),
                normalized_job.get("posted_date"),
                normalized_job["date_collected"],
                normalized_job["source_ats"],
                normalized_job["external_job_id"],
            ),
        )

        connection.commit()
        return "updated"

    cursor.execute(
        """
        INSERT INTO job_postings (
            company_id,
            source_ats,
            external_job_id,
            title,
            location,
            department,
            job_url,
            posted_date,
            date_collected
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            company_id,
            normalized_job["source_ats"],
            normalized_job["external_job_id"],
            normalized_job["title"],
            normalized_job.get("location"),
            normalized_job.get("department"),
            normalized_job.get("job_url"),
            normalized_job.get("posted_date"),
            normalized_job["date_collected"],
        ),
    )

    connection.commit()
    return "inserted"


def insert_normalized_jobs(
    connection: sqlite3.Connection,
    normalized_jobs: List[Dict],
) -> Dict[str, int]:
    """
    Inserts a list of normalized jobs.

    Returns a small summary dictionary.
    """

    summary = {
        "jobs_found": len(normalized_jobs),
        "jobs_inserted": 0,
        "jobs_updated": 0,
    }

    for job in normalized_jobs:
        result = insert_or_update_job(connection, job)

        if result == "inserted":
            summary["jobs_inserted"] += 1
        elif result == "updated":
            summary["jobs_updated"] += 1

    return summary


def insert_run_log(
    connection: sqlite3.Connection,
    source_ats: str,
    company_name: Optional[str],
    jobs_found: int,
    jobs_inserted: int,
    jobs_updated: int,
    run_status: str,
    error_message: Optional[str] = None,
) -> None:
    """
    Inserts a record into the run_logs table.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO run_logs (
            source_ats,
            company_name,
            jobs_found,
            jobs_inserted,
            jobs_updated,
            run_status,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (
            source_ats,
            company_name,
            jobs_found,
            jobs_inserted,
            jobs_updated,
            run_status,
            error_message,
        ),
    )

    connection.commit()


def fetch_all_jobs(connection: sqlite3.Connection) -> List[sqlite3.Row]:
    """
    Fetches all stored job postings with their company names.
    Useful for testing.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            job_postings.job_id,
            companies.company_name,
            job_postings.source_ats,
            job_postings.external_job_id,
            job_postings.title,
            job_postings.location,
            job_postings.department,
            job_postings.job_url,
            job_postings.posted_date,
            job_postings.date_collected,
            job_postings.first_seen_date,
            job_postings.last_seen_date,
            job_postings.is_active
        FROM job_postings
        JOIN companies
            ON job_postings.company_id = companies.company_id
        ORDER BY companies.company_name, job_postings.title;
        """
    )

    return cursor.fetchall()