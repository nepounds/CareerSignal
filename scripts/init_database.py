from careersignal.database import initialize_database, DATABASE_PATH


def main():
    initialize_database()
    print(f"Database initialized at: {DATABASE_PATH}")


if __name__ == "__main__":
    main()