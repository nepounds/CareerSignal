import re


BASE_SCORE = 25


TITLE_RULES = {
    # Accounting
    "staff accountant": 32,
    "junior accountant": 30,
    "accounting analyst": 30,
    "accounting associate": 28,
    "accounting specialist": 24,
    "accountant": 26,
    "accounts payable": 24,
    "accounts receivable": 24,
    "audit associate": 26,
    "tax associate": 24,
    "assurance associate": 24,

    # Finance
    "financial analyst": 32,
    "finance analyst": 30,
    "fp&a analyst": 30,
    "budget analyst": 28,
    "pricing analyst": 26,
    "revenue analyst": 26,
    "cost accountant": 28,
    "billing analyst": 24,

    # Analyst lanes
    "business analyst": 30,
    "operations analyst": 30,
    "compliance analyst": 30,
    "reporting analyst": 30,
    "data analyst": 28,
    "process analyst": 26,
    "program analyst": 24,
    "quality analyst": 24,
    "risk analyst": 24,
    "internal controls analyst": 28,
    "procurement analyst": 22,
    "purchasing analyst": 22,
    "contract analyst": 22,
    "claims analyst": 22,
    "implementation analyst": 22,

    # Supervisor / operations lanes
    "plant supervisor": 30,
    "operations supervisor": 30,
    "production supervisor": 26,
    "utility supervisor": 28,
    "water treatment supervisor": 30,
    "wastewater supervisor": 30,

    # Public utility / water-adjacent
    "utility billing analyst": 30,
    "public works analyst": 28,
    "environmental compliance specialist": 26,
    "water plant operator": 20,
    "wastewater plant operator": 20,

    # Broader-but-still-useful matches
    "analyst": 18,
    "associate": 14,
    "specialist": 12,
    "coordinator": 10,
    "assistant": 8,
    "trainee": 12,
    "entry level": 14,
    "entry-level": 14,
    "junior": 14,
    "rotational": 10,
    "development program": 10,
}


KEYWORD_RULES = {
    # Accounting / finance
    "journal entries": 8,
    "reconciliations": 8,
    "reconciliation": 8,
    "month-end": 7,
    "month end": 7,
    "general ledger": 8,
    "financial statements": 7,
    "gaap": 6,
    "accounts payable": 6,
    "accounts receivable": 6,
    "budget": 5,
    "forecast": 5,
    "variance analysis": 6,
    "cost accounting": 6,

    # Data / reporting
    "excel": 6,
    "power bi": 6,
    "sql": 6,
    "python": 4,
    "reporting": 6,
    "dashboard": 5,
    "data analysis": 6,
    "metrics": 4,
    "kpi": 4,

    # Compliance / public sector / operations
    "compliance": 6,
    "internal controls": 6,
    "quality control": 6,
    "regulatory": 5,
    "public sector": 5,
    "government": 4,
    "utility operations": 7,
    "water operations": 8,
    "wastewater": 8,
    "manufacturing": 5,
    "plant experience": 6,
    "operations": 4,

    # Education/background fit
    "bachelor": 5,
    "accounting degree": 6,
    "finance degree": 6,
    "business degree": 6,
    "related field": 4,
}


LOCATION_RULES = {
    # Strong NC / Triangle / nearby fit
    "raleigh": 18,
    "durham": 16,
    "cary": 16,
    "morrisville": 16,
    "research triangle": 16,
    "triangle": 14,
    "rtp": 14,
    "apex": 14,
    "garner": 14,
    "clayton": 16,
    "smithfield": 16,
    "selma": 14,
    "benson": 12,
    "goldsboro": 14,
    "wilson": 12,
    "kinston": 12,
    "greenville": 10,
    "rocky mount": 10,
    "fayetteville": 8,
    "wake county": 16,
    "johnston county": 16,
    "wayne county": 14,
    "north carolina": 12,
    "nc": 12,

    # Acceptable but not ideal
    "charlotte": 6,
    "greensboro": 6,
    "winston-salem": 6,
    "wilmington": 6,
    "new bern": 6,
    "jacksonville": 5,
}


