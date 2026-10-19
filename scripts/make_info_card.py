#!/usr/bin/env python3
"""
Generates the Neofetch Info Card SVG (info-card.svg).
Features:
- Academic Base & Core Architecture Summary
- Dynamic Technology Domain Allocation Donut Chart (Solid curated premium colors, NO gradients)
- Animated System Monitor (btop/htop style) Resource Proficiency Meters with enlarged typography
- Hackathon Honors & Awards Log
- Iconic Neofetch 8-color swatches & blinking prompt cursor
Pairs side-by-side with krishna-ascii.svg inside an 840x880 canvas.
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

# Curated premium aesthetic flat colors - NO GRADIENTS
COLOR_AI = "#a371f7"       # Electric Violet
COLOR_BACKEND = "#388bfd"  # Cyber Cobalt Blue
COLOR_CLOUD = "#3fb950"    # Emerald Mint
COLOR_HARDWARE = "#f0883e" # Amber Flame
COLOR_GIS = "#39c5cf"      # Bright Teal / Cyan

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
svg_parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4.5}" fill="{TITLE_TEXT}" font-size="12.5" text-anchor="middle">krishna@github: ~$ neofetch --metrics</text>')

y_cursor = 64

# Header: Host title
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.08s;">
  <text x="{PAD}" y="{y_cursor}" font-size="21" font-weight="700" fill="#58a6ff">krishna<tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">du-fot-terminal</tspan></text>
  <line x1="{PAD}" y1="{y_cursor + 11}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 11}" stroke="{FRAME}" stroke-dasharray="3 3"/>
</g>
""")

y_cursor += 36

# Highlight boxes (larger height and larger typography)
box_h = 74
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.18s;">
  <rect x="{PAD}" y="{y_cursor}" width="370" height="{box_h}" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 16}" y="{y_cursor + 25}" font-size="11.5" fill="#8b949e" font-weight="700" letter-spacing="0.6">ACADEMIC BASE</text>
  <text x="{PAD + 16}" y="{y_cursor + 46}" font-size="14.5" fill="#58a6ff" font-weight="700">University of Delhi · FoT</text>
  <text x="{PAD + 16}" y="{y_cursor + 63}" font-size="12.5" fill="#c9d1d9">B.Tech CSE (AI/ML) · Class of 2029</text>

  <rect x="{PAD + 394}" y="{y_cursor}" width="382" height="{box_h}" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 410}" y="{y_cursor + 25}" font-size="11.5" fill="#8b949e" font-weight="700" letter-spacing="0.6">CORE ARCHITECTURE</text>
  <text x="{PAD + 410}" y="{y_cursor + 46}" font-size="14.5" fill="#3fb950" font-weight="700">Full-Stack AI &amp; GIS Systems</text>
  <text x="{PAD + 410}" y="{y_cursor + 63}" font-size="12.5" fill="#c9d1d9">Hardware Signal Analysis &amp; RAG</text>
</g>
""")

y_cursor += box_h + 24

# Section Title for Visual Tech Distribution
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.28s;">
  <text x="{PAD}" y="{y_cursor}" font-size="13" font-weight="700" fill="#58a6ff" letter-spacing="0.8">SYSTEM WORKLOAD &amp; TECHNOLOGY PROFICIENCY MATRIX</text>
  <line x1="{PAD}" y1="{y_cursor + 9}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 9}" stroke="{FRAME}"/>
</g>
""")

y_cursor += 24

# Donut Chart Parameters
cx = PAD + 120
cy = y_cursor + 124
r = 92
stroke_w = 20
circumference = 2 * math.pi * r

slices = [
    ("AI / ML & Vision", 35, COLOR_AI),
    ("Backend Systems", 25, COLOR_BACKEND),
    ("Cloud & Infra", 18, COLOR_CLOUD),
    ("Hardware & IoT", 12, COLOR_HARDWARE),
    ("Geospatial GIS", 10, COLOR_GIS),
]

