from app.services.vector_memory_service import (
    store_campaign_memory
)


def store_strategic_learning(
    campaign_id,
    strategy,
    creators,
    workflow,
    behavioral_signals
):

    learning_text = f"""
    Campaign Narrative:
    {strategy.get("campaign_narrative")}

    Hooks:
    {strategy.get("hooks")}

    Content Pillars:
    {strategy.get("content_pillars")}

    Creator Insights:
    {creators}

    Workflow Insights:
    {workflow}

    Audience Emotions:
    {behavioral_signals.get("audience_emotions")}

    Narrative Patterns:
    {behavioral_signals.get("narrative_patterns")}
    """

    metadata = {
        "type": "strategic_learning"
    }

    return store_campaign_memory(
        campaign_id=f"{campaign_id}_strategic_learning",
        text=learning_text,
        metadata=metadata
    )
