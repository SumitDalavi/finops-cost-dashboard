import os
import json
import redis
from sqlalchemy import create_engine, text
from ..models import CostItem, CostSummary

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
DB_URL = os.environ.get("DB_URL", "postgresql://postgres:postgres@localhost:5432/finops")

redis_client = redis.Redis.from_url(REDIS_URL, socket_timeout=1, socket_connect_timeout=1)

try:
    engine = create_engine(DB_URL, connect_args={"connect_timeout": 1})
except Exception as e:
    engine = None
    print(f"Failed to connect to database: {e}")

def get_monthly_costs(subscription_id: str = "mock-sub-id", period: str = "2026-08") -> CostSummary:
    cache_key = f"costs:{subscription_id}:{period}"
    
    # Check cache first
    try:
        cached = redis_client.get(cache_key)
        if cached:
            data = json.loads(cached)
            # Reconstruct models
            return CostSummary(**data)
    except Exception as e:
        print(f"Redis cache error: {e}")

    # Fallback to simulated database (Athena/CUR)
    mock_items = []
    
    if engine:
        try:
            with engine.connect() as conn:
                # Setup mock data table if it doesn't exist
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS mock_cur_export (
                        id SERIAL PRIMARY KEY,
                        resource_group VARCHAR,
                        service_name VARCHAR,
                        cost_usd FLOAT,
                        billing_period VARCHAR,
                        tags JSONB
                    )
                """))
                
                # Check if we have data for this period
                res = conn.execute(text("SELECT COUNT(*) FROM mock_cur_export WHERE billing_period = :p"), {"p": period}).scalar()
                
                if res == 0:
                    # Seed mock data
                    seed_data = [
                        {"resource_group": "rg-production", "service_name": "Azure Kubernetes Service", "cost_usd": 2847.50, "billing_period": period, "tags": json.dumps({"team": "platform", "env": "prod"})},
                        {"resource_group": "rg-production", "service_name": "Azure Cosmos DB", "cost_usd": 1523.20, "billing_period": period, "tags": json.dumps({"team": "backend", "env": "prod"})},
                        {"resource_group": "rg-production", "service_name": "Azure Blob Storage", "cost_usd": 342.80, "billing_period": period, "tags": json.dumps({"team": "data", "env": "prod"})},
                    ]
                    for seed in seed_data:
                        conn.execute(text("""
                            INSERT INTO mock_cur_export (resource_group, service_name, cost_usd, billing_period, tags)
                            VALUES (:resource_group, :service_name, :cost_usd, :billing_period, :tags)
                        """), seed)
                    conn.commit()

                # Fetch data
                rows = conn.execute(text("SELECT resource_group, service_name, cost_usd, billing_period, tags FROM mock_cur_export WHERE billing_period = :p"), {"p": period})
                for row in rows:
                    mock_items.append(CostItem(
                        resource_group=row[0],
                        service_name=row[1],
                        cost_usd=row[2],
                        billing_period=row[3],
                        tags=row[4]
                    ))
        except Exception as e:
            print(f"Database error: {e}, falling back to static mock data")

    if not mock_items:
        # Static mock data as final fallback
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
    
    summary = CostSummary(
        total_cost=round(total, 2),
        period=period,
        breakdown=mock_items,
        top_services=top_services
    )

    # Set cache (expire in 1 hour)
    try:
        redis_client.setex(cache_key, 3600, summary.model_dump_json())
    except Exception as e:
        print(f"Redis cache set error: {e}")

    return summary
