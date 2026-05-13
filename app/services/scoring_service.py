def calculate_audience_fit(campaign_audience, creator_audience):

    score = 0

    campaign_text = campaign_audience.lower()
    creator_text = creator_audience.lower()

    keywords = [
        "fitness",
        "wellness",
        "health",
        "running",
        "gen z",
        "millennials",
        "women",
        "men"
    ]

    for keyword in keywords:

        if keyword in campaign_text and keyword in creator_text:
            score += 15

    return min(score, 100)

def calculate_style_match(strategy_hooks, creator_style):

    score = 0

    creator_style = creator_style.lower()

    for hook in strategy_hooks:

        hook = hook.lower()

        if "challenge" in hook and "challenge" in creator_style:
            score += 25

        if "story" in hook and "storytelling" in creator_style:
            score += 25

        if "educational" in hook and "educational" in creator_style:
            score += 25

    return min(score, 100)

def calculate_engagement_quality(engagement_rate):

    if engagement_rate >= 8:
        return 95

    elif engagement_rate >= 6:
        return 80

    elif engagement_rate >= 4:
        return 65

    return 40

def calculate_final_score(
    audience_score,
    style_score,
    engagement_score
):

    final_score = (
        audience_score * 0.4 +
        style_score * 0.3 +
        engagement_score * 0.3
    )

    return round(final_score)