from pathlib import Path
from urllib.parse import urlparse
import csv


AUDIT_PATH = Path("config/ats_coverage_audit.csv")
OUTPUT_PATH = Path("config/company_config_generated.csv")

SUPPORTED_ATS_TYPES = {"workday", "greenhouse"}

DEFAULT_TARGET_LOCATION = "Raleigh NC;Remote;North Carolina"
DEFAULT_KEYWORDS = "accounting;tax;audit;analyst;associate"
DEFAULT_JOB_TITLE_KEYWORDS = (
    "associate;staff;entry level;tax associate;audit associate;"
    "accounting associate;analyst"
)
DEFAULT_EXCLUDED_KEYWORDS = (
    "senior;manager;director;principal;partner;intern;internship;campus;student"
)


def clean(value):
    """Return a stripped string, even when the original value is blank."""
    return (value or "").strip()


def normalize(value):
    """Return a lowercase stripped string."""
    return clean(value).lower()


def build_workday_api_url(career_url):
    """
    Convert a direct Workday career URL into the Workday CXS API URL.

    Example:
    https://amgen.wd1.myworkdayjobs.com/Careers

    becomes:
    https://amgen.wd1.myworkdayjobs.com/wday/cxs/amgen/Careers/jobs
    """
    career_url = clean(career_url)

    if not career_url:
        return ""

    parsed_url = urlparse(career_url)
    host = parsed_url.netloc.strip()
    path = parsed_url.path.strip("/")

    if "myworkdayjobs.com" not in host:
        return ""

    if not path:
        return ""

    tenant = host.split(".")[0]

    return f"https://{host}/wday/cxs/{tenant}/{path}/jobs"


def get_status_for_supported_row(ats_type):
    """
    Generated rows should be inactive by default.

    This keeps the collector from trying to run 100 companies at once.
    Turn selected rows to TRUE manually after reviewing them.
    """
    return "FALSE"


def main():
    if not AUDIT_PATH.exists():
        raise FileNotFoundError(f"Could not find {AUDIT_PATH}")

    ready_companies = []
    skipped_count = 0

    with AUDIT_PATH.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {"company_name", "career_url", "ats_type", "status"}
        missing_columns = required_columns - set(reader.fieldnames or [])

        if missing_columns:
            raise ValueError(
                f"Missing required column(s) in {AUDIT_PATH}: "
                f"{', '.join(sorted(missing_columns))}"
            )

        for row in reader:
            company = clean(row.get("company_name"))
            career_url = clean(row.get("career_url"))
            ats_type = normalize(row.get("ats_type"))
            status = normalize(row.get("status"))

            if status != "ready_now":
                skipped_count += 1
                continue

            if ats_type not in SUPPORTED_ATS_TYPES:
                skipped_count += 1
                continue

            if not company or not career_url:
                skipped_count += 1
                continue

            workday_api_url = ""

            if ats_type == "workday":
                workday_api_url = build_workday_api_url(career_url)

                if not workday_api_url:
                    print(
                        f"Warning: Could not build Workday API URL for "
                        f"{company}: {career_url}"
                    )

            ready_companies.append(
                {
                    "company": company,
                    "ats_type": ats_type,
                    "career_url": career_url,
                    "workday_api_url": workday_api_url,
                    "job_url_base": "",
                    "target_location": DEFAULT_TARGET_LOCATION,
                    "keywords": DEFAULT_KEYWORDS,
                    "job_title_keywords": DEFAULT_JOB_TITLE_KEYWORDS,
                    "excluded_keywords": DEFAULT_EXCLUDED_KEYWORDS,
                    "is_active": get_status_for_supported_row(ats_type),
                }
            )

    ready_companies.sort(key=lambda row: (row["ats_type"], row["company"]))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
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

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ready_companies)

    print(f"Wrote {len(ready_companies)} ready companies to {OUTPUT_PATH}")
    print(f"Skipped {skipped_count} companies that are not ready_now/supported.")
    print("Generated companies are inactive by default: is_active = FALSE")

    workday_count = sum(1 for row in ready_companies if row["ats_type"] == "workday")
    greenhouse_count = sum(1 for row in ready_companies if row["ats_type"] == "greenhouse")

    print()
    print("Generated ATS counts:")
    print(f"- workday: {workday_count}")
    print(f"- greenhouse: {greenhouse_count}")


if __name__ == "__main__":
    main()