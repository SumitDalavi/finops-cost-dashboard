# FinOps Cost Dashboard 💰📊

> Azure Cost Management API + Kubernetes right-sizing recommender — giving engineering teams real-time cost visibility and actionable optimization recommendations.

## The Problem

Cloud costs are the new technical debt. Teams over-provision resources "just in case," and nobody notices until the monthly bill arrives. FinOps (Financial Operations) is a growing discipline that brings cost accountability to engineering teams — but most organizations lack the tooling to make it actionable.

## The Solution

This project provides two integrated capabilities:
1. **Cloud Cost API**: A FastAPI backend that queries Azure Cost Management APIs to surface cost breakdowns by resource group, service, and tag
2. **K8s Right-Sizing Recommender**: Analyzes Kubernetes resource utilization (CPU/memory requests vs actual usage) and recommends optimal resource requests
3. **Automated Remediation**: Can automatically generate GitHub/GitLab Pull Requests to the GitOps repository to apply the recommended right-sizing changes.

```
┌────────────────┐     ┌────────────────────┐     ┌──────────────┐
│ Azure Cost     │────►│  FastAPI Backend    │────►│  Dashboard   │
│ Management API │     │                    │     │  (JSON API)  │
└────────────────┘     │  ┌──────────────┐  │     └──────────────┘
                       │  │ K8s Metrics  │  │
┌────────────────┐     │  │ Right-Sizer  │  │
│ metrics-server │────►│  └──────────────┘  │
│ (K8s)          │     └────────────────────┘
└────────────────┘
```

## Why This Over the Obvious Alternative

Opening the Azure portal and viewing Cost Analysis is not FinOps. This project demonstrates **programmatic cost management**: API-driven data retrieval, automated right-sizing recommendations, and a structured JSON API that can feed into Slack bots, Grafana dashboards, or executive reports.

## 📁 Project Structure

```
├── app/
│   ├── main.py               # FastAPI application
│   ├── cost/
│   │   ├── routes.py          # Cost Management API endpoints
│   │   └── azure_client.py    # Azure Cost Management SDK wrapper
│   ├── rightsizing/
│   │   ├── routes.py          # Right-sizing recommendation endpoints
│   │   ├── analyzer.py        # Resource utilization analyzer
│   │   └── pr_generator.py    # GitOps PR generation logic
│   └── models.py              # Pydantic schemas
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── docs/ARCHITECTURE.md
└── README.md
```

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Cloud APIs**: Azure Cost Management, Azure Resource Graph
- **Kubernetes**: metrics-server, VPA data
- **Containerization**: Docker

## Decision Log

| Decision | Rationale |
|----------|-----------|
| FastAPI over Flask | Async support for concurrent API calls to Azure; auto-generated OpenAPI docs |
| Mock data layer | Keeps PoC self-contained; Azure Cost Management APIs require billing access |
| Right-sizing as separate module | Clean separation allows this component to work independently with any K8s cluster |
| JSON API over UI | API-first enables consumption by Grafana, Slack bots, and CI/CD pipelines |


## ðŸ“‹ Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://www.docker.com/) | >= 24.x | Container runtime |
| [Docker Compose](https://docs.docker.com/compose/) | >= 2.x | Multi-container orchestration |
| [curl](https://curl.se/) or browser | Any | API testing |

*For local dev without Docker: Python >= 3.11, pip*

## ðŸš€ Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/SumitDalavi/finops-cost-dashboard.git
cd finops-cost-dashboard

# 2. Build and start
docker-compose up -d --build

# 3. Verify it's running
curl http://localhost:8080/health
```

The API is now available at **http://localhost:8080** | Swagger UI at **http://localhost:8080/docs**

## ðŸ§ª Usage & Demo

### Cloud Cost Analysis
```bash
# Get monthly cost breakdown
curl http://localhost:8080/api/v1/costs/monthly?period=2026-08

# Get costs grouped by environment (dev/staging/prod)
curl http://localhost:8080/api/v1/costs/by-environment?period=2026-08

# Get costs grouped by team
curl http://localhost:8080/api/v1/costs/by-team?period=2026-08
```

### Kubernetes Right-Sizing
```bash
# Get right-sizing recommendations for all pods
curl http://localhost:8080/api/v1/k8s/recommendations

# Apply a recommendation (generates a GitOps PR)
curl -X POST http://localhost:8080/api/v1/k8s/apply \
  -H "Content-Type: application/json" \
  -d '{
    "pod_name": "api-gateway-7d8f9c6b5-x2k4m",
    "namespace": "production",
    "gitops_repo_url": "https://github.com/org/k8s-manifests"
  }'
```

### Interactive Testing
Open **http://localhost:8080/docs** for the full Swagger UI.

## âœ… Verification

| Check | Command | Expected |
|-------|---------|----------|
| Health | `curl http://localhost:8080/health` | `{"status": "ok"}` |
| Costs | `curl http://localhost:8080/api/v1/costs/monthly` | Cost breakdown JSON |
| Right-Sizing | `curl http://localhost:8080/api/v1/k8s/recommendations` | Pod recommendations |
| Swagger | Open `http://localhost:8080/docs` | Interactive API docs |

```bash
# Stop the service
docker-compose down
```

## 👨‍💻 Author

*Built to demonstrate FinOps engineering: programmatic cost management and Kubernetes resource optimization.*
