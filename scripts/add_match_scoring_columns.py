import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/careersignal.db")


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        if column[1] == column_name:
            return True

    return False


def add_column_if_missing(cursor, table_name, column_name, column_definition):
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )
        print(f"Added column: {column_name}")
    else:
        print(f"Column already exists: {column_name}")


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DATABASE_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    add_column_if_missing(
        cursor,
        table_name="jobs",
        column_name="match_score",
        column_definition="INTEGER DEFAULT 0",
    )

    add_column_if_missing(
        cursor,
        table_name="jobs",
        column_name="match_notes",
        column_definition="TEXT",
    )

    connection.commit()
    connection.close()

    print("Match scoring columns are ready.")


if __name__ == "__main__":
    main()