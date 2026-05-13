from groq import Groq
from app.schemas.campaign import CampaignInput
from dotenv import load_dotenv
import os

from app.utils.json_utils import safe_json_parse

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_research_insights(data: CampaignInput):

    prompt = f"""
    You are an elite AI campaign strategist.

    Analyze this campaign:

    Brand: {data.brand}
    Product: {data.product}
    Audience: {data.audience}
    Budget: {data.budget}
    Platforms: {", ".join(data.platforms)}
    Goals: {", ".join(data.goals)}

    Return ONLY valid JSON in this exact structure:

    {{
      "trend_signals": [],
      "audience_insights": [],
      "competitor_patterns": [],
      "content_opportunities": []
    }}

    IMPORTANT:
    - Return ONLY raw JSON
    - No markdown
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite campaign intelligence strategist."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5,

        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()

    fallback = {

        "trend_signals": [],

        "audience_insights": [],

        "competitor_patterns": [],

        "content_opportunities": []
    }

    return safe_json_parse(content, fallback)