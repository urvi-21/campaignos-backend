from pydantic import BaseModel
from typing import List


class CampaignInput(BaseModel):

    brand: str
    product: str
    audience: str

    budget: str = ""

    platforms: List[str] = []

    goals: List[str] = []

class ResearchInsights(BaseModel):
    trend_signals: List[str]
    audience_insights: List[str]
    competitor_patterns: List[str]
    content_opportunities: List[str]

class StrategyBrief(BaseModel):
    campaign_narrative: str
    content_pillars: List[str]
    hooks: List[str]
    rollout_strategy: List[str]

class CreatorRecommendation(BaseModel):
    creator_name: str
    fit_score: int
    reasoning: str
    strategic_role: str

class WorkflowPlan(BaseModel):
    phases: List[str]
    deliverables: List[str]
    approvals: List[str]
    dependencies: List[str]
    risk_alerts: List[str]