# FinOps Cost Dashboard 💰📊

> Azure Cost Management API + Kubernetes right-sizing recommender — giving engineering teams real-time cost visibility and actionable optimization recommendations.

## The Problem

Cloud costs are the new technical debt. Teams over-provision resources "just in case," and nobody notices until the monthly bill arrives. FinOps (Financial Operations) is a growing discipline that brings cost accountability to engineering teams — but most organizations lack the tooling to make it actionable.

## The Solution

This project provides two integrated capabilities:
1. **Cloud Cost API**: A FastAPI backend that queries Azure Cost Management APIs to surface cost breakdowns by resource group, service, and tag
2. **K8s Right-Sizing Recommender**: Analyzes Kubernetes resource utilization (CPU/memory requests vs actual usage) and recommends optimal resource requests

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
│   │   └── analyzer.py        # Resource utilization analyzer
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

## 👨‍💻 Author

*Built to demonstrate FinOps engineering: programmatic cost management and Kubernetes resource optimization.*
