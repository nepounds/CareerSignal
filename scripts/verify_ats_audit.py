import csv
from pathlib import Path

import requests


INPUT_PATH = Path("config/company_ats_audit.csv")
OUTPUT_PATH = Path("config/company_ats_audit_verification_results.csv")

TIMEOUT_SECONDS = 15

ATS_PATTERNS = {
    "workday": [
        "myworkdayjobs.com",
        "/wday/cxs/",
    ],
    "greenhouse": [
        "boards.greenhouse.io",
        "job-boards.greenhouse.io",
        "greenhouse.io",
    ],
    "oracle": [
        "oraclecloud.com",
        "fa.us2.oraclecloud.com",
        "hcmUI/CandidateExperience",
    ],
    "lever": [
        "jobs.lever.co",
        "lever.co",
    ],
    "icims": [
        "icims.com",
        "careers.icims.com",
    ],
    "smartrecruiters": [
        "smartrecruiters.com",
    ],
    "ashby": [
        "jobs.ashbyhq.com",
        "ashbyhq.com",
    ],
    "avature": [
        "avature.net",
    ],
    "adp": [
        "adp.com",
        "workforcenow.adp.com",
    ],
    "neogov": [
        "governmentjobs.com",
        "neogov.com",
    ],
    "usajobs": [
        "usajobs.gov",
    ],
}


def normalize(value):
    return (value or "").strip().lower()


def guess_ats_from_text(url, html):
    combined = f"{url}\n{html}".lower()

    for ats_type, patterns in ATS_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in combined:
                return ats_type

    return "unknown"


def fetch_url(url):
    if not url:
        return {
            "http_status": "",
            "final_url": "",
            "detected_ats": "missing_url",
            "error": "missing career_url",
        }

    try:
        response = requests.get(
            url,
            timeout=TIMEOUT_SECONDS,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 CareerSignal ATS audit verification "
                    "(local portfolio project)"
                )
            },
            allow_redirects=True,
        )

        html_sample = response.text[:50000] if response.text else ""
        detected_ats = guess_ats_from_text(response.url, html_sample)

        return {
            "http_status": str(response.status_code),
            "final_url": response.url,
            "detected_ats": detected_ats,
            "error": "",
        }

    except requests.RequestException as error:
        return {
            "http_status": "",
            "final_url": "",
            "detected_ats": "error",
            "error": str(error),
        }


def classify_result(row, check):
    listed_ats = normalize(row.get("ats_type"))
    detected_ats = normalize(check.get("detected_ats"))
    status = normalize(row.get("status"))

    if check["error"]:
        return "needs_manual_review"

    if check["http_status"] and not check["http_status"].startswith(("2", "3")):
        return "needs_manual_review"

    if listed_ats in {"greenhouse", "workday"}:
        if detected_ats == listed_ats:
            return "supported_verified"
        return "supported_mismatch_review"

    if listed_ats in {
        "oracle",
        "lever",
        "icims",
        "smartrecruiters",
        "ashby",
        "avature",
        "adp",
        "neogov",
        "usajobs",
    }:
        if detected_ats == listed_ats:
            return "unsupported_verified"
        return "unsupported_mismatch_review"

    if status == "manual_only":
        return "manual_only_review"

    return "needs_manual_review"


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Could not find {INPUT_PATH}")

    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    new_columns = [
        "http_status",
        "final_url",
        "detected_ats",
        "verification_result",
        "verification_error",
    ]

    output_fieldnames = fieldnames + [
        column for column in new_columns if column not in fieldnames
    ]

    verified_rows = []

    for index, row in enumerate(rows, start=1):
        company_name = row.get("company_name", "")
        career_url = row.get("career_url", "")

        print(f"[{index}/{len(rows)}] Checking {company_name}...")

        check = fetch_url(career_url)
        verification_result = classify_result(row, check)

        row["http_status"] = check["http_status"]
        row["final_url"] = check["final_url"]
        row["detected_ats"] = check["detected_ats"]
        row["verification_result"] = verification_result
        row["verification_error"] = check["error"]

        verified_rows.append(row)

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(verified_rows)

    print()
    print(f"Verification complete: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()