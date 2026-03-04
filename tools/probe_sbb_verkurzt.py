#!/usr/bin/env python3
"""Kleine Sondierung: sucht in SBB-Ergebnissen nach "verkürzt geführt".

Hinweis:
- Das Script ist als Startpunkt gedacht; Selektoren müssen ggf. angepasst werden.
- Ausführung lokal (nicht in allen CI/Proxy-Umgebungen möglich).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SBB Probe auf 'verkürzt geführt'-Hinweise")
    parser.add_argument("--url", required=True, help="Fahrplan-URL mit vordefinierter Suche")
    parser.add_argument("--out", default="artifacts/sbb_probe.json", help="Zieldatei JSON")
    parser.add_argument("--headless", action="store_true", help="Browser headless starten")
    return parser.parse_args()


def _load_playwright_sync() -> object:
    """Importiert Playwright erst zur Laufzeit für bessere Fehlermeldungen."""
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        print(
            "Fehler: Das Paket 'playwright' fehlt.\n"
            "Bitte so installieren:\n"
            "  1) python3 -m pip install playwright\n"
            "  2) python3 -m playwright install chromium\n",
            file=sys.stderr,
        )
        raise SystemExit(2)

    return sync_playwright


def main() -> None:
    args = parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sync_playwright = _load_playwright_sync()

    findings: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page()
        page.goto(args.url, wait_until="networkidle", timeout=60_000)

        page_text = page.inner_text("body")
        needle = "verkürzt geführt"
        match = needle in page_text.lower()

        findings.append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "url": page.url,
                "needle": needle,
                "match": match,
            }
        )

        if match:
            page.screenshot(path=str(out_path.with_suffix(".png")), full_page=True)

        browser.close()

    out_path.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
