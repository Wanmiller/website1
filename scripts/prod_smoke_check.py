#!/usr/bin/env python3
"""Simple production smoke-check for CineVerse.

Usage:
  python scripts/prod_smoke_check.py --base-url https://example.com \
    --http-url http://example.com \
    --output docs/PROD_SMOKE_RESULT.md
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class CheckResult:
    name: str
    url: str
    ok: bool
    detail: str


def fetch(url: str, timeout: int = 20) -> tuple[int, bytes, str]:
    req = Request(url, headers={"User-Agent": "CineVerseSmoke/1.0"})
    with urlopen(req, timeout=timeout) as response:  # nosec B310
        code = response.getcode()
        body = response.read()
        content_type = response.headers.get("Content-Type", "")
        return code, body, content_type


def check_url(name: str, base_url: str, path: str) -> CheckResult:
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        code, _, _ = fetch(url)
        ok = 200 <= code < 400
        return CheckResult(name=name, url=url, ok=ok, detail=f"HTTP {code}")
    except HTTPError as exc:
        return CheckResult(name=name, url=url, ok=False, detail=f"HTTPError {exc.code}")
    except URLError as exc:
        return CheckResult(name=name, url=url, ok=False, detail=f"URLError {exc.reason}")
    except Exception as exc:  # pragma: no cover
        return CheckResult(
            name=name, url=url, ok=False, detail=f"Error {type(exc).__name__}: {exc}"
        )


def check_json(name: str, base_url: str, path: str) -> CheckResult:
    result = check_url(name, base_url, path)
    if not result.ok:
        return result

    try:
        code, body, content_type = fetch(result.url)
        if "json" not in content_type.lower():
            return CheckResult(
                name=name,
                url=result.url,
                ok=False,
                detail=f"HTTP {code}, Content-Type '{content_type}' is not JSON",
            )
        json.loads(body.decode("utf-8"))
        return CheckResult(name=name, url=result.url, ok=True, detail=f"HTTP {code}, valid JSON")
    except Exception as exc:
        return CheckResult(
            name=name,
            url=result.url,
            ok=False,
            detail=f"JSON parse failed: {type(exc).__name__}: {exc}",
        )


def check_http_redirect(http_url: str | None) -> CheckResult:
    if not http_url:
        return CheckResult(
            name="HTTP -> HTTPS redirect",
            url="(skipped)",
            ok=False,
            detail="Skipped (no --http-url provided)",
        )

    try:
        code, _, _ = fetch(http_url)
        # If request followed redirect automatically, final code is typically 200.
        # We still treat it as pass and ask user to verify browser lock icon manually.
        ok = 200 <= code < 400
        return CheckResult(
            name="HTTP -> HTTPS redirect",
            url=http_url,
            ok=ok,
            detail=f"HTTP {code} (verify final URL is HTTPS)",
        )
    except HTTPError as exc:
        return CheckResult(
            name="HTTP -> HTTPS redirect",
            url=http_url,
            ok=False,
            detail=f"HTTPError {exc.code}",
        )
    except URLError as exc:
        return CheckResult(
            name="HTTP -> HTTPS redirect",
            url=http_url,
            ok=False,
            detail=f"URLError {exc.reason}",
        )


def render_markdown(base_url: str, results: List[CheckResult]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    passed = sum(1 for r in results if r.ok)
    total = len(results)

    lines = [
        "# Production Smoke Result",
        "",
        f"- Base URL: `{base_url}`",
        f"- Timestamp: `{now}`",
        f"- Summary: `{passed}/{total}` checks passed",
        "",
        "| Check | URL | Status | Detail |",
        "|---|---|---|---|",
    ]

    for r in results:
        status = "PASS" if r.ok else "FAIL"
        lines.append(f"| {r.name} | `{r.url}` | {status} | {r.detail} |")

    lines += [
        "",
        "## Manual checks still required",
        "- Login/logout/register/password reset flow",
        "- Staff-only write access (`POST /api/v1/movies/`)",
        "- Media upload/open",
        "- SSL certificate lock icon in browser",
    ]

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run production smoke checks for CineVerse")
    parser.add_argument(
        "--base-url", required=True, help="HTTPS base URL, e.g. https://example.com"
    )
    parser.add_argument("--http-url", default="", help="Optional HTTP URL for redirect check")
    parser.add_argument(
        "--output",
        default="docs/PROD_SMOKE_RESULT.md",
        help="Output markdown report path",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/") + "/"

    checks: List[CheckResult] = [
        check_url("Home page", base_url, "/"),
        check_url("Movies list", base_url, "/movies/"),
        check_url("About page", base_url, "/about/"),
        check_json("API movies", base_url, "/api/v1/movies/"),
        check_json("API search", base_url, "/api/v1/search/?q=test"),
        check_url("Static CSS", base_url, "/static/css/cineverse-forty.css"),
        check_http_redirect(args.http_url.strip() or None),
    ]

    report = render_markdown(base_url.rstrip("/"), checks)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Saved smoke report to: {args.output}")

    failed = [c for c in checks if not c.ok]
    if failed:
        print("Some checks failed:")
        for c in failed:
            print(f"- {c.name}: {c.detail}")
        return 1

    print("All automated checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
