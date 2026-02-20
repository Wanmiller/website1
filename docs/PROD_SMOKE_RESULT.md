# Production Smoke Result

Run command below to generate/update this report:

```bash
python scripts/prod_smoke_check.py --base-url https://<your-domain> --http-url http://<your-domain>
```

This file will contain automated checks for:
- public pages
- API endpoints
- static file delivery
- HTTP -> HTTPS check

Manual checks must still be completed for:
- auth flow
- staff permissions on write endpoints
- media upload/display
- browser SSL lock
