# CareerSignal

CareerSignal is a Python portfolio project that tracks job postings from target companies and sends alerts when new matching jobs appear.

## Project Goal

The goal of this project is to help job seekers monitor companies they care about instead of manually checking each career page every day.

## Planned Features

- Store a list of target companies
- Check company career pages for new job postings
- Filter jobs by location, title, and keywords
- Save discovered jobs in a local SQLite database
- Avoid sending duplicate alerts
- Send email alerts when new matching jobs are found

## Tech Stack

- Python
- SQLite
- Requests
- BeautifulSoup
- python-dotenv
- GitHub

## Project Structure

```text
CareerSignal/
├── src/
│   └── careersignal/
│       ├── __init__.py
│       └── main.py
├── data/
├── logs/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python src/careersignal/main.py
```

Expected output:

```text
CareerSignal is running.
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your real settings.

Do not commit `.env` to GitHub.

## Current Status

Step 1 complete: basic project structure, virtual environment, starter files, and Git setup.

## Future Improvements

- Add company configuration file
- Add scraper for one test company
- Add SQLite database setup
- Add duplicate job detection
- Add email alerts
- Add scheduled runs