# Render Donut Chart with Solid Colors - NO GRADIENTS
svg_parts.append('<g class="fade-item" style="animation-delay: 0.38s;">')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r+17}" fill="none" stroke="#21262d" stroke-width="1" stroke-dasharray="3 4"/>')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r-17}" fill="none" stroke="#21262d" stroke-width="1" stroke-dasharray="3 4"/>')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#161b22" stroke-width="{stroke_w}"/>')

accum_offset = 0
for label, pct, col in slices:
    dash_len = (pct / 100.0) * circumference
    gap_len = circumference - dash_len
    angle = (accum_offset / circumference) * 360 - 90
    svg_parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{stroke_w}" '
        f'stroke-dasharray="{dash_len:.2f} {gap_len:.2f}" stroke-linecap="round" '
        f'transform="rotate({angle:.2f} {cx} {cy})"/>'
    )
    accum_offset += dash_len

# Donut Center Readout
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r-24}" fill="#161b22" stroke="{FRAME}" stroke-width="1.5"/>')
svg_parts.append(f'<text x="{cx}" y="{cy - 14}" text-anchor="middle" font-size="11" fill="#8b949e" font-weight="700" letter-spacing="1.2">STACK</text>')
svg_parts.append(f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="16" fill="#f0f6fc" font-weight="800">ACTIVE</text>')
svg_parts.append(f'<text x="{cx}" y="{cy + 24}" text-anchor="middle" font-size="10.5" fill="#3fb950" font-weight="700">● PRODUCTION</text>')

# Chart Legend below Donut
legend_y = cy + r + 30
svg_parts.append(f'<g transform="translate({PAD + 10}, {legend_y})">')
for i, (label, pct, col) in enumerate(slices):
    col_x = (i % 2) * 122
    row_y = (i // 2) * 19
    svg_parts.append(f'<circle cx="{col_x}" cy="{row_y}" r="5" fill="{col}"/>')
    svg_parts.append(f'<text x="{col_x + 12}" y="{row_y + 4}" font-size="11.5" font-weight="600" fill="#e6edf3">{pct}% <tspan fill="#8b949e" font-weight="400">{label.split()[0]}</tspan></text>')
svg_parts.append("</g>")
svg_parts.append("</g>")

# Right side: System Monitor Resource Bars
bars_x = 312
bar_w = CANVAS_W - PAD - bars_x

meters = [
    ("AI, RAG & Vision", "94%", 0.94, "RAG · Google Gemini · Vertex AI · XGBoost · OpenCV · EasyOCR", COLOR_AI),
    ("Backend & Distributed", "88%", 0.88, "FastAPI · Python · Django · Node.js · Express · C++ · REST", COLOR_BACKEND),
    ("Cloud & Containers", "82%", 0.82, "Google Cloud Run · AWS Lambda · S3 · CloudFront · Docker", COLOR_CLOUD),
    ("Edge Hardware & RF", "76%", 0.76, "ESP32 (802.11 Sniffing) · Signal Processing · NumPy · SciPy", COLOR_HARDWARE),
    ("Interactive GIS & Web", "86%", 0.86, "MapLibre GL JS · React · Next.js · TypeScript · NASA FIRMS", COLOR_GIS),
]

bar_cursor_y = y_cursor + 14
track_h = 10

for idx, (title, pct_str, pct_val, stack_str, col) in enumerate(meters):
    delay = 0.45 + idx * 0.08
    meter_w = int(bar_w * pct_val)
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <!-- Title & Percentage -->
      <text x="{bars_x}" y="{bar_cursor_y}" font-size="13.5" font-weight="700" fill="{col}">{html.escape(title)}</text>
      <text x="{CANVAS_W - PAD}" y="{bar_cursor_y}" font-size="13" font-weight="700" fill="#f0f6fc" text-anchor="end">{pct_str}</text>
      
      <!-- Progress Bar Track & Fill (Solid color, NO GRADIENTS) -->
      <rect x="{bars_x}" y="{bar_cursor_y + 6}" width="{bar_w}" height="{track_h}" rx="5" fill="#161b22" stroke="#21262d" stroke-width="1"/>
      <rect class="bar-anim" x="{bars_x}" y="{bar_cursor_y + 6}" width="{meter_w}" height="{track_h}" rx="5" fill="{col}" style="animation-delay: {delay+0.08:.2f}s;"/>
      
      <!-- Subtitle Stack Tags -->
      <text x="{bars_x}" y="{bar_cursor_y + 29}" font-size="12" fill="#b1bac4">{html.escape(stack_str)}</text>
    </g>
    """)
    bar_cursor_y += 50

y_cursor = max(legend_y + 58, bar_cursor_y + 12)

# Divider for Achievements
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.95s;">
  <line x1="{PAD}" y1="{y_cursor}" x2="{CANVAS_W - PAD}" y2="{y_cursor}" stroke="{FRAME}"/>
  <text x="{PAD}" y="{y_cursor + 22}" font-size="12.5" font-weight="700" fill="#d29922" letter-spacing="0.6">HACKATHON HONORS &amp; RECOGNITION</text>
</g>
""")

y_cursor += 44

achievements = [
    ("Finalist", "Nari Kavach 2026", "NAZAR Wi-Fi Cam Detection (IEEE WIE DU)", "#3fb950"),
    ("Top 15", "Hack-4-Viksit Bharat", "Nyaya-Sahayak Legal RAG (SISL × Google Cloud)", "#388bfd"),
    ("SIH 2026", "IGNISSENSE", "Satellite Thermal Anomaly Classifier (PS 26162)", "#a371f7"),
    ("SIH 2025", "Team Encrypted", "Academic Doc Authenticity Validator (PS 25029)", "#39c5cf"),
]

for idx, (badge, title, desc, col) in enumerate(achievements):
    delay = 1.05 + idx * 0.08
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <text x="{PAD + 4}" y="{y_cursor}" font-size="13.5" font-weight="700" fill="{col}">[{html.escape(badge)}]</text>
      <text x="{PAD + 115}" y="{y_cursor}" font-size="14" font-weight="600" fill="#f0f6fc">{html.escape(title)}</text>
      <text x="{PAD + 310}" y="{y_cursor}" font-size="12.5" fill="#9da7b3">— {html.escape(desc)}</text>
    </g>
    """)
    y_cursor += 26

y_cursor += 12

# Terminal Color Palette Blocks
colors_dark = ["#484f58", "#ff7b72", "#7ee787", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"]
colors_light = ["#6e7681", "#ffa198", "#aff5b4", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#f0f6fc"]

svg_parts.append('<g class="fade-item" style="animation-delay: 1.35s;">')
for i, col in enumerate(colors_dark):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="38" height="15" rx="3" fill="{col}"/>')
y_cursor += 19
for i, col in enumerate(colors_light):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="38" height="15" rx="3" fill="{col}"/>')
svg_parts.append("</g>")

status_line_y = TITLEBAR_H + 800 + PAD * 0.35
status_y = status_line_y + 20
svg_parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
status_prompt_plain = "krishna@github:~$ status OPEN TO WORK & COLLABORATION "
svg_parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13.5">'
    f'krishna@github:~$ status <tspan fill="#3fb950" font-weight="600">OPEN TO WORK &amp; COLLABORATION</tspan></text>'
)
cursor_x = PAD + len(status_prompt_plain) * 13.5 * 0.60
svg_parts.append(
    f'<rect x="{cursor_x:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="#3fb950">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
)

svg_parts.append("</svg>")

svg_code = "".join(svg_parts)
with open(OUT, "w") as f:
    f.write(svg_code)

try:
    ET.fromstring(svg_code)
    print(f"Generated {OUT} ({len(svg_code)} bytes)")
except Exception as e:
    print("XML Error:", e)
