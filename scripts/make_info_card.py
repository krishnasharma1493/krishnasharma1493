#!/usr/bin/env python3
"""
Generates the Neofetch Info Card SVG (info-card.svg).
Features:
- School & "works on" lines
- Technology domain donut with animated btop-style meters (the meters double as its legend)
- Hackathon honors log
- Blinking prompt cursor in the status bar
Pairs side-by-side with krishna-ascii.svg inside an 840x880 canvas. GitHub shows the card at
roughly 48% of its size, so every text is >= 22px here (about 11px on screen); the script
stops if a line would run past the card edge.
"""

import html
import math
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 840
CANVAS_H = 880
PAD = 32
TITLEBAR_H = 30
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
TITLE_TEXT = "#7d8590"

# Curated Nord aesthetic flat colors
COLOR_AI = "#B48EAD"       # Nord Purple / Magenta
COLOR_BACKEND = "#81A1C1"  # Nord Frost Blue
COLOR_CLOUD = "#A3BE8C"    # Nord Aurora Green
COLOR_HARDWARE = "#D08770" # Nord Aurora Orange
COLOR_GIS = "#88C0D0"      # Nord Frost Teal / Cyan

svg_parts = []
svg_parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">'
)

svg_parts.append("""
<style>
  .fade-item {
    opacity: 0;
    animation: fadeIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes barGrow {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }
  .bar-anim {
    transform-origin: left;
    animation: barGrow 0.75s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .fade-item { opacity: 1 !important; transform: none !important; animation: none !important; }
    .bar-anim { transform: none !important; animation: none !important; }
  }
</style>
""")

# Defs (NO GRADIENTS for charts, simple flat solid colors throughout)
svg_parts.append(f"""
<defs>
  <linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG2}"/>
    <stop offset="1" stop-color="{BG}"/>
  </linearGradient>
</defs>
""")

# Card Frame
svg_parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#card-bg)"/>')
svg_parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')

# Top Titlebar
svg_parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    svg_parts.append(f'<circle cx="{20 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
svg_parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4.5}" fill="{TITLE_TEXT}" font-size="16" text-anchor="middle">krishna@github: ~$ neofetch --metrics</text>')

MONO_ADV = 0.6  # monospace glyph advance, in em


def fits(text, x, size, what):
    if x + len(text) * size * MONO_ADV > CANVAS_W - PAD:
        sys.exit(f"info card: {what} '{text}' runs past the card edge; shorten it")


y_cursor = 84

# Header: Host title
host = "Krishna Sharma"
fits(host, PAD, 36, "header")
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.08s;">
  <text x="{PAD}" y="{y_cursor}" font-size="36" font-weight="700" fill="#f0f6fc">{host}</text>
  <line x1="{PAD}" y1="{y_cursor + 18}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 18}" stroke="{FRAME}" stroke-dasharray="3 3"/>
</g>
""")

# School & focus as neofetch key/value lines
y_cursor += 66
kv_size = 24
key_col = PAD + 10 * kv_size * MONO_ADV
for i, (key, val, col) in enumerate([
    ("school", "University of Delhi · B.Tech CSE AI/ML '29", "#58a6ff"),
    ("works on", "Full-stack AI · GIS · RF signal analysis", "#3fb950"),
]):
    fits(val, key_col, kv_size, key)
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {0.18 + i * 0.06:.2f}s;">
      <text x="{PAD}" y="{y_cursor}" font-size="{kv_size}" font-weight="700" fill="{col}">{key}</text>
      <text x="{key_col:.0f}" y="{y_cursor}" font-size="{kv_size}" fill="#c9d1d9">{html.escape(val)}</text>
    </g>
    """)
    y_cursor += 44

# Section Title for Visual Tech Distribution
y_cursor += 18
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.3s;">
  <text x="{PAD}" y="{y_cursor}" font-size="22" font-weight="700" fill="#58a6ff" letter-spacing="0.8">TECHNOLOGY PROFICIENCY MATRIX</text>
  <line x1="{PAD}" y1="{y_cursor + 12}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 12}" stroke="{FRAME}"/>
