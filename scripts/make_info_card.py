#!/usr/bin/env python3
"""
Generates the Neofetch Info Card SVG (info-card.svg).
Features:
- Academic Base & Core Architecture Summary
- Dynamic Technology Domain Allocation Donut Chart
- Animated System Monitor (btop/htop style) Resource Proficiency Meters
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
    animation: barGrow 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .fade-item { opacity: 1 !important; transform: none !important; animation: none !important; }
    .bar-anim { transform: none !important; animation: none !important; }
  }
</style>
""")

# Defs with gradients
svg_parts.append(f"""
<defs>
  <linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG2}"/>
    <stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <linearGradient id="grad-purple" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8957e5"/><stop offset="1" stop-color="#bc8cff"/>
  </linearGradient>
  <linearGradient id="grad-blue" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1f6feb"/><stop offset="1" stop-color="#58a6ff"/>
  </linearGradient>
  <linearGradient id="grad-green" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#238636"/><stop offset="1" stop-color="#3fb950"/>
  </linearGradient>
  <linearGradient id="grad-orange" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#bd561d"/><stop offset="1" stop-color="#f78166"/>
  </linearGradient>
  <linearGradient id="grad-cyan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1b7c83"/><stop offset="1" stop-color="#39c5cf"/>
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
svg_parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">krishna@github: ~$ neofetch --metrics</text>')

y_cursor = 62

# Header: Host title
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.08s;">
  <text x="{PAD}" y="{y_cursor}" font-size="19" font-weight="700" fill="#58a6ff">krishna<tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">du-fot-terminal</tspan></text>
  <line x1="{PAD}" y1="{y_cursor + 10}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 10}" stroke="{FRAME}" stroke-dasharray="3 3"/>
</g>
""")

y_cursor += 36

# Highlight boxes
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.18s;">
  <rect x="{PAD}" y="{y_cursor}" width="370" height="66" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 16}" y="{y_cursor + 24}" font-size="10.5" fill="#8b949e" font-weight="600" letter-spacing="0.5">ACADEMIC BASE</text>
  <text x="{PAD + 16}" y="{y_cursor + 42}" font-size="13" fill="#58a6ff" font-weight="700">University of Delhi · FoT</text>
  <text x="{PAD + 16}" y="{y_cursor + 57}" font-size="11" fill="#c9d1d9">B.Tech CSE (AI/ML) · Class of 2029</text>

  <rect x="{PAD + 394}" y="{y_cursor}" width="382" height="66" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 410}" y="{y_cursor + 24}" font-size="10.5" fill="#8b949e" font-weight="600" letter-spacing="0.5">CORE ARCHITECTURE</text>
  <text x="{PAD + 410}" y="{y_cursor + 42}" font-size="13" fill="#7ee787" font-weight="700">Full-Stack AI &amp; GIS Systems</text>
  <text x="{PAD + 410}" y="{y_cursor + 57}" font-size="11" fill="#c9d1d9">Hardware Signal Analysis &amp; RAG</text>
</g>
""")

y_cursor += 88

# Section Title for Visual Tech Distribution
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.28s;">
  <text x="{PAD}" y="{y_cursor}" font-size="12" font-weight="700" fill="#58a6ff" letter-spacing="0.8">SYSTEM WORKLOAD &amp; TECHNOLOGY PROFICIENCY MATRIX</text>
  <line x1="{PAD}" y1="{y_cursor + 8}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 8}" stroke="{FRAME}"/>
</g>
""")

y_cursor += 24

# Donut Chart Parameters
cx = PAD + 115
cy = y_cursor + 116
r = 82
circumference = 2 * math.pi * r

slices = [
    ("AI / ML & Vision", 35, "#bc8cff", "grad-purple"),
    ("Backend Systems", 25, "#58a6ff", "grad-blue"),
    ("Cloud & Infra", 18, "#3fb950", "grad-green"),
    ("Hardware & IoT", 12, "#f78166", "grad-orange"),
    ("Geospatial GIS", 10, "#39c5cf", "grad-cyan"),
]

# Render Donut Chart
svg_parts.append('<g class="fade-item" style="animation-delay: 0.38s;">')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r+15}" fill="none" stroke="#21262d" stroke-width="1" stroke-dasharray="2 4"/>')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r-15}" fill="none" stroke="#21262d" stroke-width="1" stroke-dasharray="2 4"/>')
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#161b22" stroke-width="16"/>')

accum_offset = 0
for label, pct, col, grad in slices:
    dash_len = (pct / 100.0) * circumference
    gap_len = circumference - dash_len
    angle = (accum_offset / circumference) * 360 - 90
    svg_parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#{grad})" stroke-width="16" '
        f'stroke-dasharray="{dash_len:.2f} {gap_len:.2f}" stroke-linecap="round" '
        f'transform="rotate({angle:.2f} {cx} {cy})"/>'
    )
    accum_offset += dash_len

