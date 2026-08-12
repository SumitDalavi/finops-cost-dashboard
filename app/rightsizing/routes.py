from fastapi import APIRouter
from .analyzer import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def rightsizing_recommendations():
    recs = get_recommendations()
    total_savings = sum(r.estimated_savings_pct for r in recs if r.estimated_savings_pct > 0)
    actionable = [r for r in recs if r.estimated_savings_pct > 10]
    return {
        "total_pods_analyzed": len(recs),
        "actionable_recommendations": len(actionable),
        "recommendations": recs
    }
