#!/usr/bin/env python3
"""Validate Render blueprint config for PersonaVerse."""

from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_ENV_KEYS = {
    "SECRET_KEY",
    "DEBUG",
    "USE_SQLITE",
    "DATABASE_URL",
    "DB_SSL_REQUIRE",
    "ALLOWED_HOSTS",
    "CSRF_TRUSTED_ORIGINS",
    "SECURE_SSL_REDIRECT",
    "SESSION_COOKIE_SECURE",
    "CSRF_COOKIE_SECURE",
}


def parse_lines(lines: list[str]) -> tuple[bool, bool, bool, set[str]]:
    has_web = False
    has_db = False
    has_start_cmd = False
    env_keys: set[str] = set()

    for i, raw in enumerate(lines):
        line = raw.strip()
        if line == "- type: web":
            has_web = True
        if line.startswith("- name: personaverse-db"):
            has_db = True
        if line.startswith("startCommand:") and "gunicorn cineverse.wsgi:application" in line:
            has_start_cmd = True
        if line.startswith("- key:"):
            key = line.split(":", 1)[1].strip()
            if key:
                env_keys.add(key)

    return has_web, has_db, has_start_cmd, env_keys


def main() -> int:
    path = Path("render.yaml")
    if not path.exists():
        print("FAIL: render.yaml not found")
        return 1

    lines = path.read_text(encoding="utf-8").splitlines()
    has_web, has_db, has_start_cmd, env_keys = parse_lines(lines)

    failed = False

    if not has_web:
        print("FAIL: missing web service declaration (- type: web)")
        failed = True
    else:
        print("PASS: web service declaration found")

    if not has_db:
        print("FAIL: missing database declaration for personaverse-db")
        failed = True
    else:
        print("PASS: database declaration found")

    if not has_start_cmd:
        print("FAIL: startCommand does not include gunicorn cineverse.wsgi:application")
        failed = True
    else:
        print("PASS: startCommand includes gunicorn")

    missing = sorted(REQUIRED_ENV_KEYS - env_keys)
    if missing:
        print("FAIL: missing required env keys:")
        for key in missing:
            print(f"  - {key}")
        failed = True
    else:
        print("PASS: all required env keys present")

    if failed:
        return 1

    print("\nBlueprint validation successful.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
