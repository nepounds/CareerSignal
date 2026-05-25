import re


POSITIVE_TITLE_RULES = {
    "accounting": 18,
    "accountant": 18,
    "staff accountant": 25,
    "finance": 16,
    "financial analyst": 24,
    "analyst": 18,
    "audit": 16,
    "tax": 16,
    "associate": 12,
    "entry level": 15,
    "entry-level": 15,
    "junior": 12,
    "rotational": 10,
    "development program": 10,
    "apprentice": 8,
    "intern": 6,
}

POSITIVE_KEYWORD_RULES = {
    "excel": 5,
    "power bi": 5,
    "sql": 5,
    "python": 4,
    "data": 4,
    "reporting": 5,
    "reconciliation": 6,
    "accounts payable": 6,
    "accounts receivable": 6,
    "general ledger": 8,
    "journal entries": 8,
    "financial statements": 8,
    "month end": 7,
    "month-end": 7,
    "gaap": 6,
}

LOCATION_RULES = {
    "raleigh": 15,
    "durham": 12,
    "cary": 12,
    "morrisville": 12,
    "research triangle": 12,
    "rtp": 12,
    "clayton": 10,
    "smithfield": 10,
    "garner": 10,
    "knightdale": 10,
    "wake forest": 10,
    "chapel hill": 8,
    "goldsboro": 8,
    "wilson": 8,
    "greenville": 6,
    "north carolina": 8,
    "nc": 8,
}

WORK_STYLE_RULES = {
    "hybrid": 14,
    "remote": 12,
    "work from home": 12,
    "wfh": 10,
    "flexible": 5,
}

NEGATIVE_TITLE_RULES = {
    "senior manager": -40,
    "sr. manager": -40,
    "manager": -28,
    "director": -45,
    "vice president": -50,
    "vp": -50,
    "principal": -30,
    "controller": -35,
    "chief": -50,
    "head of": -40,
}

NEGATIVE_REQUIREMENT_RULES = {
    "cpa required": -30,
    "active cpa": -30,
    "cpa license required": -35,
    "must have cpa": -35,
    "public accounting experience required": -18,
    "supervisory experience": -18,
    "management experience": -20,
    "people management": -20,
}

EXPERIENCE_PATTERNS = [
    (r"([5-9]|\d{2,})\+?\s+years", -30, "Requires 5+ years of experience"),
    (r"([3-4])\+?\s+years", -12, "Requires 3-4 years of experience"),
    (r"minimum of ([5-9]|\d{2,}) years", -30, "Requires 5+ years of experience"),
    (r"minimum of ([3-4]) years", -12, "Requires 3-4 years of experience"),
]


def clean_text(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def contains_phrase(text, phrase):
    return phrase in text


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


def apply_experience_penalties(text, notes):
    score_change = 0

    for pattern, points, reason in EXPERIENCE_PATTERNS:
        if re.search(pattern, text):
            score_change += points
            notes.append(f"{points}: {reason}")

    return score_change


def clamp_score(score):
    return max(0, min(100, score))


def score_job(job):
    """
    Scores one job from 0 to 100.

    Expected job fields:
    - title
    - location
    - department
    - description, if available
    """

    title = clean_text(job.get("title"))
    location = clean_text(job.get("location"))
    department = clean_text(job.get("department"))
    description = clean_text(job.get("description"))

    combined_text = " ".join([title, location, department, description])

    score = 35
    notes = []

    notes.append("+35: Base score")

    score += apply_phrase_rules(
        text=title,
        rules=POSITIVE_TITLE_RULES,
        notes=notes,
        label="Title",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=POSITIVE_KEYWORD_RULES,
        notes=notes,
        label="Keyword",
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
        label="Work style",
    )

    score += apply_phrase_rules(
        text=title,
        rules=NEGATIVE_TITLE_RULES,
        notes=notes,
        label="Seniority penalty",
    )

    score += apply_phrase_rules(
        text=combined_text,
        rules=NEGATIVE_REQUIREMENT_RULES,
        notes=notes,
        label="Requirement penalty",
    )

    score += apply_experience_penalties(combined_text, notes)

    final_score = clamp_score(score)

    if final_score >= 80:
        notes.append("Strong match")
    elif final_score >= 60:
        notes.append("Possible match")
    elif final_score >= 40:
        notes.append("Weak match")
    else:
        notes.append("Poor match")

    return {
        "match_score": final_score,
        "match_notes": "; ".join(notes),
    }