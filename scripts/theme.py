"""
Shared GitHub-dark theme for the generated profile SVGs (code-stats and project figures),
matching the colors of the original hero cards (info-card.svg, krishna-ascii.svg).

`series` is the categorical chart palette, in fixed order (Python, TypeScript, Swift,
JavaScript, CSS/HTML). It was checked with the dataviz palette validator (lightness band,
chroma floor, CVD and normal-vision separation, contrast) against `bg2`. Re-run that if
you change it; green and orange must not be neighbours (they merge for red-green CVD).
"""

DARK = {
    "suffix": "",
    "bg": "#0d1117", "bg2": "#161b22", "panel": "#161b22", "frame": "#30363d",
    "fg": "#c9d1d9", "head": "#f0f6fc", "muted": "#8b949e", "title": "#7d8590",
    "accent": "#58a6ff", "accent2": "#ff7b72",
    "problem": "#ff7b72", "solution": "#7ee787",
    "series": ["#1f6feb", "#238636", "#8957e5", "#db6d28", "#bf4b8a"],
    "other": "#484f58",
}

THEMES = [DARK]

import html

FONT = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
MONO_ADV = 0.6  # monospace glyph advance, in em

# Tech name -> Simple Icons slug. fetch_icons.py downloads these into icons.json;
# a name whose slug isn't there just renders as text.
TECH_ICONS = {
    "Python": "python", "TypeScript": "typescript", "JavaScript": "javascript",
    "Swift": "swift", "C++": "cplusplus", "C": "c",
    "CSS / HTML": "html5", "C++ & other": "cplusplus",
    "ESP32": "espressif", "React": "react", "FastAPI": "fastapi", "Django": "django",
    "Flask": "flask", "Node.js": "nodedotjs", "Next.js": "nextdotjs",
    "SwiftUI": "swift", "SwiftData": "swift", "WidgetKit": "apple",
    "PyTorch": "pytorch", "EfficientNet": "pytorch", "Gradio": "gradio",
    "Gemini": "googlegemini", "Vertex AI": "googlecloud", "Cloud Run": "googlecloud",
    "XGBoost": "xgboost", "scikit-learn": "scikitlearn", "NumPy": "numpy", "SciPy": "scipy",
    "OpenCV": "opencv", "Hugging Face": "huggingface",
    "MapLibre GL": "maplibre", "Docker": "docker", "MongoDB": "mongodb", "SQLite": "sqlite",
    "AWS Lambda": "awslambda", "AWS S3": "amazons3", "Manifest V3": "googlechrome",
    "Chrome": "googlechrome", "S3": "amazons3", "CloudFront": "amazoncloudfront",
    "HTML": "html5", "CSS": "css3", "Express.js": "express", "MySQL": "mysql", "Firebase": "firebase",
    "Git / GitHub": "git",
}

_ICONS = None


def icon(name, x, y, size, color):
    """Logo for a tech name as an inline path, top-left at (x, y); "" if there's no glyph."""
    global _ICONS
    if _ICONS is None:
        import json
        import os
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")
        _ICONS = json.load(open(path)) if os.path.exists(path) else {}
    d = _ICONS.get(TECH_ICONS.get(name, ""))
    if not d:
        return ""
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size/24:.4f})" fill="{color}" d="{d}"/>'


def tech_label(name, x, y, size, color, suffix="", weight="400", logo_color=None):
    """Logo then name (plus optional suffix like " 74%"), text baseline at y. Returns (svg, width).
    Every tech name printed in an SVG should go through here so it carries its logo."""
    ico = size * 1.05
    logo = icon(name, x, y - size * 0.86, ico, logo_color or color)
    text_x = x + (ico + size * 0.35 if logo else 0)
    label = html.escape(name + suffix, quote=False)
    svg = logo + f'<text x="{text_x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{color}">{label}</text>'
    return svg, (text_x - x) + len(name + suffix) * size * MONO_ADV


# Language groups shared by the code-stats donut and each figure's language bar.
# Fixed order = fixed color: group i always uses theme["series"][i]; unlisted languages fold into OTHER.
GROUPS = [
    ("Python", {"Python", "Jupyter Notebook"}),
    ("TypeScript", {"TypeScript"}),
    ("Swift", {"Swift"}),
    ("JavaScript", {"JavaScript"}),
    ("CSS / HTML", {"CSS", "HTML", "SCSS"}),
]
OTHER = "C++ & other"
GROUP_ORDER = [g for g, _ in GROUPS] + [OTHER]


def grouped(langs):
    """Linguist {language: bytes} -> {group: bytes} over GROUP_ORDER."""
    out = {g: 0 for g in GROUP_ORDER}
    for lang, n in langs.items():
        out[next((g for g, members in GROUPS if lang in members), OTHER)] += n
    return out


def group_colors(t):
    return dict(zip(GROUP_ORDER, t["series"] + [t["other"]]))


def chip(name, x, y, size, t, outline=True):
    """Logo + name pill with its top-left at (x, y). Returns (svg, width)."""
    pad, gap, ico = size * 0.6, size * 0.4, size * 1.05
    logo = icon(name, x + pad, y + (size * 1.9 - ico) / 2, ico, t["fg"])
    text_x = x + pad + (ico + gap if logo else 0)
    w = (text_x - x) + len(name) * size * MONO_ADV + pad
    h = size * 1.9
    box = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" '
           f'fill="{t["panel"]}" stroke="{t["frame"]}"/>') if outline else ""
    label = (f'<text x="{text_x:.1f}" y="{y + h/2 + size*0.36:.1f}" font-size="{size}" '
             f'fill="{t["fg"]}">{html.escape(name, quote=False)}</text>')
    return box + logo + label, w


def window(t, w, h, title):
    """Terminal window chrome matching the original hero cards: background, frame, titlebar."""
    return (
        f'<defs><linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient></defs>'
        f'<rect width="{w}" height="{h}" rx="12" fill="url(#card-bg)"/>'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{t["frame"]}"/>'
        f'<line x1="0" y1="30" x2="{w}" y2="30" stroke="{t["frame"]}"/>'
        + "".join(f'<circle cx="{20 + i*16}" cy="15" r="5" fill="{c}"/>'
                  for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]))
        + f'<text x="{w/2}" y="19.5" fill="{t["title"]}" font-size="12.5" text-anchor="middle">{title}</text>'
    )
