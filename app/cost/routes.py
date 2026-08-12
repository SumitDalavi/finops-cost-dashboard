from fastapi import APIRouter
from .azure_client import get_monthly_costs

router = APIRouter()

@router.get("/monthly")
def monthly_costs(period: str = "2026-08"):
    return get_monthly_costs(period=period)

@router.get("/by-environment")
def costs_by_environment(period: str = "2026-08"):
    costs = get_monthly_costs(period=period)
    env_totals: dict = {}
    for item in costs.breakdown:
        env = item.tags.get("env", "untagged")
        env_totals[env] = env_totals.get(env, 0) + item.cost_usd
    return {"period": period, "by_environment": {k: round(v, 2) for k, v in env_totals.items()}}

@router.get("/by-team")
def costs_by_team(period: str = "2026-08"):
    costs = get_monthly_costs(period=period)
    team_totals: dict = {}
    for item in costs.breakdown:
        team = item.tags.get("team", "untagged")
        team_totals[team] = team_totals.get(team, 0) + item.cost_usd
    return {"period": period, "by_team": {k: round(v, 2) for k, v in team_totals.items()}}
