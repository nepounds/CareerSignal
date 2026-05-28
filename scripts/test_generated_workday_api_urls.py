from pathlib import Path
import csv
import requests


CONFIG_PATH = Path("config/company_config_generated.csv")
OUTPUT_PATH = Path("config/workday_api_url_test_results.csv")


def clean(value):
    return (value or "").strip()


def test_workday_api_url(company, api_url):
    payload = {
        "appliedFacets": {},
        "limit": 5,
        "offset": 0,
        "searchText": "",
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "CareerSignal/1.0",
    }

    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response_text_sample = response.text[:300].replace("\n", " ").replace("\r", " ")

        return {
            "company": company,
            "workday_api_url": api_url,
            "status_code": response.status_code,
            "success": "yes" if response.status_code == 200 else "no",
            "response_sample": response_text_sample,
        }

    except requests.RequestException as error:
        return {
            "company": company,
            "workday_api_url": api_url,
            "status_code": "ERROR",
            "success": "no",
            "response_sample": str(error),
        }


def main():
    results = []

    with CONFIG_PATH.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            company = clean(row.get("company"))
            ats_type = clean(row.get("ats_type")).lower()
            api_url = clean(row.get("workday_api_url"))

            if ats_type != "workday":
                continue

            if not api_url:
                results.append(
                    {
                        "company": company,
                        "workday_api_url": "",
                        "status_code": "MISSING",
                        "success": "no",
                        "response_sample": "Missing workday_api_url",
                    }
                )
                continue

            print(f"Testing {company}...")
            result = test_workday_api_url(company, api_url)
            results.append(result)

            print(f"  Status: {result['status_code']}")

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "company",
            "workday_api_url",
            "status_code",
            "success",
            "response_sample",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    successful = [row for row in results if row["success"] == "yes"]
    failed = [row for row in results if row["success"] != "yes"]

    print()
    print("Workday API URL Test Summary")
    print("----------------------------")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Results written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()