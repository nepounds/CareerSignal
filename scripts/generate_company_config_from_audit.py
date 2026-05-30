import csv
from pathlib import Path
from urllib.parse import urlparse


AUDIT_PATH = Path("config/company_ats_audit.csv")
OUTPUT_PATH = Path("config/company_config_candidate.csv")

SUPPORTED_ATS_TYPES = {"workday", "greenhouse"}

DEFAULT_TARGET_LOCATION = "North Carolina"

DEFAULT_KEYWORDS = (
    "accounting,finance,analyst,business,operations,compliance,"
    "reporting,supervisor,plant,water,wastewater,utility"
)

DEFAULT_JOB_TITLE_KEYWORDS = (
    "accountant,accounting analyst,financial analyst,finance analyst,"
    "business analyst,operations analyst,compliance analyst,"
    "reporting analyst,data analyst,plant supervisor,"
    "operations supervisor,utility analyst"
)

DEFAULT_EXCLUDED_KEYWORDS = (
    "senior manager,director,principal,software engineer,developer,"
    "nurse,physician,sales executive,truck driver,warehouse associate"
)


CONFIG_COLUMNS = [
    "company",
    "ats_type",
    "career_url",
    "workday_api_url",
    "job_url_base",
    "target_location",
    "keywords",
    "job_title_keywords",
    "excluded_keywords",
    "is_active",
]


def clean(value):
    return (value or "").strip()


def lower_clean(value):
    return clean(value).lower()


def build_workday_urls(career_url):
    """
    Converts a public Workday career URL into the likely CXS API URL.

    Example:
    https://company.wd1.myworkdayjobs.com/Careers

    becomes:
    https://company.wd1.myworkdayjobs.com/wday/cxs/company/Careers/jobs

    Some Workday sites may still need manual repair after collector testing.
    """
    parsed = urlparse(career_url)

    if "myworkdayjobs.com" not in parsed.netloc:
        return "", ""

    host = parsed.netloc
    path_parts = [part for part in parsed.path.split("/") if part]

    if not path_parts:
        return "", career_url

    site_name = path_parts[0]
    tenant = host.split(".")[0]

    workday_api_url = f"https://{host}/wday/cxs/{tenant}/{site_name}/jobs"
    job_url_base = f"https://{host}/{site_name}"

    return workday_api_url, job_url_base


def build_config_row(audit_row):
    company = clean(
        audit_row.get("company_name")
        or audit_row.get("company")
        or audit_row.get("Company")
    )

    ats_type = lower_clean(audit_row.get("ats_type"))
    career_url = clean(audit_row.get("career_url"))

    workday_api_url = ""
    job_url_base = ""

    if ats_type == "workday":
        workday_api_url, job_url_base = build_workday_urls(career_url)

    return {
        "company": company,
        "ats_type": ats_type,
        "career_url": career_url,
        "workday_api_url": workday_api_url,
        "job_url_base": job_url_base,
        "target_location": DEFAULT_TARGET_LOCATION,
        "keywords": DEFAULT_KEYWORDS,
        "job_title_keywords": DEFAULT_JOB_TITLE_KEYWORDS,
        "excluded_keywords": DEFAULT_EXCLUDED_KEYWORDS,
        "is_active": "TRUE",
    }


def main():
    if not AUDIT_PATH.exists():
        raise FileNotFoundError(f"Could not find {AUDIT_PATH}")

    with AUDIT_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        audit_rows = list(reader)

    config_rows = []
    skipped_rows = []

    for row in audit_rows:
        company = clean(row.get("company_name") or row.get("company"))
        ats_type = lower_clean(row.get("ats_type"))
        status = lower_clean(row.get("status"))

        if status == "ready_now" and ats_type in SUPPORTED_ATS_TYPES:
            config_rows.append(build_config_row(row))
        else:
            skipped_rows.append(
                {
                    "company": company,
                    "ats_type": ats_type,
                    "status": status,
                }
            )

    config_rows = sorted(config_rows, key=lambda row: row["company"].lower())

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CONFIG_COLUMNS)
        writer.writeheader()
        writer.writerows(config_rows)

    print(f"Created: {OUTPUT_PATH}")
    print(f"Config rows created: {len(config_rows)}")
    print(f"Audit rows skipped: {len(skipped_rows)}")
    print()
    print("Included companies:")
    for row in config_rows:
        print(f"- {row['company']} ({row['ats_type']})")


if __name__ == "__main__":
    main()