from groq import Groq
from dotenv import load_dotenv
import os

from app.utils.json_utils import safe_json_parse
from app.services.workflow_analysis_service import (
    analyze_campaign_complexity,
    analyze_operational_risk
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _fallback_workflow(data, complexity="simple", risk_level="low", error=None):

    fallback = {
        "workflow_phases": [
            {
                "phase": "Campaign foundation",
                "objective": "Align narrative, platforms, creators, and launch requirements.",
                "key_actions": [
                    "Confirm final brief and success criteria.",
                    "Map creator roles to selected platforms.",
                    "Prepare approval and publishing checkpoints."
                ]
            },
            {
                "phase": "Creator execution",
                "objective": "Produce and review creator content against campaign strategy.",
                "key_actions": [
                    "Send creator briefs with hook examples.",
                    "Review drafts for claims, fit, and platform-native execution.",
                    "Lock publishing windows and asset handoffs."
                ]
            },
            {
                "phase": "Launch and optimization",
                "objective": "Publish, monitor signals, and amplify the strongest content.",
                "key_actions": [
                    "Track early engagement and comments.",
                    "Promote strongest hooks across active platforms.",
                    "Capture learnings for strategic memory."
                ]
            }
        ],
        "approval_chain": [
            "Campaign strategy approval",
            "Creator brief approval",
            "Content draft approval",
            "Final publishing approval"
        ],
        "operational_dependencies": [
            "Final campaign narrative",
            "Creator availability",
            "Platform posting schedule",
            "Review turnaround time"
        ],
        "publishing_coordination": [
            f"Coordinate launch across {', '.join(data.platforms) or 'selected platforms'}.",
            "Sequence proof-led content after initial narrative framing."
        ],
        "execution_bottlenecks": [
            "Slow creative approvals",
            "Creator revisions arriving close to launch",
            "Unclear ownership of platform-specific edits"
        ],
        "risk_alerts": [
            f"Operational risk level: {risk_level}",
            f"Campaign complexity: {complexity}"
        ],
        "service_status": {
            "source": "groq",
            "status": "fallback"
        }
    }

    if error:
        fallback["service_status"]["error"] = str(error)

    return fallback


def generate_workflow(data, strategy, creators):

    complexity = analyze_campaign_complexity(data)
    risk_level = analyze_operational_risk(data)

    if not os.getenv("GROQ_API_KEY"):
        return _fallback_workflow(
            data,
            complexity,
            risk_level,
            "GROQ_API_KEY is not configured"
        )

    prompt = f"""
    You are a senior campaign operations director
    specializing in creator marketing execution systems.

    Your job is to generate REALISTIC operational workflows.

    DO NOT generate generic task lists.

    Instead:
    think like a real campaign operations team.

    Reason about:
    - creator coordination
    - operational sequencing
    - approval bottlenecks
    - publishing synchronization
    - execution dependencies
    - campaign risks
    - platform-native rollout logic

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

    Campaign Complexity:
    {complexity}

    Operational Risk Level:
    {risk_level}

    Strategic Context:
    {strategy}

    Creator Intelligence:
    {creators}

    Return ONLY valid JSON in this exact structure:

    {{
      "workflow_phases": [
        {{
          "phase": "string",
          "objective": "string",
          "key_actions": [
            "string"
          ]
        }}
      ],
      "approval_chain": [
        "string"
      ],
      "operational_dependencies": [
        "string"
      ],
      "publishing_coordination": [
        "string"
      ],
      "execution_bottlenecks": [
        "string"
      ],
      "risk_alerts": [
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
                        "You are an elite campaign operations strategist "
                        "specialized in operational workflow orchestration "
                        "for creator marketing campaigns."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.25,
            max_tokens=1600
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(
            content,
            _fallback_workflow(data, complexity, risk_level)
        )

        if isinstance(parsed, dict):
            parsed.setdefault(
                "service_status",
                {
                    "source": "groq",
                    "status": "success"
                }
            )

        return parsed

    except Exception as e:
        return _fallback_workflow(data, complexity, risk_level, e)
