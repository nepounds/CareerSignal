from pathlib import Path
import csv


def parse_list_field(value):
    """
    Converts a semicolon-separated text field into a Python list.

    Example:
    "Raleigh NC;Remote;North Carolina"

    becomes:

    ["Raleigh NC", "Remote", "North Carolina"]
    """
    if not value:
        return []

    return [item.strip() for item in value.split(";") if item.strip()]


def parse_active(value):
    """
    Converts the active column from text into True or False.

    Examples:
    TRUE -> True
    FALSE -> False
    yes -> True
    no -> False
    """
    if not value:
        return False

    return value.strip().lower() in ["true", "yes", "y", "1"]


def load_companies(config_path="config/company_config.csv"):
    """
    Loads all companies from the company config CSV file.
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Could not find company config file at: {path}")

    companies = []

    with path.open(mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            company = {
                "company_name": row["company_name"].strip(),
                "ats_type": row["ats_type"].strip().lower(),
                "career_url": row["career_url"].strip(),
                "target_locations": parse_list_field(row["target_locations"]),
                "keywords": parse_list_field(row["keywords"]),
                "job_title_keywords": parse_list_field(row["job_title_keywords"]),
                "excluded_keywords": parse_list_field(row["excluded_keywords"]),
                "active": parse_active(row["active"]),
            }

            companies.append(company)

    return companies


def load_active_companies(config_path="config/company_config.csv"):
    """
    Loads only companies marked active in the CSV file.
    """
    companies = load_companies(config_path)

    active_companies = [
        company for company in companies
        if company["active"]
    ]

    return active_companies