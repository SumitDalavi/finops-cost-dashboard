# Runbook — finops-cost-dashboard
> Last updated: 2026-08-29

## Quick Start
```bash
docker-compose up -d --build
```
UI: `http://localhost:5173`
API Docs: `http://localhost:8080/docs`

## Environment Variables
| Variable | Default | Purpose |
|---|---|---|
| AZURE_TENANT_ID | - | For real Azure AD auth |
| AZURE_CLIENT_ID | - | For real Azure AD auth |
| AZURE_CLIENT_SECRET | - | For real Azure AD auth |

## Common Failure Modes
| Symptom | Cause | Fix |
|---|---|---|
| No data in UI | API unreachable | Check if backend is running on 8080 |
