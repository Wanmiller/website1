# Production Smoke Result

- Base URL: `https://website1-uoa2.onrender.com`
- Timestamp: `2026-02-20 20:09 UTC`
- Summary: `7/7` checks passed

| Check | URL | Status | Detail |
|---|---|---|---|
| Home page | `https://website1-uoa2.onrender.com/` | PASS | HTTP 200 |
| Movies list | `https://website1-uoa2.onrender.com/movies/` | PASS | HTTP 200 |
| About page | `https://website1-uoa2.onrender.com/about/` | PASS | HTTP 200 |
| API movies | `https://website1-uoa2.onrender.com/api/v1/movies/` | PASS | HTTP 200, valid JSON |
| API search | `https://website1-uoa2.onrender.com/api/v1/search/?q=test` | PASS | HTTP 200, valid JSON |
| Static CSS | `https://website1-uoa2.onrender.com/static/css/cineverse-forty.css` | PASS | HTTP 200 |
| HTTP -> HTTPS redirect | `http://website1-uoa2.onrender.com` | PASS | HTTP 200 (verify final URL is HTTPS) |

## Manual checks still required
- Login/logout/register/password reset flow
- Staff-only write access (`POST /api/v1/movies/`)
- Media upload/open
- SSL certificate lock icon in browser
