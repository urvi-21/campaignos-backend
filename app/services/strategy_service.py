from groq import Groq
from dotenv import load_dotenv
import os

from app.utils.json_utils import safe_json_parse
from app.services.vector_memory_service import (
    retrieve_similar_campaigns
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _fallback_strategy(data, signals=None, error=None):

    signals = signals or {}

    fallback = {
        "campaign_narrative": (
            f"Position {data.product} around the clearest audience tension "
            f"for {data.audience}, then support it with platform-native proof."
        ),
        "strategic_reasoning": [
            "Generated from local fallback logic because strategy LLM generation was unavailable."
        ],
        "content_pillars": [
            "Audience problem",
            "Product proof",
            "Creator-led demonstration",
            "Community validation"
        ],
        "hooks": [
            f"POV: {data.product} solves the problem everyone keeps ignoring",
            f"What {data.audience} should know before choosing {data.product}",
            "The simple shift that changes the whole routine"
        ],
        "creator_direction": [
            "Use creators who can demonstrate the product in a credible daily-use context.",
            "Prioritize honest explanation, visible proof, and audience-specific language."
        ],
        "rollout_strategy": [
            "Open with audience tension and problem framing.",
            "Follow with creator demonstrations and proof.",
            "Amplify high-performing hooks across selected platforms."
        ],
        "service_status": {
            "source": "groq",
            "status": "fallback"
        }
    }

    if signals.get("audience_frustrations"):
        fallback["strategic_reasoning"].append(
            f"Audience friction detected: {signals.get('audience_frustrations')}"
        )

    if error:
        fallback["service_status"]["error"] = str(error)

    return fallback


def generate_strategy(data, signals):

    memory_results = retrieve_similar_campaigns(
        query=f"{data.product} {data.audience}"
    )

    historical_context = memory_results.get(
        "documents",
        []
    )

    if not os.getenv("GROQ_API_KEY"):
        return _fallback_strategy(
            data,
            signals,
            "GROQ_API_KEY is not configured"
        )

    prompt = f"""
    You are a senior campaign strategist at a top creator marketing agency.

    Your job is to generate HIGH-QUALITY,
    evidence-grounded campaign strategy.

    DO NOT generate generic marketing advice.

    Every strategic recommendation MUST:
    - connect to behavioral signals
    - reflect audience psychology
    - feel operationally realistic
    - feel platform-native
    - feel creator-native

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

    Behavioral Intelligence Signals:

    Audience Frustrations:
    {signals.get("audience_frustrations", [])}

    Emotional Motivators:
    {signals.get("emotional_motivators", [])}

    Trust Signals:
    {signals.get("trust_signals", [])}

    Narrative Tensions:
    {signals.get("narrative_tensions", [])}

    Viral Hook Patterns:
    {signals.get("viral_hook_patterns", [])}

    Creator Behavior Patterns:
    {signals.get("creator_behavior_patterns", [])}

    Engagement Psychology:
    {signals.get("engagement_psychology", [])}

    Historical Campaign Intelligence:
    {historical_context}

    IMPORTANT:

    Build strategy ONLY from:
    - behavioral intelligence signals
    - retrieved audience psychology
    - historical campaign memory
    - creator behavior patterns

    Avoid generic marketing advice.

    Your strategy should:
    - explain WHY specific narratives matter
    - align creator behavior with audience psychology
    - leverage observed engagement patterns
    - use emotionally resonant positioning
    - feel execution-aware
    - feel strategically differentiated

    Generate:

    1. Campaign Narrative
    2. Strategic Reasoning
    3. Content Pillars
    4. Platform-Native Hooks
    5. Creator Positioning Strategy
    6. Rollout Strategy

    Return ONLY valid JSON in this exact structure:

    {{
      "campaign_narrative": "string",

      "strategic_reasoning": [
        "string"
      ],

      "content_pillars": [
        "string"
      ],

      "hooks": [
        "string"
      ],

      "creator_direction": [
        "string"
      ],

      "rollout_strategy": [
        "string"
      ]
    }}

    IMPORTANT:
    - Return ONLY raw JSON
    - No markdown
    - No explanations
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite evidence-driven campaign strategist "
                        "specialized in creator marketing and audience psychology."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.25,
            max_tokens=1800
        )

        content = response.choices[0].message.content.strip()

        parsed_response = safe_json_parse(
            content,
            fallback=_fallback_strategy(data, signals)
        )

        if isinstance(parsed_response, dict):
            parsed_response.setdefault(
                "service_status",
                {
                    "source": "groq",
                    "status": "success"
                }
            )

        return parsed_response

    except Exception as e:
        return _fallback_strategy(data, signals, e)
