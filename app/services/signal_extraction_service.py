from groq import Groq
from dotenv import load_dotenv
import os

from app.utils.json_utils import safe_json_parse
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _fallback_signals(error=None):

    fallback = {
        "audience_frustrations": [],
        "emotional_motivators": [],
        "trust_signals": [],
        "narrative_tensions": [],
        "viral_hook_patterns": [],
        "creator_behavior_patterns": [],
        "engagement_psychology": [],
        "service_status": {
            "source": "groq",
            "status": "fallback"
        }
    }

    if error:
        fallback["service_status"]["error"] = str(error)

    return fallback


def extract_signals(retrieved_data):

    if not os.getenv("GROQ_API_KEY"):
        return _fallback_signals("GROQ_API_KEY is not configured")

    prompt = f"""
You are an elite behavioral intelligence analyst.

Your job is to extract HIGH-VALUE operational intelligence
from campaign retrieval evidence.

Focus on:

1. Audience frustrations
2. Emotional motivators
3. Trust signals
4. Narrative tensions
5. Viral hook structures
6. Creator behavior patterns
7. Engagement psychology

IMPORTANT:
Avoid generic observations.

Retrieved Intelligence:
{retrieved_data}

Return ONLY valid JSON in this exact structure:

{{
  "audience_frustrations": [],
  "emotional_motivators": [],
  "trust_signals": [],
  "narrative_tensions": [],
  "viral_hook_patterns": [],
  "creator_behavior_patterns": [],
  "engagement_psychology": []
}}

IMPORTANT:
- Return ONLY raw JSON
- No markdown
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite behavioral intelligence analyst."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1500
        )

        content = response.choices[0].message.content.strip()

    except Exception as e:
        return _fallback_signals(e)

    # =========================================================
    # CLEAN MARKDOWN WRAPPERS
    # =========================================================

    if content.startswith("```json"):
        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    elif content.startswith("```"):
        content = content.replace(
            "```",
            ""
        ).strip()

    # =========================================================
    # FALLBACK RESPONSE
    # =========================================================

    fallback = _fallback_signals()

    parsed = safe_json_parse(content, fallback)

    if isinstance(parsed, dict):
        parsed.setdefault(
            "service_status",
            {
                "source": "groq",
                "status": "success"
            }
        )

    return parsed
