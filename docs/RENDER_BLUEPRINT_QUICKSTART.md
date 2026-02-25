# Render Blueprint Quickstart (PersonaVerse)

Use this checklist to execute deployment via Render Blueprint.

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

## 4) Verify Environment in Render web service
Required env vars:
- `SECRET_KEY` (generated)
- `DEBUG=False`
- `USE_SQLITE=False`
- `DATABASE_URL` (linked from DB)
- `DB_SSL_REQUIRE=True`
- `ALLOWED_HOSTS=<service>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<service>.onrender.com`
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
- `https://<service>.onrender.com/`
- `https://<service>.onrender.com/threads/`
- `https://<service>.onrender.com/api/v1/threads/`

## 6) After buying domain
Update env:
- `ALLOWED_HOSTS=<your-domain>,<service>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-domain>,https://<service>.onrender.com`

Add Custom Domain in Render and configure DNS records at registrar.

## 7) Smoke report
Run after deployment:
```bash
python scripts/prod_smoke_check.py --base-url https://<your-domain> --http-url http://<your-domain>
```
Output:
- `docs/PROD_SMOKE_RESULT.md`
