#!/usr/bin/env python3
"""Build public/olympiads/olympiads.json from the YAML source of truth.

Source of truth:
  public/olympiads/olympiads.yml

Output (consumed by olympiads/index.md client-side JS and by the iOS app):
  public/olympiads/olympiads.json

Output shape:
    {"items": [ {id, type, subject, date, sort_key, name, highlighted,
                 subjects?[], invited?, competitive?}, ... ]}

Run this after editing the YAML, then commit both the YAML and the JSON.
There is no CI validation — the editor is responsible for remembering to rebuild.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT = ROOT / "public" / "olympiads"

SUBJECTS = {"Mathematics", "Computing", "Physics", "Chemistry", "Biology", "Astronomy"}
TYPES = {"olympiad", "textbook"}
MONTHS = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12",
}


def sort_key(date: str) -> str:
    """'November 2025' -> '2025-11'."""
    try:
        month, year = date.split(" ")
        return f"{year}-{MONTHS[month]}"
    except (ValueError, KeyError) as e:
        raise ValueError(f"invalid date {date!r}: expected 'Month YYYY'") from e


def build_activities() -> list[dict]:
    data = yaml.safe_load((CONTENT / "olympiads.yml").read_text())
    if not isinstance(data, list):
        raise ValueError("olympiads.yml must be a YAML list")
    items = []
    for i, e in enumerate(data):
        # Validate required fields
        for field in ("type", "subject", "date", "name"):
            if field not in e:
                raise ValueError(f"entry[{i}] missing required field {field!r}: {e}")
        if e["type"] not in TYPES:
            raise ValueError(f"entry[{i}] invalid type {e['type']!r}")
        if e["subject"] not in SUBJECTS:
            raise ValueError(f"entry[{i}] invalid subject {e['subject']!r}")
        if "subjects" in e:
            for s in e["subjects"]:
                if s not in SUBJECTS:
                    raise ValueError(f"entry[{i}] invalid subject {s!r} in subjects list")

        item: dict = {
            "id": i + 1,
            "type": e["type"],
            "subject": e["subject"],
            "date": e["date"],
            "sort_key": sort_key(e["date"]),
            "name": e["name"],
            "highlighted": 1 if e.get("highlighted") else 0,
        }
        if e.get("subjects"):
            item["subjects"] = e["subjects"]
        if e.get("invited"):
            item["invited"] = 1
        if e.get("competitive"):
            item["competitive"] = 1
        items.append(item)
    return items


def write_json(path: Path, items: list[dict]) -> None:
    payload = {"items": items}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {path.relative_to(ROOT)} ({len(items)} items)")


def main() -> int:
    try:
        activities = build_activities()
    except ValueError as e:
        print(f"validation error: {e}", file=sys.stderr)
        return 1
    CONTENT.mkdir(exist_ok=True)
    write_json(CONTENT / "olympiads.json", activities)
    return 0


if __name__ == "__main__":
    sys.exit(main())
