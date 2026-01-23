from openai import OpenAI
from app.core.settings import settings


client = OpenAI(api_key=settings.openai_api_key)


def rewrite_message(*, text: str, tone: str, channel: str) -> str:
    """
    Rewrite a message in a chosen tone.
    Guardrails:
      - do NOT change numbers, dates, or names
      - do NOT invent facts
      - do NOT promise coverage
      - keep it short for sms
    """
    system_rules = (
        "You are an assistant for an insurance agency.\n"
        "Rules:\n"
        "1) Do NOT change any numbers, dollar amounts, dates, or policy numbers.\n"
        "2) Do NOT invent facts or coverage details.\n"
        "3) Do NOT promise coverage; ask the customer to confirm or let the agent review.\n"
        "4) Keep the same meaning.\n"
    )

    length_rule = (
        "Keep it under 320 characters."
        if channel == "sms"
        else "Keep it concise and professional."
    )

    prompt = (
        f"{system_rules}\n"
        f"Rewrite the message in '{tone}' tone. {length_rule}\n\n"
        f"Message:\n{text}"
    )

    response = client.responses.create(
        model="gpt-5.2",
        input=prompt,
    )

    return response.output_text
