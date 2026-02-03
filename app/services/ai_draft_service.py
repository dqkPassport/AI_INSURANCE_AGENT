from __future__ import annotations

from app.schemas.ai_draft import Channel, RenewalFacts, Tone


def _money(v: float) -> str:
    return f"${v:,.2f}"


def _build_sms(f: RenewalFacts, tone: Tone) -> str:
    exp = f.expiration_date.strftime("%b %d, %Y")

    if tone == "friendly":
        return (
            f"Hi {f.customer_name}! Quick heads-up: your {f.product_type} policy "
            f"({f.policy_number}) with {f.carrier} expires on {exp}. "
            f"Renewal premium is {_money(f.renewal_premium)}. Want me to renew it for you?"
        )

    if tone == "neutral":
        return (
            f"{f.customer_name}, your {f.product_type} policy ({f.policy_number}) with {f.carrier} "
            f"expires on {exp}. Renewal premium: {_money(f.renewal_premium)}. "
            f"Reply YES to renew or ask any questions."
        )

    if tone == "super_friendly":
        return (
            f"Hi {f.customer_name}! 😊 Quick heads-up: your {f.product_type} policy "
            f"({f.policy_number}) with {f.carrier} expires on {exp}. "
            f"Renewal premium is {_money(f.renewal_premium)}. Want me to renew it for you?\n"
            f"Thanks so much — I’m here if you need anything!"
        )

    # urgent
    return (
        f"Important: {f.customer_name}, your {f.product_type} policy ({f.policy_number}) with {f.carrier} "
        f"expires on {exp}. Renewal premium: {_money(f.renewal_premium)}. "
        f"Please reply today so we can keep coverage active."
    )


def _build_email(f: RenewalFacts, tone: Tone) -> str:
    exp = f.expiration_date.strftime("%B %d, %Y")
    old_p = _money(f.old_premium)
    new_p = _money(f.renewal_premium)

    subject = f"Renewal reminder: {f.product_type} policy {f.policy_number}"
    greeting = f"Hi {f.customer_name},"

    if tone == "friendly":
        body = (
            f"{greeting}\n\n"
            f"Just a friendly reminder that your {f.product_type} policy ({f.policy_number}) with {f.carrier} "
            f"is set to expire on {exp}.\n\n"
            f"Your current premium is {old_p}, and the renewal premium is {new_p}.\n\n"
            f"If you'd like, I can take care of the renewal for you—just reply to this email.\n\n"
            f"Thank you!"
        )
    elif tone == "neutral":
        body = (
            f"{greeting}\n\n"
            f"Your {f.product_type} policy ({f.policy_number}) with {f.carrier} expires on {exp}.\n\n"
            f"Current premium: {old_p}\n"
            f"Renewal premium: {new_p}\n\n"
            f"Please reply to confirm renewal or ask questions.\n"
        )
    else:  # urgent
        body = (
            f"{greeting}\n\n"
            f"Your {f.product_type} policy ({f.policy_number}) with {f.carrier} will expire on {exp}.\n\n"
            f"Current premium: {old_p}\n"
            f"Renewal premium: {new_p}\n\n"
            f"To avoid a lapse in coverage, please confirm renewal as soon as possible.\n"
        )

    return f"Subject: {subject}\n\n{body}"


def validate_contains_key_facts(text: str, f: RenewalFacts) -> None:
    """
    Strict guardrail: ensure key facts are present in the final draft.
    If something is missing, we raise ValueError so API returns 422.
    """
    required = [
        f.customer_name,
        f.policy_number,
        f.carrier,
        f.expiration_date.strftime("%Y"),  # at least the year appears
        f"{f.renewal_premium:,.2f}".rstrip("0").rstrip("."),
    ]
    missing = [x for x in required if x and x not in text]
    if missing:
        raise ValueError(f"Draft missing required facts: {missing}")


def draft_renewal_message(
    facts: RenewalFacts, tone: Tone, channel: Channel, strict: bool
) -> str:
    if channel == "sms":
        text = _build_sms(facts, tone)
    else:
        text = _build_email(facts, tone)

    if strict:
        validate_contains_key_facts(text, facts)

    return text
