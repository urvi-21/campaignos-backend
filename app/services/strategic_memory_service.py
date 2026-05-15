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

    # =========================================================
    # SAFE SIGNAL EXTRACTION
    # =========================================================

    frustrations = behavioral_signals.get(
        "audience_frustrations",
        []
    )

    motivators = behavioral_signals.get(
        "emotional_motivators",
        []
    )

    trust_signals = behavioral_signals.get(
        "trust_signals",
        []
    )

    tensions = behavioral_signals.get(
        "narrative_tensions",
        []
    )

    creator_patterns = behavioral_signals.get(
        "creator_behavior_patterns",
        []
    )

    viral_hooks = behavioral_signals.get(
        "viral_hook_patterns",
        []
    )

    # =========================================================
    # LEARNING TEXT
    # =========================================================

    learning_text = f"""
    =====================================================
    CAMPAIGN STRATEGIC MEMORY
    =====================================================

    Campaign Narrative:
    {strategy.get("campaign_narrative")}

    =====================================================
    CONTENT PILLARS
    =====================================================

    {strategy.get("content_pillars")}

    =====================================================
    VIRAL HOOKS
    =====================================================

    {strategy.get("hooks")}

    =====================================================
    AUDIENCE FRUSTRATIONS
    =====================================================

    {frustrations}

    =====================================================
    EMOTIONAL MOTIVATORS
    =====================================================

    {motivators}

    =====================================================
    TRUST SIGNALS
    =====================================================

    {trust_signals}

    =====================================================
    NARRATIVE TENSIONS
    =====================================================

    {tensions}

    =====================================================
    CREATOR BEHAVIOR PATTERNS
    =====================================================

    {creator_patterns}

    =====================================================
    VIRAL CONTENT PATTERNS
    =====================================================

    {viral_hooks}

    =====================================================
    CREATOR INTELLIGENCE
    =====================================================

    {creators}

    =====================================================
    WORKFLOW INTELLIGENCE
    =====================================================

    {workflow}
    """

    # =========================================================
    # METADATA
    # =========================================================

    metadata = {
        "type": "strategic_learning",
        "memory_category": "campaign_intelligence"
    }

    # =========================================================
    # STORE MEMORY
    # =========================================================

    return store_campaign_memory(

        campaign_id=f"{campaign_id}_strategic_learning",

        text=learning_text,

        metadata=metadata
    )