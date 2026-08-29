from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = [
    ("Role", "M.S. Cybersecurity Student"),
    ("School", "George Washington University"),
    ("Focus", "SOC · Cloud · AI Security"),
    ("Stack", "Python · AWS · Terraform · Docker"),
    ("Tools", "Linux · Wireshark · Git · SQL"),
    ("Build", "Security automation &amp; detection"),
    ("Location", "Arlington, Virginia"),
]
lines = []
for i, (key, value) in enumerate(rows):
    y = 92 + i * 31
    lines.append(f'<g class="line l{i}"><text x="30" y="{y}" class="key">{key}</text><text x="130" y="{y}" class="value">{value}</text></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="330" viewBox="0 0 490 330">
<style>
text {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:14px }}
.title,.value {{ fill:#e6edf3 }} .key {{ fill:#39d353; font-weight:700 }} .muted {{ fill:#8b949e }}
.line {{ opacity:0; transform:translateX(-8px); animation:print .35s ease-out forwards }}
{''.join(f'.l{i}{{animation-delay:{0.25+i*0.13:.2f}s}}' for i in range(len(rows)))}
@keyframes print {{ to {{ opacity:1; transform:translateX(0) }} }}
</style>
<rect width="488" height="328" x="1" y="1" rx="12" fill="#0d1117" stroke="#30363d"/>
<circle cx="22" cy="21" r="5" fill="#ff5f56"/><circle cx="40" cy="21" r="5" fill="#ffbd2e"/><circle cx="58" cy="21" r="5" fill="#27c93f"/>
<text x="245" y="26" text-anchor="middle" class="muted">nithin@github: ~</text>
<text x="30" y="60" class="title" font-weight="700">Nithin A M</text><text x="130" y="60" class="muted">--------------------</text>
{''.join(lines)}
<text x="30" y="313" class="muted">$ status --open-to-work</text><rect x="221" y="301" width="7" height="14" fill="#39d353"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
</svg>'''
(ROOT / "info-card.svg").write_text(svg, encoding="utf-8")