WORK_STYLE_RULES = {
    "hybrid": 14,
    "remote": 12,
    "work from home": 12,
    "wfh": 10,
    "telework": 10,
    "flexible": 5,
}


SENIORITY_POSITIVE_RULES = {
    "entry level": 12,
    "entry-level": 12,
    "junior": 10,
    "trainee": 10,
    "associate": 8,
    "assistant": 7,
    "coordinator": 6,
    "staff": 7,
    "analyst": 8,
    "specialist": 5,
}


SENIORITY_PENALTY_RULES = {
    "senior manager": -45,
    "sr. manager": -45,
    "senior director": -50,
    "director": -45,
    "vice president": -55,
    "vp": -55,
    "chief": -55,
    "executive": -50,
    "partner": -50,
    "principal": -40,
    "controller": -35,

    # Manager is not always impossible, but usually too high for this project.
    "manager": -25,

    # These are only mild penalties because some supervisor roles are realistic.
    "senior analyst": -8,
    "senior accountant": -8,
    "senior specialist": -12,
    "senior supervisor": -12,
}


DISQUALIFYING_OR_BAD_FIT_TITLE_RULES = {
    "software engineer": -45,
    "software developer": -45,
    "data engineer": -40,
    "machine learning engineer": -45,
    "data scientist": -35,
    "registered nurse": -45,
    " rn ": -45,
    "physician": -45,
    "therapist": -35,
    "pharmacist": -45,
    "teacher": -35,
    "professor": -35,
    "driver": -35,
    "warehouse associate": -35,
    "retail associate": -35,
    "food service": -35,
    "security officer": -35,
    "forklift operator": -35,
    "maintenance mechanic": -35,
}


REQUIREMENT_PENALTY_RULES = {
    "cpa required": -30,
    "active cpa": -30,
    "cpa license required": -35,
    "must have cpa": -35,
    "mba required": -25,
    "master's required": -25,
    "big 4 required": -25,
    "public accounting experience required": -18,
    "manager experience required": -20,
    "supervisory experience required": -15,
    "management experience": -18,
    "people management": -18,
    "travel 80%": -20,
}


REQUIREMENT_POSITIVE_RULES = {
    "cpa preferred": 3,
    "mba preferred": 2,
    "public accounting preferred": 3,
    "excel preferred": 4,
    "sql preferred": 4,
    "power bi preferred": 4,
}


EXPERIENCE_PATTERNS = [
    (r"\b0\s*[-to]+\s*2\s+years\b", 10, "Experience fit: 0-2 years"),
    (r"\b1\s*[-to]+\s*2\s+years\b", 10, "Experience fit: 1-2 years"),
    (r"\b1\s*[-to]+\s*3\s+years\b", 9, "Experience fit: 1-3 years"),
    (r"\b2\s*[-to]+\s*4\s+years\b", 7, "Experience fit: 2-4 years"),
    (r"\b2\s*[-to]+\s*5\s+years\b", 3, "Experience fit: 2-5 years"),
    (r"\b3\s*[-to]+\s*5\s+years\b", -5, "Experience stretch: 3-5 years"),
    (r"\b5\+?\s+years\b", -25, "Experience penalty: 5+ years"),
    (r"\b5 or more years\b", -25, "Experience penalty: 5+ years"),
    (r"\b7\+?\s+years\b", -35, "Experience penalty: 7+ years"),
    (r"\b10\+?\s+years\b", -45, "Experience penalty: 10+ years"),
    (r"\bminimum of 5 years\b", -25, "Experience penalty: minimum 5 years"),
    (r"\bminimum of 7 years\b", -35, "Experience penalty: minimum 7 years"),
    (r"\bminimum of 10 years\b", -45, "Experience penalty: minimum 10 years"),
]


REMOTE_WORDS = [
    "remote",
    "work from home",
    "wfh",
    "telework",
]