# Donut Center Readout
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r-22}" fill="#161b22" stroke="{FRAME}" stroke-width="1"/>')
svg_parts.append(f'<text x="{cx}" y="{cy - 12}" text-anchor="middle" font-size="9" fill="#8b949e" font-weight="700" letter-spacing="1">STACK</text>')
svg_parts.append(f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="14" fill="#f0f6fc" font-weight="800">ACTIVE</text>')
svg_parts.append(f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="9" fill="#3fb950" font-weight="600">● PRODUCTION</text>')

# Chart Legend below Donut
legend_y = cy + r + 30
svg_parts.append(f'<g transform="translate({PAD + 15}, {legend_y})">')
for i, (label, pct, col, _) in enumerate(slices):
    col_x = (i % 2) * 115
    row_y = (i // 2) * 16
    svg_parts.append(f'<circle cx="{col_x}" cy="{row_y}" r="4" fill="{col}"/>')
    svg_parts.append(f'<text x="{col_x + 9}" y="{row_y + 3.5}" font-size="9.5" fill="#c9d1d9">{pct}% <tspan fill="#8b949e">{label.split()[0]}</tspan></text>')
svg_parts.append("</g>")
svg_parts.append("</g>")

# Right side: System Monitor Resource Bars
bars_x = 300
bar_w = CANVAS_W - PAD - bars_x

meters = [
    ("AI, RAG & Vision", "94%", 0.94, "RAG · Google Gemini · Vertex AI · XGBoost · OpenCV · EasyOCR", "grad-purple", "#bc8cff"),
    ("Backend & Distributed", "88%", 0.88, "FastAPI · Python · Django · Node.js · Express · C++ · REST", "grad-blue", "#58a6ff"),
    ("Cloud & Containers", "82%", 0.82, "Google Cloud Run · AWS Lambda · S3 · CloudFront · Docker", "grad-green", "#3fb950"),
    ("Edge Hardware & RF", "76%", 0.76, "ESP32 (802.11 Sniffing) · Signal Processing · NumPy · SciPy", "grad-orange", "#f78166"),
    ("Interactive GIS & Web", "86%", 0.86, "MapLibre GL JS · React · Next.js · TypeScript · NASA FIRMS", "grad-cyan", "#39c5cf"),
]

bar_cursor_y = y_cursor + 12
for idx, (title, pct_str, pct_val, stack_str, grad, col) in enumerate(meters):
    delay = 0.45 + idx * 0.08
    meter_w = int(bar_w * pct_val)
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <!-- Title & Percentage -->
      <text x="{bars_x}" y="{bar_cursor_y}" font-size="12" font-weight="700" fill="{col}">{html.escape(title)}</text>
      <text x="{CANVAS_W - PAD}" y="{bar_cursor_y}" font-size="11.5" font-weight="700" fill="#f0f6fc" text-anchor="end">{pct_str}</text>
      
      <!-- Progress Bar Track & Fill -->
      <rect x="{bars_x}" y="{bar_cursor_y + 5}" width="{bar_w}" height="8" rx="4" fill="#161b22" stroke="#21262d" stroke-width="1"/>
      <rect class="bar-anim" x="{bars_x}" y="{bar_cursor_y + 5}" width="{meter_w}" height="8" rx="4" fill="url(#{grad})" style="animation-delay: {delay+0.1:.2f}s;"/>
      
      <!-- Subtitle Stack Tags -->
      <text x="{bars_x}" y="{bar_cursor_y + 26}" font-size="10.5" fill="#8b949e">{html.escape(stack_str)}</text>
    </g>
    """)
    bar_cursor_y += 48

y_cursor = max(legend_y + 52, bar_cursor_y + 10)

# Divider for Achievements
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.95s;">
  <line x1="{PAD}" y1="{y_cursor}" x2="{CANVAS_W - PAD}" y2="{y_cursor}" stroke="{FRAME}"/>
  <text x="{PAD}" y="{y_cursor + 20}" font-size="11.5" font-weight="700" fill="#d29922" letter-spacing="0.6">HACKATHON HONORS &amp; RECOGNITION</text>
</g>
""")

y_cursor += 40

achievements = [
    ("Finalist", "Nari Kavach 2026", "NAZAR Wi-Fi Cam Detection (IEEE WIE DU)", "#7ee787"),
    ("Top 15", "Hack-4-Viksit Bharat", "Nyaya-Sahayak Legal RAG (SISL × Google Cloud)", "#58a6ff"),
    ("SIH 2026", "IGNISSENSE", "Satellite Thermal Anomaly Classifier (PS 26162)", "#bc8cff"),
    ("SIH 2025", "Team Encrypted", "Academic Doc Authenticity Validator (PS 25029)", "#39c5cf"),
]

for idx, (badge, title, desc, col) in enumerate(achievements):
    delay = 1.05 + idx * 0.08
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <text x="{PAD + 4}" y="{y_cursor}" font-size="12" font-weight="700" fill="{col}">[{html.escape(badge)}]</text>
      <text x="{PAD + 110}" y="{y_cursor}" font-size="12.5" font-weight="600" fill="#f0f6fc">{html.escape(title)}</text>
      <text x="{PAD + 295}" y="{y_cursor}" font-size="11.5" fill="#8b949e">— {html.escape(desc)}</text>
    </g>
    """)
    y_cursor += 24

y_cursor += 12

# Terminal Color Palette Blocks (iconic Neofetch palette)
colors_dark = ["#484f58", "#ff7b72", "#7ee787", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"]
colors_light = ["#6e7681", "#ffa198", "#aff5b4", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#f0f6fc"]

svg_parts.append('<g class="fade-item" style="animation-delay: 1.35s;">')
for i, col in enumerate(colors_dark):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="{38}" height="15" rx="3" fill="{col}"/>')
y_cursor += 19
for i, col in enumerate(colors_light):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="{38}" height="15" rx="3" fill="{col}"/>')
svg_parts.append("</g>")

status_line_y = TITLEBAR_H + 800 + PAD * 0.35
status_y = status_line_y + 19
svg_parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
status_prompt_plain = "krishna@github:~$ status OPEN TO WORK & COLLABORATION "
svg_parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'krishna@github:~$ status <tspan fill="#7ee787">OPEN TO WORK &amp; COLLABORATION</tspan></text>'
)
cursor_x = PAD + len(status_prompt_plain) * 13 * 0.60
svg_parts.append(
    f'<rect x="{cursor_x:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="#7ee787">'
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
