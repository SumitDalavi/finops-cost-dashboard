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
