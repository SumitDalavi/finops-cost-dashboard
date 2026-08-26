"""
Rightsizing and cost optimization recommendations.
Analyzes resource utilization and spend patterns to suggest savings.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Recommendation:
    resource_id: str
    resource_type: str
    current_cost: float
    projected_saving: float
    saving_pct: float
    action: str
    reason: str
    priority: str  # LOW | MEDIUM | HIGH


def analyze_ec2_utilization(instances: List[dict]) -> List[Recommendation]:
    """
    Generate EC2 rightsizing recommendations based on CPU/memory utilization.

    Args:
        instances: List of {id, type, avg_cpu_pct, avg_mem_pct, monthly_cost}
    """
    recs = []
    # Tier: oversized if avg CPU < 10% and avg mem < 20%
    for inst in instances:
        cpu = inst.get("avg_cpu_pct", 50)
        mem = inst.get("avg_mem_pct", 50)
        cost = inst.get("monthly_cost", 0)

        if cpu < 5 and mem < 10:
            # Extremely underutilised — downsize 2 instance sizes
            saving_pct = 0.60
            recs.append(Recommendation(
                resource_id=inst["id"], resource_type="EC2",
                current_cost=cost, projected_saving=round(cost * saving_pct, 2),
                saving_pct=saving_pct * 100,
                action=f"Downsize {inst['type']} by 2 sizes or switch to Graviton",
                reason=f"Avg CPU={cpu:.1f}%, Avg Mem={mem:.1f}% — severely underutilised",
                priority="HIGH",
            ))
        elif cpu < 15 and mem < 30:
            saving_pct = 0.35
            recs.append(Recommendation(
                resource_id=inst["id"], resource_type="EC2",
                current_cost=cost, projected_saving=round(cost * saving_pct, 2),
                saving_pct=saving_pct * 100,
                action=f"Downsize {inst['type']} by 1 size",
                reason=f"Avg CPU={cpu:.1f}%, Avg Mem={mem:.1f}% — underutilised",
                priority="MEDIUM",
            ))

    return recs


def analyze_idle_resources(resources: List[dict]) -> List[Recommendation]:
    """Identify idle resources (0 requests, 0 connections for 7+ days)."""
    recs = []
    for res in resources:
        if res.get("requests_7d", 1) == 0 and res.get("connections_7d", 1) == 0:
            cost = res.get("monthly_cost", 0)
            recs.append(Recommendation(
                resource_id=res["id"], resource_type=res.get("type", "unknown"),
                current_cost=cost, projected_saving=cost,
                saving_pct=100.0,
                action="Delete or schedule for termination",
                reason="Zero requests and connections in the last 7 days",
                priority="HIGH",
            ))
    return recs


def total_savings(recs: List[Recommendation]) -> float:
    return round(sum(r.projected_saving for r in recs), 2)
