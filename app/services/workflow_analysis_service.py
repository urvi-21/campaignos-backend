def analyze_campaign_complexity(data):

    complexity_score = 0

    # PLATFORM COMPLEXITY
    complexity_score += len(data.platforms) * 10

    # GOAL COMPLEXITY
    complexity_score += len(data.goals) * 15

    # BUDGET COMPLEXITY
    budget = data.budget.lower()

    if "100000" in budget or "500000" in budget:
        complexity_score += 30

    elif "50000" in budget:
        complexity_score += 20

    # ENTERPRISE / COMPLIANCE SIGNALS
    sensitive_keywords = [
        "healthcare",
        "finance",
        "medical",
        "pharma"
    ]

    audience_text = data.audience.lower()
    product_text = data.product.lower()

    for keyword in sensitive_keywords:

        if keyword in audience_text or keyword in product_text:
            complexity_score += 40

    # FINAL CLASSIFICATION
    if complexity_score >= 80:
        return "enterprise"

    elif complexity_score >= 40:
        return "medium"

    return "simple"

def analyze_operational_risk(data):

    risk_score = 0

    sensitive_keywords = [
        "medical",
        "finance",
        "healthcare",
        "investment",
        "children"
    ]

    product_text = data.product.lower()

    for keyword in sensitive_keywords:

        if keyword in product_text:
            risk_score += 30

    if len(data.platforms) >= 3:
        risk_score += 20

    if len(data.goals) >= 3:
        risk_score += 20

    if risk_score >= 60:
        return "high"

    elif risk_score >= 30:
        return "moderate"

    return "low"