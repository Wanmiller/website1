# Local Compliance Checklist (No Hosting/Domain)

Date baseline: 2026-02-25.
Scope: local project readiness only. Hosting/domain/SSL are excluded here.

## 1) Core architecture and repo
- [x] Django project runs locally
  Evidence: `python manage.py check` passes, local `runserver` works.
- [x] 10+ active apps configured
  Evidence: `core`, `accounts`, `people`, `threads`, `comments`, `votes`, `moderation`, `search`, `engagement`, `dashboard`, `api` (11 total, `cineverse/settings.py`).
- [x] `.env`-based settings
  Evidence: `load_dotenv(BASE_DIR / ".env")` in `cineverse/settings.py`, template variables in `.env.example`.
- [x] base template + shared layout
  Evidence: `templates/base.html` with shared header/footer/nav + includes.
- [x] custom 404/500 pages
  Evidence: `templates/core/404.html`, `templates/core/500.html`, handlers in `cineverse/urls.py`.
- [x] `requirements.txt` + `.env.example`
  Evidence: root files `requirements.txt` and `.env.example` are present and used.
- [x] lint/format tool config (`black`, `isort`)
  Evidence: `pyproject.toml` -> `[tool.black]`, `[tool.isort]`.
- [x] logging configured (console)
  Evidence: `LOGGING` block in `cineverse/settings.py` with console handler and project loggers.

## 2) Design, HTML, CSS, JS
- [x] Free HTML template integrated (HTML5 UP ZeroFour)
  Evidence: template assets in `static/html5up-zerofour/`, integrated in `templates/base.html`.
- [x] semantic page structure
  Evidence: layout uses semantic sections (`header`, `nav`, content wrappers, footer) in `templates/base.html`.
- [x] 15+ template pages
  Count: 29 HTML templates (`templates/`), including `core/home.html`, `core/about.html`, `threads/*`, `people/*`, `accounts/*`, `moderation/panel.html`, `dashboard/panel.html`.
- [x] responsive breakpoints
  Evidence: breakpoints `1280`, `980`, `736` in `static/css/personaverse-zerofour.css`.
- [x] static files via Django static
  Evidence: `{% load static %}` and static paths in templates + `STATICFILES_DIRS/STATIC_ROOT` in settings.
- [x] 15 JS scenarios documented
  Evidence: README section `JS scenarios (17)` + implementation in `static/js/app.js`.
- [x] 15 CSS effects documented
  Evidence: README section `CSS effects (15)` + implementation in `static/css/personaverse-zerofour.css`.
- [x] accessibility basics (`alt`, focus states)
  Evidence: image `alt` in people/profile templates; focus-visible styles in CSS.

## 3) Users, roles, forms
- [x] registration with validation + messages
  Evidence: `accounts/views.py::register`, `accounts/forms.py`, `templates/includes/messages.html`.
- [x] login/logout with CSRF
  Evidence: `CustomLoginView` + POST logout form/link (`templates/base.html`) + CSRF tokens in auth forms.
- [x] profile view/edit
  Evidence: `accounts/views.py::profile/profile_edit`, `templates/accounts/profile*.html`.
- [x] 3 role levels (anonymous/user/staff)
  Evidence: role rules in `api/views.py`, `moderation/views.py`, `dashboard/views.py`, auth decorators/mixins.
- [x] password change/reset pages
  Evidence: routes in `accounts/urls.py` for change/reset flow and matching templates.
- [x] anti-bruteforce login limit (cache-based)
  Evidence: rate-limit logic in `accounts/views.py` + settings `LOGIN_MAX_ATTEMPTS/LOGIN_LOCKOUT_SECONDS`.
- [x] pagination with filter persistence
  Evidence: `threads/views.py` + `templates/includes/pagination.html` preserving filter query params.

## 4) ORM models and logic
- [x] 15 domain models
  List: `UserProfile`, `LoginAudit`, `Person`, `Thread`, `Comment`, `Vote`, `Report`, `Tag`, `ThreadTag`, `Bookmark`, `Rating`, `Follow`, `Notification`, `Attachment`, `ViewEvent`.
- [x] FK and M2M relations
  Evidence: `Thread.person` (FK), `Thread.tags` through `ThreadTag` (M2M), `Bookmark(user, thread)`, `Rating(user, thread)`.
- [x] slug uniqueness for friendly URLs
  Evidence: unique slug logic in `threads/models.py`, `people/models.py`, `engagement/models.py`.
