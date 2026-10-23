#!/usr/bin/env python3
"""
Renders code-stats.svg (dark) and code-stats-light.svg from data/code-stats.json:
- Left: donut of language share across all public repos (bytes of code, per GitHub linguist)
- Right: relative size of each project, each bar split by the same language colors
Shares and proportions only; no byte or line units on display.
Measured data only, no self-rated skill levels. Run fetch_code_stats.py first.
"""

import html
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

from theme import FONT, GROUP_ORDER, MONO_ADV, OTHER, THEMES, group_colors, grouped, tech_label, window

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "code-stats.json")
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..")

W, H = 1000, 500  # shown at ~800px wide, so canvas type is >= 15

DISPLAY = {"Nyaya-Sahayak-Core": "Nyaya-Sahayak", "multi-ocular-disease-detection": "Multi-Ocular"}


def esc(s):
    return html.escape(s, quote=False)


def arc(cx, cy, r_out, r_in, a0, a1):
    """Donut segment path from angle a0 to a1 (radians, 0 = 12 o'clock, clockwise)."""
    def pt(r, a):
        return cx + r * math.sin(a), cy - r * math.cos(a)
    large = 1 if a1 - a0 > math.pi else 0
    x0, y0 = pt(r_out, a0)
    x1, y1 = pt(r_out, a1)
    x2, y2 = pt(r_in, a1)
    x3, y3 = pt(r_in, a0)
    return (f"M{x0:.2f} {y0:.2f} A{r_out} {r_out} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r_in} {r_in} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


def build(t, data):
    colors = group_colors(t)
    order = GROUP_ORDER

    totals = {g: 0 for g in order}
    projects = []
    for proj in data["projects"]:
        g = grouped(proj["languages"])
        for k, v in g.items():
            totals[k] += v
        projects.append((DISPLAY.get(proj["repo"], proj["repo"]), g, sum(g.values())))
    projects.sort(key=lambda p: -p[2])
    grand = sum(totals.values())
    n_langs = len({lang for proj in data["projects"] for lang in proj["languages"]})

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    p.append(window(t, W, H, "krishna@github: ~$ ./code-stats.sh"))

    def heading(x, text):
        p.append(f'<text x="{x}" y="76" font-size="16" font-weight="700" fill="{t["muted"]}" letter-spacing="2">{text}</text>')

    # Left: language donut + legend
    heading(32, "LANGUAGES")
    cx, cy, r_out, r_in = 142, 270, 110, 72
    a = 0.0
    for g in order:
        if not totals[g]:
            continue
        span = totals[g] / grand * 2 * math.pi
        pct = totals[g] / grand * 100
        p.append(
            f'<path d="{arc(cx, cy, r_out, r_in, a, a + span)}" fill="{colors[g]}" '
            f'stroke="{t["bg2"]}" stroke-width="2"><title>{esc(g)}: {pct:.0f}%</title></path>'
        )
        a += span
    p.append(f'<text x="{cx}" y="{cy - 4}" font-size="46" font-weight="700" fill="{t["head"]}" text-anchor="middle">{len(projects)}</text>')
    p.append(f'<text x="{cx}" y="{cy + 20}" font-size="17" fill="{t["muted"]}" text-anchor="middle">projects</text>')
    p.append(f'<text x="{cx}" y="{cy + 40}" font-size="15" fill="{t["muted"]}" text-anchor="middle">{n_langs} languages</text>')

    ly = 172
    for g in order:
        if not totals[g]:
            continue
        pct = totals[g] / grand * 100
        p.append(f'<rect x="280" y="{ly - 13}" width="14" height="14" rx="3" fill="{colors[g]}"/>')
        p.append(tech_label(g, 304, ly, 18, t["fg"])[0])
        p.append(f'<text x="505" y="{ly}" font-size="18" font-weight="700" fill="{t["fg"]}" text-anchor="end">{pct:.0f}%</text>')
        ly += 40

    p.append(f'<line x1="530" y1="56" x2="530" y2="{H - 56}" stroke="{t["frame"]}"/>')

    # Right: bytes per project, stacked by language group
    heading(560, "CODE PER PROJECT")
    bar_x, bar_max, bar_h = 730, 238, 18
    biggest = projects[0][2]
    ry = 112
    for name, g, total in projects:
        # name, with "mostly <logo> Lang" underneath; bar to the right
        p.append(f'<text x="560" y="{ry + 14}" font-size="18" fill="{t["fg"]}">{esc(name)}</text>')
        x = bar_x
        width = bar_max * total / biggest
        for k in order:
            if not g[k]:
                continue
            seg = width * g[k] / total
            if seg < 1:
                continue
            p.append(
                f'<rect x="{x:.1f}" y="{ry}" width="{max(seg - 2, 1):.1f}" height="{bar_h}" rx="3" fill="{colors[k]}">'
                f'<title>{esc(name)} · {esc(k)}: {g[k] / total * 100:.0f}% of project</title></rect>'
            )
            x += seg
        top = max((k for k in order if k != OTHER), key=lambda k: g[k])
        p.append(f'<text x="560" y="{ry + 36}" font-size="15" fill="{t["muted"]}">mostly</text>')
        p.append(tech_label(top, 560 + 7 * 15 * MONO_ADV, ry + 36, 15, t["muted"])[0])
        ry += 56

    p.append(
        f'<text x="32" y="{H - 22}" font-size="15" fill="{t["muted"]}">share of code per GitHub linguist · '
        f'{len(projects)} public repos · as of {esc(data["fetched"])}</text>'
    )
    p.append("</svg>")
    return "".join(p)


with open(DATA) as f:
    data = json.load(f)

for theme in THEMES:
    svg = build(theme, data)
    ET.fromstring(svg)
    out = os.path.join(OUT_DIR, f"code-stats{theme['suffix']}.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Generated {out} ({len(svg)} bytes)")
