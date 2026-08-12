from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .analyzer import get_recommendations
from .pr_generator import generate_pr_for_recommendation

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

class ApplyRecommendationRequest(BaseModel):
    pod_name: str
    namespace: str
    gitops_repo_url: str

@router.post("/apply")
def apply_recommendation(req: ApplyRecommendationRequest):
    recs = get_recommendations()
    # Find the specific recommendation
    target_rec = next((r for r in recs if r.pod_name == req.pod_name and r.namespace == req.namespace), None)
    
    if not target_rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
        
    result = generate_pr_for_recommendation(target_rec, req.gitops_repo_url)
    return result
