from careersignal.config_loader import load_active_companies


def main():
    active_companies = load_active_companies()

    print(f"Loaded {len(active_companies)} active companies:")
    print()

    for company in active_companies:
        print(f"Company: {company['company_name']}")
        print(f"ATS Type: {company['ats_type']}")
        print(f"Career URL: {company['career_url']}")
        print(f"Target Locations: {company['target_locations']}")
        print(f"Keywords: {company['keywords']}")
        print(f"Job Title Keywords: {company['job_title_keywords']}")
        print(f"Excluded Keywords: {company['excluded_keywords']}")
        print("-" * 50)


if __name__ == "__main__":
    main()