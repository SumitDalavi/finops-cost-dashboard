# Decisions

## ADR-001: Separation of Cloud API and Dashboard
**Date:** 2026-08-29  
**Status:** Accepted

**Context:**  
FinOps data is complex. Trying to fetch and aggregate it in the frontend creates sluggish UIs.

**Decision:**  
We use a FastAPI backend to act as a caching/aggregation layer. The Azure client adapter standardizes the payload for the React frontend.

**Consequences:**  
- ✅ Much faster UI load times.
- ✅ Easy to add AWS or GCP adapters later by adhering to the same internal model.

## ADR-002: Progressive Credential Loading (PCL) Architecture
- **Context:** Production hardening required live backends (PostgreSQL, Redis, OpenAI, Anthropic), but removing mocks would break CI pipelines and create high developer onboarding friction.
- **Decision:** Implement Progressive Credential Loading. Keep in-memory and local mock heuristics as the default safe baseline, while wrapping external integrations in auto-promoting factory adapters triggered by environment variables.
- **Consequences:** 
  - *Pros:* 100% CI pass rate without requiring external secrets; zero setup friction for new contributors; progressive upgrade to production clusters.
  - *Cons:* Adds lightweight factory abstraction layers and runtime credential detection logic.
