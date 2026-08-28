from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from .cost import routes as cost_routes
from .rightsizing import routes as rightsizing_routes
import os

API_KEY_NAME = "X-API-Key"
API_KEY = os.environ.get("FINOPS_API_KEY", "dev-secret-key")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

app = FastAPI(
    title="FinOps Cost Dashboard",
    description="Azure Cost Management + Kubernetes Right-Sizing Recommender API",
    version="1.0.0"
)

app.include_router(cost_routes.router, prefix="/api/v1/costs", tags=["Cloud Costs"], dependencies=[Depends(get_api_key)])
app.include_router(rightsizing_routes.router, prefix="/api/v1/k8s", tags=["K8s Right-Sizing"], dependencies=[Depends(get_api_key)])

@app.get("/health")
def health():
    return {"status": "ok", "service": "finops-cost-dashboard"}
