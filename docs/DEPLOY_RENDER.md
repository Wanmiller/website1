# Render Deployment Guide (CineVerse)

## 1) Create services
1. Push repository to GitHub/GitLab.
2. In Render, create PostgreSQL database `cineverse-db`.
3. Create web service from this repository.
4. You can import `render.yaml` or set values manually.

## 2) Build and start
- Build command:
  - `pip install -r requirements.txt`
- Start command:
  - `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn cineverse.wsgi:application`

## 3) Required environment variables
- `SECRET_KEY` (random, non-default)
- `DEBUG=False`
- `USE_SQLITE=False`
- `DATABASE_URL` (from Render PostgreSQL)
- `DB_SSL_REQUIRE=True`
- `ALLOWED_HOSTS=<your-domain>,<service>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-domain>,https://<service>.onrender.com`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

## 4) Domain + SSL
1. Buy/register domain at registrar.
2. In Render web service settings, add Custom Domain.
3. Add required DNS records in registrar panel.
4. Wait for certificate issuance.
5. Verify HTTPS is active and HTTP redirects to HTTPS.

## 5) Smoke checks
- Open:
  - `/`
  - `/movies/`
  - `/movies/<slug>/`
  - `/about/`
  - `/api/v1/movies/`
  - `/api/v1/search/?q=test`
- Validate auth flow: register/login/logout/password reset.
- Validate staff-only write on movies API.
- Validate static and media loading (no 404).

## 6) Logs and restart
- Logs: Render service -> Logs tab.
- Restart: Render service -> Manual Deploy / Restart.

## 7) Backups
- Linux/macOS:
  - `export DATABASE_URL='postgres://...'`
  - `bash scripts/db_backup.sh`
  - `bash scripts/db_restore.sh backups/cineverse_xxx.sql.gz`
- Windows PowerShell:
  - `$env:DATABASE_URL='postgres://...'`
  - `./scripts/db_backup.ps1`
  - `./scripts/db_restore.ps1 -InFile backups/cineverse_xxx.sql`
