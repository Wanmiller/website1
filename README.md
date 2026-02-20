# CineVerse

CineVerse is an individual Django + DRF educational project (online movie platform) prepared for the 100-point final assignment criteria.

## Stack
- Python 3.10+
- Django 5.2
- Django REST Framework
- PostgreSQL
- HTML/CSS/JS (static assets in `static/`)

## Local setup
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

## Main URLs
- Home: `/`
- Movies: `/movies/`
- Genres: `/genres/`
- People: `/people/`
- Reviews: `/reviews/`
- Favorites: `/favorites/`
- Profile: `/auth/profile/`
- About: `/about/`
- Admin: `/admin/`

## API v1
- `GET /api/v1/movies/?q=&genre=&year=&ordering=&rating_min=`
- `POST /api/v1/movies/` (staff only)
- `GET /api/v1/movies/<slug>/`
- `PUT/PATCH/DELETE /api/v1/movies/<slug>/` (staff only)
- `GET/POST /api/v1/reviews/` (POST auth required)
- `GET/POST /api/v1/favorites/` (auth required)
- `GET /api/v1/search/?q=`

### Example response (error format)
```json
{
  "error": {
    "code": "403",
    "message": "You do not have permission to perform this action.",
    "details": {
      "detail": "You do not have permission to perform this action."
    }
  }
}
```

## Test accounts (after `seed_data`)
- staff: `staff` / `staff12345`

## Quality commands
```bash
pytest
python manage.py test
black .
isort .
```

## Deploy notes (Render)
- Use `render.yaml` as blueprint for Web + PostgreSQL services.
- Build command: `pip install -r requirements.txt`
- Start command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn cineverse.wsgi:application`
- Set env vars: `DEBUG=False`, `USE_SQLITE=False`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, secure cookie flags.
- Enable HTTPS redirect (`SECURE_SSL_REDIRECT=True`) and verify HTTP -> HTTPS.
- Add custom domain and DNS records, then verify SSL certificate is issued.
- Full step-by-step guide: `docs/DEPLOY_RENDER.md`


## Production links
- Domain: `https://website1-uoa2.onrender.com`
- Render URL: `https://website1-uoa2.onrender.com`
- Deployment guide: `docs/DEPLOY_RENDER.md`
- Render Blueprint quickstart: `docs/RENDER_BLUEPRINT_QUICKSTART.md`
- Blueprint validator: `scripts/validate_render_blueprint.py`
- Production execution checklist: `docs/PROD_EXECUTION_CHECKLIST.md`
- Automated smoke script: `scripts/prod_smoke_check.py`
- Smoke output report: `docs/PROD_SMOKE_RESULT.md`
- Submission report template: `docs/SUBMISSION_REPORT_TEMPLATE.md`

## Logs and restart (platform-agnostic)
- App logs: provider dashboard (web service logs)
- Restart: provider web service restart action

## Backup strategy
- Daily `pg_dump` backup from production PostgreSQL
- Weekly restore test into temporary database
- Linux/macOS scripts: `scripts/db_backup.sh`, `scripts/db_restore.sh`
- Windows scripts: `scripts/db_backup.ps1`, `scripts/db_restore.ps1`

## Acceptance checklist snapshot
- [x] 10 apps
- [x] 15+ models with FK/M2M
- [x] 15+ UI pages
- [x] static/media integrated
- [x] auth + roles
- [x] CRUD + pagination + filtering
- [x] 5 API endpoints + filters + protected methods
- [x] admin customizations (list/search/filter/inline/actions)
- [x] custom template filter
- [x] seed command + docs

## Deadline reminder
Project must be online and available by **01.06.2026** according to assignment rules.

## Template Source
- Template: HTML5 UP Escape Velocity
- Source path in project: `static/html5up-escape-velocity/`
- License: Creative Commons Attribution 3.0 (`static/html5up-escape-velocity/LICENSE.txt`)
- Adaptations made: Django base layout integration, top navigation for desktop/mobile, all project pages migrated to Escape Velocity sections, and custom project JS merged in `static/js/app.js`.

