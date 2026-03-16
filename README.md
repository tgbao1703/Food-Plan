# Food-Plan MVP Codebase

Backend is implemented with Django + DRF based on `docs/food-review-app-plan.md`.

## Run with Docker

```bash
docker compose up --build
```

API base: `http://localhost:8000/api/v1`

## Implemented endpoints
- `GET /api/v1/health`
- `GET/POST /api/v1/places`
- `GET /api/v1/places/{id}`
- `GET /api/v1/places/{id}/reviews`
- `GET /api/v1/places/{id}/media`
- `POST /api/v1/places/{id}/hot-marks`
- `POST /api/v1/reviews`
- `POST /api/v1/reviews/{id}/media`
- `GET /api/v1/leaderboard/users`
- `GET /api/v1/users/{id}`
- `GET /api/v1/users/{id}/reviews`
- `POST /api/v1/routes`

## Notes
- Realtime (Channels/Redis), Celery jobs, and full React/Flutter apps are planned next increments.
- Current `/api/v1/routes` is an MVP stub returning route estimates.