- [x] indexes/order_by usage
  Evidence: `Meta.indexes` and `Meta.ordering` across `threads`, `comments`, `engagement`, `moderation`.
- [x] select_related/annotate usage
  Evidence: `threads/views.py`, `core/views.py`, `api/views.py`, `dashboard/views.py`.
- [x] filters/search/sorting
  Evidence: `q`, `person`, `ordering`, `created_after`, `score_min` in `threads/views.py` and `api/views.py`.
- [x] migrations tracked in repository
  Count: migration files are present for active apps (`accounts`, `people`, `threads`, `comments`, `votes`, `moderation`, `engagement`, etc.).
- [x] seed command for test data
  Evidence: `threads/management/commands/seed_personaverse.py`.
- [x] model-level validators (rating/file limits)
  Evidence: `core/validators.py`, rating validators in `engagement/models.py` and `reviews/models.py`.

## 5) Django templates
- [x] template inheritance and blocks
  Evidence: `extends 'base.html'`, common blocks (`title`, `content`, `scripts`, `styles`).
- [x] includes for reusable components
  Evidence: `templates/includes/messages.html`, `pagination.html`, `breadcrumbs.html`, `form_fields.html`.
- [x] loops/empty handling
  Evidence: `{% for %}` + `{% empty %}` used in list/detail templates.
- [x] list/detail/filter pages
  Evidence: `threads/thread_list.html`, `threads/thread_detail.html`, `people/person_list.html`, `search/search_page.html`.
- [x] breadcrumbs
  Evidence: `templates/includes/breadcrumbs.html` used in core/profile/moderation/dashboard/threads pages.
- [x] custom template filter (`rating_badge`)
  Evidence: `core/templatetags/core_extras.py`.
- [x] no unnecessary unsafe rendering
  Evidence: no required unsafe rendering paths in active templates.

## 6) Django admin
- [x] models registered
  Evidence: admin registrations in active app admin modules.
- [x] list/search/filter for multiple models
  Evidence: configured in `threads/admin.py`, `engagement/admin.py`, `people/admin.py`, `comments/admin.py`, `accounts/admin.py`, `moderation/admin.py`.
- [x] inline editing examples
  Evidence: inline classes in `threads/admin.py` and `movies/admin.py`.
- [x] prepopulated/readonly fields
  Evidence: `prepopulated_fields`/`readonly_fields` in `threads/admin.py`, `engagement/admin.py`, `movies/admin.py`, `people/admin.py`.
- [x] admin actions and fieldsets
  Evidence: actions + fieldsets in `threads/admin.py`, `movies/admin.py`, `engagement/admin.py`.

## 7) Static and media
- [x] `MEDIA_ROOT` / `MEDIA_URL`
  Evidence: configured in `cineverse/settings.py`.
- [x] file extension + size validation
  Evidence: `core/validators.py` + model file/image validators.
- [x] placeholder support for missing images
  Evidence: placeholder usage in `templates/accounts/profile.html` and people templates.
- [x] collectstatic command in deployment config
  Evidence: `startCommand` in `render.yaml` includes `python manage.py collectstatic --noinput`.
- [x] favicon/fonts/icons from static
  Evidence: favicon and template assets loaded via static in `templates/base.html`.

## 8) API
- [x] 5+ endpoints
  Evidence: `api/urls.py` -> `persons`, `threads`, `thread_detail`, `comments`, `votes`, `bookmarks`, `ratings`, `reports` (8 total).
- [x] 5 filters on thread list
  List: `q`, `person`, `ordering`, `created_after`, `score_min` (`api/views.py`).
- [x] protected write methods
  Evidence: POST endpoints require auth; thread update/delete requires staff in `api/views.py`.
- [x] unified error response shape
  Evidence: `api/exceptions.py::unified_exception_handler`.
- [x] README API examples added
  Evidence: API examples section in `README.md`.

## 10) Additional features
- [x] bookmarks
  Evidence: `engagement/views.py` (`bookmark_list`, `bookmark_toggle`) + API endpoint.
- [x] ratings 1..5 with average
  Evidence: `engagement/views.py::rating_set`, model validators, average rendering in thread detail.
- [x] live search/autocomplete (AJAX)
  Evidence: `search/views.py::live_search` + frontend logic in `static/js/app.js`.
- [x] theme switch + localStorage
  Evidence: theme pickers in `templates/base.html` + persistence logic in `static/js/app.js`.

## Excluded from this file (deployment phase)
- [ ] domain + hosting
- [ ] public HTTPS proof
- [ ] production DB proof
- [ ] production smoke report completion
