from pydantic import BaseModel
from typing import List, Optional

class CostItem(BaseModel):
    resource_group: str
    service_name: str
    cost_usd: float
    currency: str = "USD"
    billing_period: str
    tags: dict = {}

class CostSummary(BaseModel):
    total_cost: float
    currency: str = "USD"
    period: str
    breakdown: List[CostItem]
    top_services: List[dict]

class RightsizingRecommendation(BaseModel):
    namespace: str
    pod_name: str
    container_name: str
    current_cpu_request: str
    current_memory_request: str
    avg_cpu_usage: str
    avg_memory_usage: str
    recommended_cpu: str
    recommended_memory: str
    estimated_savings_pct: float
