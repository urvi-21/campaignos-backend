import json
import re

def safe_json_parse(content, fallback=None):

    if fallback is None:
        fallback = {}

    try:
        return json.loads(content)

    except Exception:

        try:
            cleaned = re.sub(
                r"```json|```",
                "",
                content
            ).strip()

            return json.loads(cleaned)

        except Exception:
            return fallback