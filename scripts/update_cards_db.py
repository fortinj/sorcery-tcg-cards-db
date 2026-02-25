#!/usr/bin/env python3
"""
Update Sorcery TCG cards database from the official API.

Fetches card data from https://api.sorcerytcg.com/api/cards and saves it to
data/db/cards.json. Normalizes variant slugs (replaces hyphens with underscores)
for compatibility with the image naming convention used in data/imgs/.

Usage:
    python scripts/update_cards_db.py

Requirements:
    - Python 3.7+
    - requests library (pip install requests) or urllib (stdlib)
"""

import json
import sys
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Configuration
API_URL = "https://api.sorcerytcg.com/api/cards"
DB_PATH = Path("data/db/cards.json")


def fetch_cards():
    """Fetch cards from Sorcery API."""
    if HAS_REQUESTS:
        resp = requests.get(API_URL, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # Fallback to urllib (stdlib)
    import ssl
    import urllib.request
    ctx = ssl.create_default_context()
    req = urllib.request.Request(API_URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode())


def normalize_slugs(cards):
    """
    Convert variant slugs from API format (alp-card_name-b-s) to local format
    (alp_card_name_b_s) for compatibility with image filenames.
    """
    for card in cards:
        for set_data in card.get("sets", []):
            for variant in set_data.get("variants", []):
                slug = variant.get("slug")
                if slug:
                    variant["slug"] = slug.replace("-", "_")
    return cards


def main():
    print("=" * 60)
    print("Sorcery TCG – Update Cards Database")
    print("=" * 60)
    print()

    try:
        print("Fetching cards from API...")
        cards = fetch_cards()
        print(f"  Retrieved {len(cards)} cards")
    except Exception as e:
        print(f"Error fetching API: {e}", file=sys.stderr)
        sys.exit(1)

    print("Normalizing slugs for image compatibility...")
    cards = normalize_slugs(cards)

    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        print(f"  Created directory: {DB_PATH.parent}")

    print(f"Writing to {DB_PATH}...")
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print("Database updated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
