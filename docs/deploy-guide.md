# Deploy guide (GitHub -> Render)

## 1) Push code to GitHub

- Ensure `main` branch contains:
  - `backend/Dockerfile`
  - `backend/entrypoint.sh`
  - `render.yaml`

## 2) Create Render service from Blueprint

1. In Render, choose **New + > Blueprint**.
2. Connect your GitHub repo.
3. Render reads `render.yaml` and creates:
   - `foodplan-backend` (web service)
   - `foodplan-db` (Postgres)

## 3) Configure environment variables

Set these in Render (or keep defaults from `render.yaml`):

- `DEBUG=0`
- `DJANGO_SECRET_KEY=<secure-random>`
- `ALLOWED_HOSTS=<your-render-domain>`
- `CSRF_TRUSTED_ORIGINS=https://<your-render-domain>`
- `DATABASE_URL` (wired from Render DB)

## 4) Health check

Render health endpoint:
- `GET /api/v1/health`

Expected response:
```json
{"status": "ok"}
```

## 5) Local production-like run

```bash
docker compose up --build
```

Backend runs with gunicorn via `entrypoint.sh`.