## JS Scenarios Matrix (15+)
| # | Scenario | Where |
|---|---|---|
| 1 | Theme toggle + localStorage | `static/js/app.js` (`[data-theme-picker]`) |
| 2 | Flash auto-dismiss queue | `static/js/app.js` (`.flash`) |
| 3 | Live search input listener | `static/js/app.js` (`#live-search-input`) |
| 4 | Debounced query (300ms) | `static/js/app.js` |
| 5 | Fetch live search endpoint | `static/js/app.js` -> `/search/live/` |
| 6 | Render dynamic search results list | `static/js/app.js` (`#live-search-results`) |
| 7 | Filter querystring sync on change | `static/js/app.js` (`#movie-filter-form`) |
| 8 | Favorite AJAX toggle | `static/js/app.js` (`[data-favorite-toggle]`) |
| 9 | CSRF injection from hidden form/cookie | `static/js/app.js` (`csrfToken`) |
| 10 | Quick rating AJAX submit | `static/js/app.js` (`#ajax-rate-btn`) |
| 11 | Parse JSON response and update UI text | `static/js/app.js` (favorite state) |
| 12 | Keyboard shortcut Ctrl/Cmd+K | `static/js/app.js` |
| 13 | Focus transfer to search input | `static/js/app.js` |
| 14 | DOM utility wrappers (`qs`, `qsa`) | `static/js/app.js` |
| 15 | Escape Velocity nav/dropotron behavior | `static/html5up-escape-velocity/assets/js/main.js` |

## CSS Effects Matrix (15+)
| # | Effect | Where |
|---|---|---|
| 1 | Full-screen preload transition (`is-preload`) | `static/html5up-escape-velocity/assets/css/main.css` |
| 2 | Header/logo section styling | `static/html5up-escape-velocity/assets/css/main.css` |
| 3 | Top nav hover/dropdown styling | `static/html5up-escape-velocity/assets/css/main.css` |
| 4 | Wrapper section styles (`style1/2/3`) | `static/html5up-escape-velocity/assets/css/main.css` |
| 5 | Highlight card and image presentation | `static/html5up-escape-velocity/assets/css/main.css` |
| 6 | Button hover/active transitions | `static/html5up-escape-velocity/assets/css/main.css` |
| 7 | Form field focus styles | `static/html5up-escape-velocity/assets/css/main.css` |
| 8 | Responsive breakpoints (desktop/tablet/mobile) | `static/html5up-escape-velocity/assets/css/main.css` |
| 9 | Icon/font-awesome visual system | `static/html5up-escape-velocity/assets/css/fontawesome-all.min.css` |
| 10 | Theme variable switch (template/dark) | `static/css/cineverse-escape.css` |
| 11 | Mobile top-nav horizontal scroll behavior | `static/css/cineverse-escape.css` |
| 12 | Flash message accent borders | `static/css/cineverse-escape.css` |
| 13 | Genre/rating chips rounded badges | `static/css/cineverse-escape.css` |
| 14 | Inline rating control layout | `static/css/cineverse-escape.css` |
| 15 | Grid layouts for cards/stats/genres | `static/css/cineverse-escape.css` |

## Deploy Smoke Checklist (Prod)
- [x] Domain resolves to hosting and opens over HTTPS (`https://website1-uoa2.onrender.com`)
- [x] HTTP -> HTTPS redirect works (automated smoke PASS)
- [x] `DEBUG=False` in production environment
- [x] `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` set correctly
- [x] PostgreSQL connection works in production
- [x] `collectstatic` executed and static assets load without 404
- [ ] Media files open from `MEDIA_URL` (PENDING manual check)
- [ ] Auth flow works: register/login/logout/password reset (PENDING manual check)
- [x] Core pages load: `/`, `/movies/`, `/about/` (automated smoke PASS)
- [x] API smoke: `/api/v1/movies/`, `/api/v1/search/` (automated smoke PASS)
- [ ] Staff-only API/write permissions validated (`POST /api/v1/movies/`) (PENDING manual check)
- [ ] Admin panel reachable for staff, blocked for anonymous users (PENDING manual check)
- [x] Server logs are visible in provider dashboard
- [ ] Backup (`pg_dump`) task runs and restore test documented (PENDING manual check)


## Final submission artifacts
- Automated smoke report (latest): `docs/PROD_SMOKE_RESULT.md`
- Fill production links and smoke results in this README checklist.
- Complete report from `docs/SUBMISSION_REPORT_TEMPLATE.md`.
- Attach key screenshots (home, catalog, detail, profile, admin, SSL/domain).

## Production smoke command
```bash
python scripts/prod_smoke_check.py --base-url https://website1-uoa2.onrender.com --http-url http://website1-uoa2.onrender.com
```
