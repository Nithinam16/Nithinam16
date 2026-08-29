from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7
    cells = []
    for index, item in enumerate(days):
        position = index + offset
        week, weekday = divmod(position, 7)
        x, y = 52 + week * 14, 52 + weekday * 14
        level = min(4, int(item.get("level", 0)))
        delay = (week + weekday) * 0.018
        cells.append(
            f'<rect class="day" x="{x}" y="{y}" width="10" height="10" rx="2" '
            f'fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s">'
            f'<title>{html.escape(str(item["date"]))}: {int(item.get("count", 0))} contributions</title></rect>'
        )
    legend = "".join(
        f'<rect x="{704 + i * 14}" y="168" width="10" height="10" rx="2" fill="{color}"/>'
        for i, color in enumerate(PALETTE)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="210" viewBox="0 0 860 210" role="img">
<style>
  text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill:#8b949e }}
  .title {{ fill:#e6edf3; font-size:16px; font-weight:600 }}
  .day {{ opacity:0; transform:translateY(-9px); animation:reveal .32s ease-out forwards }}
  @keyframes reveal {{ to {{ opacity:1; transform:translateY(0) }} }}
</style>
<rect width="858" height="208" x="1" y="1" rx="12" fill="#0d1117" stroke="#30363d"/>
<circle cx="24" cy="22" r="5" fill="#ff5f56"/><circle cx="42" cy="22" r="5" fill="#ffbd2e"/><circle cx="60" cy="22" r="5" fill="#27c93f"/>
<text x="430" y="27" text-anchor="middle" class="title">Nithinam16 — contribution activity</text>
{''.join(cells)}
<text x="52" y="177" font-size="12">{int(payload['total']):,} contributions · current streak {int(payload['current_streak'])} days · longest {int(payload['longest_streak'])} days</text>
<text x="669" y="177" font-size="11">Less</text>{legend}<text x="779" y="177" font-size="11">More</text>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
