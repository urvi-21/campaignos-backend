from dotenv import load_dotenv
import os

from app.utils.mock_creators import mock_creators

from app.services.scoring_service import (
    calculate_audience_fit,
    calculate_style_match,
    calculate_engagement_quality,
    calculate_final_score
)

load_dotenv()


def generate_creator_matches(data, strategy):

    creator_results = []

    strategy_hooks = strategy.get("hooks", [])

    for creator in mock_creators:

        # =========================================================
        # STEP 1 — SCORING
        # =========================================================

        audience_score = calculate_audience_fit(
            data.audience,
            creator.get("audience", "")
        )

        style_score = calculate_style_match(
            strategy_hooks,
            creator.get("style", "")
        )

        engagement_score = calculate_engagement_quality(
            creator.get("engagement_rate", 0)
        )

        final_score = calculate_final_score(
            audience_score,
            style_score,
            engagement_score
        )

        # =========================================================
        # STEP 2 — STRATEGIC REASONING
        # =========================================================

        reasoning = []

        if audience_score >= 70:
            reasoning.append(
                "Strong audience alignment with campaign demographic."
            )

        if style_score >= 70:
            reasoning.append(
                "Creator storytelling style aligns with campaign narrative."
            )

        if engagement_score >= 80:
            reasoning.append(
                "High engagement quality indicates audience trust."
            )

        if not reasoning:
            reasoning.append(
                "Moderate strategic compatibility with campaign direction."
            )

        # =========================================================
        # STEP 3 — STRATEGIC ROLE
        # =========================================================

        strategic_role = "Lifestyle engagement creator"

        creator_style = creator.get(
            "style",
            ""
        ).lower()

        if "transformation" in creator_style:

            strategic_role = (
                "Authenticity-driven transformation creator"
            )

        elif "challenge" in creator_style:

            strategic_role = (
                "High-energy challenge campaign creator"
            )

        elif "educational" in creator_style:

            strategic_role = (
                "Educational authority creator"
            )

        elif "community" in creator_style:

            strategic_role = (
                "Community-driven engagement creator"
            )

        # =========================================================
        # STEP 4 — RESULT OBJECT
        # =========================================================

        creator_results.append({

            "creator_name": creator.get("name"),

            "fit_score": final_score,

            "audience_score": audience_score,

            "style_score": style_score,

            "engagement_score": engagement_score,

            "creator_style": creator.get("style"),

            "platform": creator.get("platform", "Instagram"),

            "followers": creator.get("followers", "N/A"),

            "brand_integration_style": creator.get(
                "brand_integration_style",
                "Natural creator integration"
            ),

            "audience_relationship": creator.get(
                "audience_relationship",
                "Strong audience relatability"
            ),

            "strategic_role": strategic_role,

            "reasoning": reasoning
        })

    # =========================================================
    # STEP 5 — SORT RESULTS
    # =========================================================

    creator_results = sorted(
        creator_results,
        key=lambda x: x["fit_score"],
        reverse=True
    )

    return {
        "recommended_creators": creator_results
    }