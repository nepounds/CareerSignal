"""
Initialize the CareerSignal manual application tracker table.

Run from the project root:

    python scripts/init_application_tracker.py
"""

from careersignal.application_tracker_db import initialize_application_tracker


def main() -> None:
    initialize_application_tracker()
    print("Application tracker table initialized in data/careersignal.db")


if __name__ == "__main__":
    main()