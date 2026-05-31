import sqlite3


def main() -> None:
    conn = sqlite3.connect("data/careersignal.db")

    result = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'applications';
    """).fetchone()

    print(result)


if __name__ == "__main__":
    main()