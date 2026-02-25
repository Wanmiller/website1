# Production Smoke Result

- Base URL: `https://<your-service>.onrender.com`
- Timestamp: `YYYY-MM-DD HH:MM UTC`
- Summary: `0/0` checks passed

Run and overwrite this file with real data:

```bash
python scripts/prod_smoke_check.py --base-url https://<your-service>.onrender.com --http-url http://<your-service>.onrender.com
```

Expected checks include:
- `/`
- `/threads/`
- `/people/`
- `/search/`
- `/about/`
- `/api/v1/threads/`
- `/api/v1/persons/?q=test`
- static CSS path `/static/css/personaverse-zerofour.css`
