from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Nithinam16"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "contributions.json"


def main() -> None:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, headers={"User-Agent": "profile-readme-generator"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tooltips = {
        tip.get("for"): tip.get_text(" ", strip=True)
        for tip in soup.select("tool-tip[for]")
        if tip.get("for")
    }
    values: dict[str, dict[str, int | str]] = {}
    for cell in soup.select("td[data-date]"):
        day = cell.get("data-date")
        if not day:
            continue
        level = int(cell.get("data-level", "0"))
        count = 0
        label = cell.get("aria-label", "") or tooltips.get(cell.get("id"), "")
        if label:
            first = label.split()[0].replace(",", "")
            if first.isdigit():
                count = int(first)
        values[day] = {"date": day, "count": count, "level": level}

    end = date.today()
    start = end - timedelta(days=370)
    days = []
    cursor = start
    while cursor <= end:
        key = cursor.isoformat()
        days.append(values.get(key, {"date": key, "count": 0, "level": 0}))
        cursor += timedelta(days=1)

    streak = longest = running = 0
    for item in days:
        if int(item["count"]) > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    for item in reversed(days):
        if int(item["count"]) > 0:
            streak += 1
        else:
            break

    payload = {
        "username": USERNAME,
        "days": days,
        "total": sum(int(item["count"]) for item in days),
        "current_streak": streak,
        "longest_streak": longest,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(days)} days to {OUTPUT}")


if __name__ == "__main__":
    main()
