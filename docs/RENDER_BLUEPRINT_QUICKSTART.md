# Render Blueprint Quickstart (UI)

Use this checklist to execute deployment via Render Blueprint with this repository.

## 1) Preconditions
- Repository is pushed to `main`
- `render.yaml` exists in repo root
- Local checks pass:
  - `python manage.py check`
  - `pytest -q`

## 2) Validate blueprint locally
```bash
python scripts/validate_render_blueprint.py
```
Expected: all PASS.

## 3) Import in Render
1. Render Dashboard -> **New** -> **Blueprint**.
2. Connect your Git provider and select this repository.
3. Select branch `main`.
4. Confirm creation.

Render should provision:
- PostgreSQL: `cineverse-db`
- Web service: `cineverse-web`

## 4) Verify Environment in Render web service
Required env vars:
- `SECRET_KEY` (generated)
- `DEBUG=False`
- `USE_SQLITE=False`
- `DATABASE_URL` (linked from DB)
- `DB_SSL_REQUIRE=True`
- `ALLOWED_HOSTS=cineverse-web.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://cineverse-web.onrender.com`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

If any key is missing, add it manually and redeploy.

## 5) First deploy validation
Check Render logs for:
- migrations success
- collectstatic success
- gunicorn startup without crash loop

Open:
- `https://cineverse-web.onrender.com/`
- `https://cineverse-web.onrender.com/api/v1/movies/`

## 6) After buying domain
Update env:
- `ALLOWED_HOSTS=<your-domain>,cineverse-web.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-domain>,https://cineverse-web.onrender.com`

Add Custom Domain in Render and configure DNS records at registrar.

## 7) Smoke report
Run after deployment:
```bash
python scripts/prod_smoke_check.py --base-url https://<your-domain> --http-url http://<your-domain>
```
Output:
- `docs/PROD_SMOKE_RESULT.md`
