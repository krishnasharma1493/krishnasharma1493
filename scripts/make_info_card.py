#!/usr/bin/env python3
"""
Generates the Neofetch Info Card SVG (info-card.svg).
Pairs side-by-side with krishna-ascii.svg inside an 840x880 canvas.
Uses clean terminal styling, animated entrance, color swatches, and system statistics.
"""

import html
import os
import sys

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
INK = "#c9d1d9"

svg_parts = []
svg_parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">'
)

svg_parts.append("""
<style>
  .fade-item {
    opacity: 0;
    animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .key { font-weight: 700; fill: #58a6ff; font-size: 13.5px; }
  .val { fill: #c9d1d9; font-size: 13.5px; }
  @media (prefers-reduced-motion: reduce) {
    .fade-item { opacity: 1 !important; transform: none !important; animation: none !important; }
  }
</style>
""")

svg_parts.append(f"""
<defs>
  <linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG2}"/>
    <stop offset="1" stop-color="{BG}"/>
  </linearGradient>
</defs>
""")

svg_parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#card-bg)"/>')
svg_parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')

# Titlebar
svg_parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    svg_parts.append(f'<circle cx="{20 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
svg_parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">krishna@github: ~$ neofetch --profile</text>')

y_cursor = 62

# Host header
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.1s;">
  <text x="{PAD}" y="{y_cursor}" font-size="19" font-weight="700" fill="#58a6ff">krishna<tspan fill="#8b949e">@</tspan><tspan fill="#7ee787">du-fot-terminal</tspan></text>
  <line x1="{PAD}" y1="{y_cursor + 10}" x2="{CANVAS_W - PAD}" y2="{y_cursor + 10}" stroke="{FRAME}" stroke-dasharray="3 3"/>
</g>
""")

y_cursor += 36

# Highlight boxes
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.25s;">
  <rect x="{PAD}" y="{y_cursor}" width="370" height="72" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 16}" y="{y_cursor + 25}" font-size="11" fill="#8b949e" font-weight="600" letter-spacing="0.5">ACADEMIC BASE</text>
  <text x="{PAD + 16}" y="{y_cursor + 45}" font-size="13.5" fill="#58a6ff" font-weight="700">University of Delhi · FoT</text>
  <text x="{PAD + 16}" y="{y_cursor + 61}" font-size="11.5" fill="#c9d1d9">B.Tech CSE (AI/ML) · Class of 2029</text>

  <rect x="{PAD + 394}" y="{y_cursor}" width="{CANVAS_W - PAD - (PAD + 394)}" height="72" rx="8" fill="#161b22" stroke="{FRAME}"/>
  <text x="{PAD + 410}" y="{y_cursor + 25}" font-size="11" fill="#8b949e" font-weight="600" letter-spacing="0.5">CORE ARCHITECTURE</text>
  <text x="{PAD + 410}" y="{y_cursor + 45}" font-size="13.5" fill="#7ee787" font-weight="700">Full-Stack AI &amp; GIS Systems</text>
  <text x="{PAD + 410}" y="{y_cursor + 61}" font-size="11.5" fill="#c9d1d9">Hardware Signal Analysis &amp; RAG</text>
</g>
""")

y_cursor += 98

specs = [
    ("Role", "Full-Stack Developer & AI Systems Engineer", "#58a6ff", "#c9d1d9"),
    ("Focus", "Satellite GIS · Legal Tech · Wi-Fi Hardware Security", "#58a6ff", "#c9d1d9"),
    ("Languages", "C++, C, Python, JavaScript, TypeScript, SQL", "#58a6ff", "#7ee787"),
    ("Web & Backend", "React, Next.js, FastAPI, Node.js, Django, Flask", "#58a6ff", "#c9d1d9"),
    ("AI, ML & Vision", "RAG, XGBoost, Scikit-learn, OpenCV, EasyOCR, Gemini", "#58a6ff", "#c9d1d9"),
    ("Cloud & Infra", "AWS (Lambda, S3, CloudFront), Cloud Run, Docker", "#58a6ff", "#c9d1d9"),
    ("Data & Hardware", "MongoDB, MySQL, ESP32 Promiscuous Sniffing, GIS", "#58a6ff", "#c9d1d9"),
]

for idx, (label, val, l_col, v_col) in enumerate(specs):
    delay = 0.35 + idx * 0.08
    svg_parts.append(f"""
    <g class="fade-item" style="animation-delay: {delay:.2f}s;">
      <text x="{PAD}" y="{y_cursor}" class="key" fill="{l_col}">{html.escape(label)}:</text>
      <text x="{PAD + 155}" y="{y_cursor}" class="val" fill="{v_col}">{html.escape(val)}</text>
    </g>
    """)
    y_cursor += 28

y_cursor += 6

# Divider for Achievements
svg_parts.append(f"""
<g class="fade-item" style="animation-delay: 0.95s;">
  <line x1="{PAD}" y1="{y_cursor}" x2="{CANVAS_W - PAD}" y2="{y_cursor}" stroke="{FRAME}"/>
  <text x="{PAD}" y="{y_cursor + 22}" font-size="11.5" font-weight="700" fill="#d29922" letter-spacing="0.6">HACKATHON HONORS &amp; RECOGNITION</text>
</g>
""")

y_cursor += 44

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
      <text x="{PAD + 4}" y="{y_cursor}" font-size="12.5" font-weight="700" fill="{col}">[{html.escape(badge)}]</text>
      <text x="{PAD + 110}" y="{y_cursor}" font-size="13" font-weight="600" fill="#f0f6fc">{html.escape(title)}</text>
      <text x="{PAD + 295}" y="{y_cursor}" font-size="12" fill="#8b949e">— {html.escape(desc)}</text>
    </g>
    """)
    y_cursor += 26

y_cursor += 16

colors_dark = ["#484f58", "#ff7b72", "#7ee787", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"]
colors_light = ["#6e7681", "#ffa198", "#aff5b4", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#f0f6fc"]

svg_parts.append('<g class="fade-item" style="animation-delay: 1.4s;">')
for i, col in enumerate(colors_dark):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="38" height="16" rx="3" fill="{col}"/>')
y_cursor += 20
for i, col in enumerate(colors_light):
    x = PAD + i * 44
    svg_parts.append(f'<rect x="{x}" y="{y_cursor}" width="38" height="16" rx="3" fill="{col}"/>')
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

print(f"Generated {OUT} ({len(svg_code)} bytes)")
