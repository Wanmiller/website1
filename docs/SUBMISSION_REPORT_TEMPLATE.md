# Submission Report Template

## Project
- Name: PersonaVerse
- Domain: https://website1-uoa2.onrender.com
- Render URL: https://website1-uoa2.onrender.com
- Verification timestamp (UTC): YYYY-MM-DD HH:MM
- Verified by: <name / role>

## Compliance Snapshot
- Pass count: 10
- Partial count: 4
- Fail count: 0
- Source of truth: `README.md` -> `PDF Compliance Matrix (Pass/Partial/Fail)`

## Team
- Individual project
- Role: Full-stack developer

## Implemented requirements
- Persona domain (people + community threads): done
- Thread/comment/vote/report workflow: done
- 15+ UI pages and adaptive UX: done
- Localization EN/RU/KK (default KK): done
- Auth/roles/forms/permissions: done
- API endpoints + protected methods: done
- Staff moderation panel: done
- Deploy with HTTPS: pass (onrender domain)

## Smoke results
- Feed `/`: pass
- People list `/people/`: pass
- Person detail `/people/<slug>/`: pass
- Threads `/threads/`: pass
- Thread detail `/threads/<slug>/`: pass
- Moderation `/moderation/` staff-only: pending manual check
- API `/api/v1/persons/`: pass
- API `/api/v1/threads/`: pass
- API `/api/v1/comments/` POST auth: pending manual check
- API `/api/v1/votes/` POST auth: pending manual check
- Auth flow: pending manual check
- Localization switch (EN/RU/KK + cookie persistence): pass
- Static/media: static pass, media pending

## Operations
- Logs access: Render dashboard logs
- Restart method: Render manual restart
- Backup method: pg_dump via scripts in `scripts/`
- Restore test: pending manual check

## Evidence
- Screenshot list:
  - feed
  - people list
  - thread detail
  - profile
  - moderation panel
  - HTTPS certificate/domain
