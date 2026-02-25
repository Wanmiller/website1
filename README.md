# PersonaVerse

PersonaVerse is a Django + DRF community platform for discussions about public personalities.
This stage is focused on **local readiness**. Hosting/domain proof is intentionally deferred.

## Stack
- Python 3.10+
- Django 5.2
- Django REST Framework
- PostgreSQL (production) / SQLite (local fallback)
- Base UI template: HTML5 UP ZeroFour (`static/html5up-zerofour/`)

## Active project structure
Custom apps (11):
- `core`
- `accounts`
- `people`
- `threads`
- `comments`
- `votes`
- `moderation`
- `search`
- `engagement`
- `dashboard`
- `api`

Domain models (15):
- `UserProfile`, `LoginAudit`
- `Person`
- `Thread`
- `Comment`
- `Vote`
- `Report`
- `Tag`, `ThreadTag`
- `Bookmark`
- `Rating`
- `Follow`
- `Notification`
- `Attachment`
- `ViewEvent`

## Local setup
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_personaverse
python manage.py runserver
```

## Main web routes
- `/` - feed
- `/people/` - people directory
- `/people/<slug>/` - person detail
- `/threads/` - thread list with filters + pagination
- `/threads/create/` - create thread (auth)
- `/threads/<slug>/` - thread detail
- `/threads/<slug>/edit/` - edit thread (author/staff)
- `/threads/<slug>/delete/` - delete thread (author/staff)
- `/comments/<id>/reply/` - reply to comment (auth)
- `/bookmarks/` - my bookmarks (auth)
- `/search/` and `/search/live/` - search + AJAX autocomplete
- `/moderation/` - moderation panel (staff)
- `/dashboard/` - dashboard (staff)
- `/auth/profile/` - profile + "my activity"

## Roles and permissions
- Anonymous: read-only pages + read-only API list/detail
- Auth user: create thread/comment/vote/bookmark/rating/report
- Staff/admin: moderation + dashboard + thread write operations in detail API

Test users from `seed_personaverse`:
- `staff` / `staff12345`
- `pv_user_1..5` / `test12345`

## Login rate-limit (local security)
Simple anti-bruteforce is enabled in login view (IP + username cache key).

Env vars:
- `LOGIN_MAX_ATTEMPTS` (default `5`)
- `LOGIN_LOCKOUT_SECONDS` (default `600`)

Behavior:
- failed attempts increase counter
- after threshold, login is temporarily blocked
- successful login resets counter

## API v1
Endpoints:
- `GET /api/v1/persons/?q=`
- `GET /api/v1/threads/?q=&person=&ordering=&created_after=&score_min=`
- `POST /api/v1/threads/` (auth)
- `GET /api/v1/threads/<slug>/`
- `PATCH/DELETE /api/v1/threads/<slug>/` (staff)
- `POST /api/v1/comments/` (auth)
- `POST /api/v1/votes/` (auth)
- `POST /api/v1/bookmarks/` (auth)
- `POST /api/v1/ratings/` (auth)
- `POST /api/v1/reports/` (auth)

Unified error format:
```json
{"error":{"code":"...","message":"...","details":{}}}
```

### API examples
List threads:
```bash
curl -s "http://127.0.0.1:8000/api/v1/threads/?ordering=hot&score_min=0"
```

Create thread (auth):
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/threads/" \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=<session>" \
  -d "{\"title\":\"Local API thread\",\"body\":\"Body\",\"person_id\":1}"
```

400 validation error example:
```json
{
  "error": {
    "code": "400",
    "message": "Request failed.",
    "details": {"value": ["Ensure this value is less than or equal to 5."]}
  }
}
```

403 permission error example:
```json
{
  "error": {
    "code": "403",
    "message": "You do not have permission to perform this action.",
    "details": {"detail": "You do not have permission to perform this action."}
  }
}
```

404 not found example:
```json
{
  "error": {
    "code": "404",
    "message": "Not found.",
    "details": {"detail": "Not found."}
  }
}
```

## Template/navigation/accessibility notes
- Base layout with header/footer/menu and active section highlight.
- Custom 404/500 pages.
- Breadcrumbs on key internal pages.
- Visible focus states for links/buttons/inputs.
- `alt` is used for rendered images; placeholder fallback is provided.

## JS scenarios (17)
1. Theme switch and persistence (`localStorage`).
2. Auto-dismiss flash messages.
3. Manual flash dismiss button.
4. Submit-lock for forms (`data-submit-lock`).
5. Client-side required field validation.
6. Client-side email format validation.
7. Client-side password match validation.
8. Client-side numeric/date/range validation for filters.
9. Client-side validation for report reason length.
10. Modal confirmation before destructive submit (`data-confirm-message`).
11. Keyboard shortcut Ctrl/Cmd+K for search focus.
12. Escape clears active notifications/results.
13. Live search debounce.
14. Live search loading state (`aria-busy`) + stale-request guard.
15. Live search keyboard navigation (up/down + Enter select).
16. AJAX bookmark/rating/vote updates with UI feedback.
17. Nav dropdown `aria-expanded` sync for hover/focus/click.

## CSS effects (15)
1. Link hover color change.
2. Link visible focus outline.
3. Flash card transition.
4. Flash hover elevation.
5. Flash dismiss hover/focus styling.
6. Action feedback fade/slide animation.
7. Article card transition.
8. Article card hover elevation.
9. Search item hover state.
10. Search item keyboard-active state.
11. Input focus ring.
12. Button hover lift.
13. Button focus ring.
14. Loading button visual state.
15. Responsive breakpoints (`1280`, `980`, `736`).

## Logging (local)
Console logging is configured in `cineverse/settings.py` (`LOGGING` block).
No secrets are logged intentionally. Only level/name/message format is printed.

Tune with:
- `LOG_LEVEL=INFO` (or `DEBUG`, `WARNING`)

## Local quality checks
```bash
python manage.py check
pytest -q
```

## Local compliance status
See:
- `docs/LOCAL_COMPLIANCE_CHECKLIST.md`

Summary:
- Local code/functionality requirements are mostly closed.
- Hosting/domain/SSL/production evidence remain for the deployment phase.

## What remains for deployment phase
- Real domain and SSL proof
- Public production smoke result
- Final production checklist completion
- Public availability confirmation before **2026-06-01**

## Deployment references
- `docs/DEPLOY_RENDER.md`
- `docs/RENDER_BLUEPRINT_QUICKSTART.md`
- `docs/PROD_EXECUTION_CHECKLIST.md`
- `docs/PROD_SMOKE_RESULT.md`
