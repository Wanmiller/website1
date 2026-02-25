#!/usr/bin/env python3
"""Simple production smoke-check for PersonaVerse.

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


def fetch(url: str, timeout: int = 20) -> tuple[int, bytes, str, str]:
    req = Request(url, headers={"User-Agent": "PersonaVerseSmoke/1.0"})
    with urlopen(req, timeout=timeout) as response:  # nosec B310
        code = response.getcode()
        body = response.read()
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        return code, body, content_type, final_url


def check_url(name: str, base_url: str, path: str) -> CheckResult:
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        code, _, _, _ = fetch(url)
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
        code, body, content_type, _ = fetch(result.url)
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
        code, _, _, final_url = fetch(http_url)
        ok = final_url.startswith("https://")
        return CheckResult(
            name="HTTP -> HTTPS redirect",
            url=http_url,
            ok=ok,
            detail=f"HTTP {code}, final URL: {final_url}",
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

    for result in results:
        status = "PASS" if result.ok else "FAIL"
        lines.append(f"| {result.name} | `{result.url}` | {status} | {result.detail} |")

    lines += [
        "",
        "## Manual checks still required",
        "- Login/logout/register/password reset flow",
        "- Anonymous/user/staff permission matrix",
        "- Bookmark + rating flows",
        "- Media upload/open",
        "- SSL certificate lock icon in browser",
    ]

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run production smoke checks for PersonaVerse")
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
        check_url("Threads list", base_url, "/threads/"),
        check_url("People list", base_url, "/people/"),
        check_url("Search page", base_url, "/search/"),
        check_url("About page", base_url, "/about/"),
        check_json("API threads", base_url, "/api/v1/threads/"),
        check_json("API persons", base_url, "/api/v1/persons/?q=test"),
        check_url("Static CSS", base_url, "/static/css/personaverse-zerofour.css"),
        check_http_redirect(args.http_url.strip() or None),
    ]

    report = render_markdown(base_url.rstrip("/"), checks)
    with open(args.output, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Saved smoke report to: {args.output}")

    failed = [check for check in checks if not check.ok]
    if failed:
        print("Some checks failed:")
        for check in failed:
            print(f"- {check.name}: {check.detail}")
        return 1

    print("All automated checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
