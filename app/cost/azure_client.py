"""
Mock Azure Cost Management Client.
In production, this would use azure-mgmt-costmanagement SDK.
"""

from ..models import CostItem, CostSummary

def get_monthly_costs(subscription_id: str = "mock-sub-id", period: str = "2026-08") -> CostSummary:
    """Simulates querying Azure Cost Management API."""
    
    mock_items = [
        CostItem(resource_group="rg-production", service_name="Azure Kubernetes Service", cost_usd=2847.50, billing_period=period, tags={"team": "platform", "env": "prod"}),
        CostItem(resource_group="rg-production", service_name="Azure Cosmos DB", cost_usd=1523.20, billing_period=period, tags={"team": "backend", "env": "prod"}),
        CostItem(resource_group="rg-production", service_name="Azure Blob Storage", cost_usd=342.80, billing_period=period, tags={"team": "data", "env": "prod"}),
        CostItem(resource_group="rg-staging", service_name="Azure Kubernetes Service", cost_usd=891.00, billing_period=period, tags={"team": "platform", "env": "staging"}),
        CostItem(resource_group="rg-staging", service_name="Azure SQL Database", cost_usd=456.30, billing_period=period, tags={"team": "backend", "env": "staging"}),
        CostItem(resource_group="rg-dev", service_name="Virtual Machines", cost_usd=1205.60, billing_period=period, tags={"team": "dev", "env": "dev"}),
        CostItem(resource_group="rg-dev", service_name="Azure Kubernetes Service", cost_usd=678.90, billing_period=period, tags={"team": "platform", "env": "dev"}),
        CostItem(resource_group="rg-shared", service_name="Azure Monitor", cost_usd=289.40, billing_period=period, tags={"team": "sre", "env": "shared"}),
    ]
    
    total = sum(item.cost_usd for item in mock_items)
    
    # Aggregate by service
    service_totals: dict = {}
    for item in mock_items:
        service_totals[item.service_name] = service_totals.get(item.service_name, 0) + item.cost_usd
    
    top_services = sorted(
        [{"service": k, "cost_usd": round(v, 2)} for k, v in service_totals.items()],
        key=lambda x: x["cost_usd"],
        reverse=True
    )
    
    return CostSummary(
        total_cost=round(total, 2),
        period=period,
        breakdown=mock_items,
        top_services=top_services
    )
