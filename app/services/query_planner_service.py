from groq import Groq
from dotenv import load_dotenv
import os

from app.utils.json_utils import safe_json_parse

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _fallback_queries(data, error=None):

    product_audience = f"{data.product} {data.audience}".strip()

    fallback = {
        "trend_queries": [
            f"{product_audience} social media trends"
        ],
        "audience_queries": [
            f"{product_audience} audience frustrations motivators"
        ],
        "competitor_queries": [
            f"{data.product} competitor campaigns positioning"
        ],
        "creator_queries": [
            f"{data.product} creator marketing examples"
        ],
        "viral_queries": [
            f"{data.product} viral content hooks"
        ],
        "service_status": {
            "source": "groq",
            "status": "fallback"
        }
    }

    if error:
        fallback["service_status"]["error"] = str(error)

    return fallback


def generate_retrieval_queries(data):

    if not os.getenv("GROQ_API_KEY"):
        return _fallback_queries(data, "GROQ_API_KEY is not configured")

    prompt = f"""
    You are an elite campaign intelligence planner.

    Campaign Information:

    Brand:
    {data.brand}

    Product:
    {data.product}

    Audience:
    {data.audience}

    Platforms:
    {", ".join(data.platforms)}

    Goals:
    {", ".join(data.goals)}

    Generate retrieval queries for:
    - trends
    - audience psychology
    - competitors
    - creators
    - viral content

    Return ONLY valid JSON:

    {{
      "trend_queries": [],
      "audience_queries": [],
      "competitor_queries": [],
      "creator_queries": [],
      "viral_queries": []
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
                        "You are an elite campaign intelligence planner."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()

    except Exception as e:
        return _fallback_queries(data, e)

    fallback = _fallback_queries(data)

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