EXCLUDE_UNLESS_REMOTE_LOCATIONS = [
    "california",
    "new york",
    "new jersey",
    "massachusetts",
    "washington",
    "oregon",
    "colorado",
    "texas",
    "florida",
    "illinois",
    "georgia",
    "virginia",
    "maryland",
    "pennsylvania",
    "ohio",
    "arizona",
]


def clean_text(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def contains_phrase(text, phrase):
    phrase = clean_text(phrase)

    if not phrase:
        return False

    return phrase in text


def clamp_score(score):
    return max(0, min(100, score))


def apply_phrase_rules(text, rules, notes, label):
    score_change = 0

    for phrase, points in rules.items():
        if contains_phrase(text, phrase):
            score_change += points

            if points > 0:
                notes.append(f"+{points}: {label} matched '{phrase}'")
            else:
                notes.append(f"{points}: {label} matched '{phrase}'")

    return score_change


def apply_experience_rules(text, notes):
    score_change = 0

    for pattern, points, reason in EXPERIENCE_PATTERNS:
        if re.search(pattern, text):
            score_change += points

            if points > 0:
                notes.append(f"+{points}: {reason}")
            else:
                notes.append(f"{points}: {reason}")

    return score_change


def is_remote_or_hybrid(text):
    return "hybrid" in text or any(remote_word in text for remote_word in REMOTE_WORDS)


def apply_out_of_state_location_penalty(location, combined_text, notes):
    if is_remote_or_hybrid(combined_text):
        return 0

    for location_phrase in EXCLUDE_UNLESS_REMOTE_LOCATIONS:
        if contains_phrase(location, location_phrase):
            notes.append(
                f"-20: Location penalty matched '{location_phrase}' without remote/hybrid wording"
            )
            return -20

    return 0


def get_score_band(score):
    if score >= 80:
        return "Strong match"
    if score >= 60:
        return "Possible match"
    if score >= 40:
        return "Weak/stretch match"

    return "Low match / likely skip"


def score_job(job):
    """
    Scores one job from 0 to 100.

    Expected job fields:
    - title
    - location
    - department
    - description, if available

    Return shape must stay stable because email and Excel code may depend on it:
    {
        "match_score": int,
        "match_notes": str,
    }
    """

    title = clean_text(job.get("title"))
    location = clean_text(job.get("location"))
    department = clean_text(job.get("department"))
    description = clean_text(job.get("description"))

    combined_text = " ".join([title, location, department, description])

    score = BASE_SCORE
    notes = [f"+{BASE_SCORE}: Base score"]

    score += apply_phrase_rules(
        text=title,
        rules=TITLE_RULES,
        notes=notes,
        label="Title",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=KEYWORD_RULES,
        notes=notes,
        label="Keyword/background",
    )

    score += apply_phrase_rules(
        text=location,
        rules=LOCATION_RULES,
        notes=notes,
        label="Location",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=WORK_STYLE_RULES,
        notes=notes,
        label="Remote/hybrid/work style",
    )

    score += apply_phrase_rules(
        text=title,
        rules=SENIORITY_POSITIVE_RULES,
        notes=notes,
        label="Seniority fit",
    )

    score += apply_phrase_rules(
        text=title,
        rules=SENIORITY_PENALTY_RULES,
        notes=notes,
        label="Seniority penalty",
    )

    score += apply_phrase_rules(
        text=title,
        rules=DISQUALIFYING_OR_BAD_FIT_TITLE_RULES,
        notes=notes,
        label="Bad-fit title penalty",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=REQUIREMENT_PENALTY_RULES,
        notes=notes,
        label="Requirement penalty",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=REQUIREMENT_POSITIVE_RULES,
        notes=notes,
        label="Requirement positive",
    )

    score += apply_experience_rules(combined_text, notes)

    score += apply_out_of_state_location_penalty(
        location=location,
        combined_text=combined_text,
        notes=notes,
    )

    final_score = clamp_score(score)
    score_band = get_score_band(final_score)

    notes.append(score_band)

    return {
        "match_score": final_score,
        "match_notes": "; ".join(notes),
    }