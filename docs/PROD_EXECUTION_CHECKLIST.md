# Production Execution Checklist (Render)

This file is the actionable checklist to close remaining requirements from local-ready to submission-ready.

## 1) Repository readiness
- [ ] Code pushed to `main` in GitHub/GitLab
- [ ] `render.yaml` present
- [ ] `.env.example` present and complete
- [ ] `docs/DEPLOY_RENDER.md` present
- [ ] `python manage.py check` passes
- [ ] `pytest -q` passes

## 2) Render infrastructure
- [ ] PostgreSQL service `cineverse-db` created
- [ ] Web service created from repository
- [ ] Build command set: `pip install -r requirements.txt`
- [ ] Start command set: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn cineverse.wsgi:application`
- [ ] First deploy successful on `https://<service>.onrender.com`

## 3) Environment variables (Render)
- [ ] `SECRET_KEY` (strong random)
- [ ] `DEBUG=False`
- [ ] `USE_SQLITE=False`
- [ ] `DATABASE_URL` from Render DB
- [ ] `DB_SSL_REQUIRE=True`
- [ ] `ALLOWED_HOSTS=<service>.onrender.com`
- [ ] `CSRF_TRUSTED_ORIGINS=https://<service>.onrender.com`
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] Service redeployed and healthy

## 4) Domain + SSL
- [ ] Domain purchased/registered
- [ ] Custom domain added in Render
- [ ] DNS records configured at registrar
- [ ] `ALLOWED_HOSTS=<domain>,<service>.onrender.com`
- [ ] `CSRF_TRUSTED_ORIGINS=https://<domain>,https://<service>.onrender.com`
- [ ] SSL certificate issued
- [ ] `https://<domain>` opens correctly

## 5) HTTPS redirect
- [ ] `http://<domain>` redirects to `https://<domain>`
- [ ] Browser lock icon visible

## 6) Smoke checks
- [ ] `/`
- [ ] `/movies/`
- [ ] `/movies/<slug>/`
- [ ] `/about/`
- [ ] `/api/v1/movies/`
- [ ] `/api/v1/search/?q=test`
- [ ] Auth flow (register/login/logout/password reset)
- [ ] Staff-only write rules validated
- [ ] Static/media no 404

### Automated smoke helper
Run:
```bash
python scripts/prod_smoke_check.py --base-url https://<domain> --http-url http://<domain>
```
Generated report:
- `docs/PROD_SMOKE_RESULT.md`

## 7) Operations and backups
- [ ] Logs location documented (Render Logs)
- [ ] Restart procedure documented (Manual Deploy/Restart)
- [ ] Daily `pg_dump` backup configured
- [ ] Restore tested using scripts in `scripts/`

## 8) Submission package
- [ ] `README.md` updated with real domain/render links
- [ ] `README.md` checklist marked Pass/Fail
- [ ] `docs/SUBMISSION_REPORT_TEMPLATE.md` filled
- [ ] Screenshots attached (home, catalog, detail, profile, admin, SSL/domain)
- [ ] Final deadline check: project online before **2026-06-01**
