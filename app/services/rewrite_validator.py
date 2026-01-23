import re

DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")  # matches 2026-02-01
MONEY_RE = re.compile(r"\$\s?\d+(?:,\d{3})*(?:\.\d{1,2})?")  # $1450 or $1,450.00
NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")  # 1200, 20, 20.5


def extract_facts(text: str) -> set[str]:
    facts = set()
    facts.update(DATE_RE.findall(text))
    facts.update(MONEY_RE.findall(text))
    facts.update(NUMBER_RE.findall(text))
    return facts


def validate_no_fact_change(
    base_text: str, rewritten_text: str
) -> tuple[bool, str | None]:
    """
    Simple guardrail: rewritten must contain all extracted facts from base.
    If not, fail validation.
    """
    base_facts = extract_facts(base_text)
    rewritten_facts = extract_facts(rewritten_text)

    missing = sorted(list(base_facts - rewritten_facts))
    if missing:
        return False, f"Rewrite missing facts: {missing[:10]}"  # keep message short
    return True, None
