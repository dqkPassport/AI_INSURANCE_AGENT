class SafeDict(dict):
    def __missing__(self, key: str):
        # If a placeholder is missing, keep it visible instead of crashing
        return "{" + key + "}"


def render_template(body: str, context: dict) -> str:
    """
    Render template using Python str.format_map safely.
    Missing keys won't crash.
    """
    return body.format_map(SafeDict(context))