</g>
""")

# Domains: donut on the left, meters on the right (same colors, so the meters are the legend)
slices = [
    ("AI, RAG & Vision", 35, 0.94, COLOR_AI),
    ("Backend & Distributed", 25, 0.88, COLOR_BACKEND),
    ("Cloud & Containers", 18, 0.82, COLOR_CLOUD),
    ("Edge Hardware & RF", 12, 0.76, COLOR_HARDWARE),
    ("Interactive GIS & Web", 10, 0.86, COLOR_GIS),
]
meter_top = y_cursor + 58
meter_gap = 54
cx = PAD + 112
cy = meter_top + (len(slices) - 1) * meter_gap / 2 + 2
r = 98
stroke_w = 24
circumference = 2 * math.pi * r

svg_parts.append('<g class="fade-item" style="animation-delay: 0.38s;">')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#161b22" stroke-width="{stroke_w}"/>')
accum_offset = 0
segment_gap = 5.0
for label, pct, _, col in slices:
    full_len = (pct / 100.0) * circumference
    dash_len = max(full_len - segment_gap, 1.0)
    gap_len = circumference - dash_len
    angle = (accum_offset / circumference) * 360 - 90 + (segment_gap / 2.0 / circumference) * 360
    svg_parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{stroke_w}" '
        f'stroke-dasharray="{dash_len:.2f} {gap_len:.2f}" transform="rotate({angle:.2f} {cx} {cy})">'
        f'<title>{html.escape(label)}: {pct}%</title></circle>'
    )
    accum_offset += full_len
svg_parts.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="22" fill="#8b949e" font-weight="700" letter-spacing="1.2">STACK</text>')
svg_parts.append(f'<text x="{cx}" y="{cy + 24}" text-anchor="middle" font-size="28" fill="#f0f6fc" font-weight="800">ACTIVE</text>')
svg_parts.append("</g>")

bars_x = cx + r + 46
bar_w = CANVAS_W - PAD - bars_x
for idx, (title, pct, level, col) in enumerate(slices):
    delay = 0.45 + idx * 0.08
    y = meter_top + idx * meter_gap - 14
    fits(title, bars_x, 22, "meter title")
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <text x="{bars_x:.0f}" y="{y}" font-size="22" font-weight="700" fill="{col}">{html.escape(title)}</text>
      <text x="{CANVAS_W - PAD}" y="{y}" font-size="22" font-weight="700" fill="#f0f6fc" text-anchor="end">{round(level * 100)}%</text>
      <rect x="{bars_x:.0f}" y="{y + 9}" width="{bar_w:.0f}" height="14" rx="7" fill="#161b22" stroke="#21262d" stroke-width="1"/>
      <rect class="bar-anim" x="{bars_x:.0f}" y="{y + 9}" width="{bar_w * level:.0f}" height="14" rx="7" fill="{col}" style="animation-delay: {delay + 0.08:.2f}s;"/>
    </g>
    """)

y_cursor = max(cy + r + stroke_w / 2, meter_top + (len(slices) - 1) * meter_gap + 9) + 40

# Hackathon honors
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.95s;">
  <line x1="{PAD}" y1="{y_cursor}" x2="{CANVAS_W - PAD}" y2="{y_cursor}" stroke="{FRAME}"/>
  <text x="{PAD}" y="{y_cursor + 34}" font-size="22" font-weight="700" fill="#d29922" letter-spacing="0.6">HACKATHON HONORS &amp; RECOGNITION</text>
</g>
""")
y_cursor += 76

achievements = [
    ("Finalist", "Nari Kavach 2026", "#A3BE8C"),
    ("Top 15", "Hack-4-Viksit Bharat", "#81A1C1"),
    ("SIH 2026", "IGNISSENSE", "#B48EAD"),
    ("SIH 2025", "Authenticity Validator", "#88C0D0"),
]
title_x = PAD + 12 * 24 * MONO_ADV
for idx, (badge, title, col) in enumerate(achievements):
    delay = 1.05 + idx * 0.08
    fits(title, title_x, 24, "honor")
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <text x="{PAD}" y="{y_cursor}" font-size="24" font-weight="700" fill="{col}">[{html.escape(badge)}]</text>
      <text x="{title_x:.0f}" y="{y_cursor}" font-size="24" font-weight="600" fill="#f0f6fc">{html.escape(title)}</text>
    </g>
    """)
    y_cursor += 38

if y_cursor > CANVAS_H - 60:
    sys.exit(f"info card: content ends at y={y_cursor}, overlapping the status bar")

# Status bar
status_line_y = CANVAS_H - 48
status_y = status_line_y + 32
svg_parts.append(f'<line x1="0" y1="{status_line_y}" x2="{CANVAS_W}" y2="{status_line_y}" stroke="{FRAME}"/>')
status_prompt_plain = "krishna@github:~$ status OPEN TO WORK & COLLABORATION "
fits(status_prompt_plain, PAD - 12, 22, "status")
svg_parts.append(
    f'<text x="{PAD - 12}" y="{status_y}" fill="{TITLE_TEXT}" font-size="22">'
    f'krishna@github:~$ status <tspan fill="#3fb950" font-weight="600">OPEN TO WORK &amp; COLLABORATION</tspan></text>'
)
cursor_x = PAD - 12 + len(status_prompt_plain) * 22 * MONO_ADV
svg_parts.append(
    f'<rect x="{cursor_x:.1f}" y="{status_y - 18:.1f}" width="12" height="22" fill="#3fb950">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
)

svg_parts.append("</svg>")

svg_code = "".join(svg_parts)
with open(OUT, "w") as f:
    f.write(svg_code)

try:
    ET.fromstring(svg_code)
    print(f"Generated {OUT} ({len(svg_code)} bytes; content ends at y={y_cursor:.0f})")
except Exception as e:
    print("XML Error:", e)
