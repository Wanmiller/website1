# Submission Report Template

## Project
- Name: CineVerse
- Domain: https://website1-uoa2.onrender.com
- Render URL: https://website1-uoa2.onrender.com
- Verification date/time (UTC): 2026-02-20 20:09

## Team
- Individual project
- Role: Full-stack developer

## Implemented requirements
- 10 apps: done
- 15+ models + relations: done
- 15+ UI pages: done
- Auth/roles/forms/CRUD: done
- API endpoints + filters + protected methods: done
- Admin customizations: done
- Deploy with domain + SSL: pass (onrender domain)

## Smoke results
- Home `/`: pass
- Movies list `/movies/`: pass
- Movie detail `/movies/<slug>/`: pending manual seed/data check
- About `/about/`: pass
- API `/api/v1/movies/`: pass
- API `/api/v1/search/`: pass
- Auth flow: pending manual check
- Staff permissions: pending manual check
- Static/media: static pass, media pending

## Operations
- Logs access: Render dashboard logs
- Restart method: Render manual restart
- Backup method: pg_dump via scripts in `scripts/`
- Restore test: pending manual check

## Evidence
- Screenshot list:
  - home
  - catalog
  - detail
  - profile
  - admin
  - HTTPS certificate/domain
