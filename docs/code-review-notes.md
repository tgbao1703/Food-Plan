# Code review notes (backend MVP)

## Issues found and fixed in this PR

1. **Weak error handling with `.get()`** in API views could return 500 for missing records.
   - Fixed by switching to `get_object_or_404` in critical endpoints.

2. **Missing validation** for key input fields.
   - Added validation for:
     - `Place.latitude` / `Place.longitude` ranges in serializer.
     - `Review.star` must be 1..5.
     - Route request `origin/destination` lat/lng with type and range checks.

3. **Permission clarity for write endpoints**.
   - Explicitly enforced `IsAuthenticated` on create/write actions.

4. **No health endpoint for deployment checks**.
   - Added `GET /api/v1/health` for readiness/smoke checks.

5. **No automated tests in repo for API basics**.
   - Added initial API tests covering health, auth requirement, review->stats update, route validation, and place detail retrieval.

## Next PR proposal: hostable + proper UI

- Web UI (React + Vite) with pages:
  - Map + leaderboard layout
  - Place detail panel (Info/Reviews/Photos/Route)
- Docker multi-service compose:
  - nginx + backend + frontend + db
- Production-ready runtime:
  - Gunicorn for Django
  - Static file serving
  - `.env.example` and deploy guide
- Basic auth flow + route query integration in UI
