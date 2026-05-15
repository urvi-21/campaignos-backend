from app.agents.retrieval.trend_retrieval import (
    retrieve_trends
)

from app.agents.retrieval.competitor_retrieval import (
    retrieve_competitors
)

from app.agents.retrieval.social_retrieval import (
    retrieve_social_signals
)

from app.agents.retrieval.creator_retrieval import (
    retrieve_creator_patterns
)

from app.agents.retrieval.reddit_retrieval import (
    retrieve_reddit_signals
)

from app.agents.retrieval.instagram_retrieval import (
    retrieve_instagram_signals
)

from app.services.query_planner_service import (
    generate_retrieval_queries
)

import os


# =========================================================
# SAFE RETRIEVAL
# =========================================================

def safe_retrieval(source_name, retrieval_function, *args):

    live_retrieval_enabled = (
        os.getenv("CAMPAIGNOS_ENABLE_LIVE_RETRIEVAL", "").lower()
        in {"1", "true", "yes"}
    )

    required_key = (
        "APIFY_API_TOKEN"
        if source_name == "instagram_intelligence"
        else "TAVILY_API_KEY"
    )

    print(f"\n=== RETRIEVAL: {source_name} ===")

    if not live_retrieval_enabled:

        print("LIVE RETRIEVAL DISABLED")

        return {
            "status": "skipped",
            "source": source_name,
            "error": "Live retrieval disabled",
            "data": []
        }

    if not os.getenv(required_key):

        print(f"MISSING KEY: {required_key}")

        return {
            "status": "skipped",
            "source": source_name,
            "error": f"{required_key} missing",
            "data": []
        }

    try:

        result = retrieval_function(*args)

        if not result:
            result = []

        print(f"SUCCESS: {len(result)} results")

        return {
            "status": "success",
            "source": source_name,
            "data": result
        }

    except Exception as e:

        print(f"FAILED: {str(e)}")

        return {
            "status": "failed",
            "source": source_name,
            "error": str(e),
            "data": []
        }


# =========================================================
# MAIN ORCHESTRATION FUNCTION
# =========================================================

def orchestrate_retrieval(data):

    print("\n===================================")
    print("STARTING RETRIEVAL PIPELINE")
    print("===================================\n")

    retrieval_queries = generate_retrieval_queries(data)

    trend_data = safe_retrieval(
        "trend_intelligence",
        retrieve_trends,
        data.product,
        data.audience
    )

    competitor_data = safe_retrieval(
        "competitor_intelligence",
        retrieve_competitors,
        data.product
    )

    social_data = safe_retrieval(
        "social_intelligence",
        retrieve_social_signals,
        data.product,
        data.audience
    )

    creator_data = safe_retrieval(
        "creator_intelligence",
        retrieve_creator_patterns,
        data.product
    )

    reddit_data = safe_retrieval(
        "reddit_intelligence",
        retrieve_reddit_signals,
        data.product,
        data.audience
    )

    instagram_data = safe_retrieval(
        "instagram_intelligence",
        retrieve_instagram_signals,
        data.product
    )

    successful_sources = len([
        source for source in [
            trend_data,
            competitor_data,
            social_data,
            creator_data,
            reddit_data,
            instagram_data
        ]
        if source["status"] == "success"
    ])

    print(f"\nSUCCESSFUL SOURCES: {successful_sources}")

    return {

        "retrieval_queries": retrieval_queries,

        "sources": {

            "trend_intelligence": trend_data,

            "competitor_intelligence": competitor_data,

            "social_intelligence": social_data,

            "creator_intelligence": creator_data,

            "reddit_intelligence": reddit_data,

            "instagram_intelligence": instagram_data
        },

        "retrieval_summary": {

            "sources_attempted": 6,

            "sources_successful": successful_sources
        }
    }