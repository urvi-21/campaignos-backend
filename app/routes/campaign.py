from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.schemas.campaign import CampaignInput

from app.agents.retrieval.retrieval_orchestrator import (
    orchestrate_retrieval
)

from app.services.signal_extraction_service import (
    extract_signals
)

from app.services.strategy_service import (
    generate_strategy
)

from app.services.creator_service import (
    generate_creator_matches
)

from app.services.workflow_service import (
    generate_workflow
)

from app.services.vector_memory_service import (
    store_campaign_memory
)

from app.services.strategic_memory_service import (
    store_strategic_learning
)

from app.services.retrieval_cleaning_service import (
    clean_retrieval_results
)
router = APIRouter()


@router.post("/create-campaign")
def create_campaign(data: CampaignInput):

    try:
        warnings = []

        # =========================================================
        # STEP 1 — MULTI-SOURCE RETRIEVAL
        # =========================================================
        retrieval_data = orchestrate_retrieval(data)

        # =========================================================
        # STEP 2 — BEHAVIORAL SIGNAL EXTRACTION
        # =========================================================
        cleaned_retrieval = clean_retrieval_results(
           retrieval_data
        )

        extracted_signals = extract_signals(
            cleaned_retrieval
        )

        # =========================================================
        # STEP 3 — STRATEGY GENERATION
        # =========================================================
        strategy = generate_strategy(
            data,
            extracted_signals
        )

        # =========================================================
        # STEP 4 — CREATOR MATCHING
        # =========================================================
        creators = generate_creator_matches(
            data,
            strategy
        )

        # =========================================================
        # STEP 5 — WORKFLOW GENERATION
        # =========================================================
        workflow = generate_workflow(
            data,
            strategy,
            creators
        )

        # =========================================================
        # STEP 6 — STORE SEMANTIC MEMORY
        # =========================================================
        memory_result = store_campaign_memory(

            campaign_id=f"{data.brand}_{data.product}",

            text=f"""
            Campaign Narrative:
            {strategy.get("campaign_narrative")}

            Content Pillars:
            {strategy.get("content_pillars")}

            Hooks:
            {strategy.get("hooks")}

            Creator Direction:
            {strategy.get("creator_direction")}
            """,

            metadata={
                "brand": data.brand,
                "product": data.product,
                "audience": data.audience,
                "platforms": ", ".join(data.platforms),
                "goals": ", ".join(data.goals)
            }
        )

        if memory_result.get("status") != "success":
            warnings.append({
                "service": "campaign_memory",
                "detail": memory_result
            })

        # =========================================================
        # STEP 7 — STORE STRATEGIC LEARNINGS
        # =========================================================
        strategic_memory_result = store_strategic_learning(

            campaign_id=f"{data.brand}_{data.product}",

            strategy=strategy,

            creators=creators,

            workflow=workflow,

            behavioral_signals=extracted_signals
        )

        if strategic_memory_result.get("status") != "success":
            warnings.append({
                "service": "strategic_memory",
                "detail": strategic_memory_result
            })

        # =========================================================
        # FINAL RESPONSE
        # =========================================================
        response_payload = {

            "status": "success" if not warnings else "degraded",

            "warnings": warnings,

            "campaign_input": {
                "brand": data.brand,
                "product": data.product,
                "audience": data.audience,
                "budget": data.budget,
                "platforms": data.platforms,
                "goals": data.goals
            },

            "retrieval_intelligence": retrieval_data,

            "behavioral_signals": extracted_signals,

            "strategy_brief": strategy,

            "creator_intelligence": creators,

            "workflow_operations": workflow
        }

        return jsonable_encoder(response_payload)

    except Exception as e:

        print("PIPELINE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "CampaignOS pipeline failed",
                "error": str(e)
            }
        )
