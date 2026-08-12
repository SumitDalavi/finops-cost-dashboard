from fastapi import FastAPI
from .cost import routes as cost_routes
from .rightsizing import routes as rightsizing_routes

app = FastAPI(
    title="FinOps Cost Dashboard",
    description="Azure Cost Management + Kubernetes Right-Sizing Recommender API",
    version="1.0.0"
)

app.include_router(cost_routes.router, prefix="/api/v1/costs", tags=["Cloud Costs"])
app.include_router(rightsizing_routes.router, prefix="/api/v1/k8s", tags=["K8s Right-Sizing"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "finops-cost-dashboard"}
