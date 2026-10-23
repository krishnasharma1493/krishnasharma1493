#!/usr/bin/env python3
"""
Renders one lab-notebook style figure per project: figures/<slug>.svg (dark) and
figures/<slug>-light.svg. Each figure shows the project's actual result (a plot) or how it
works (a pipeline diagram) on the left, a Problem / Solution side caption on the right, and,
for public repos, a language bar built from the repo's real GitHub linguist data
(data/code-stats.json, from fetch_code_stats.py) along the bottom.

Figures are shown one per row at full README width (~800px of a 1000px canvas), so canvas
type is 15px or larger. Plots use real numbers only; the Presently curve is a labelled example
of the app's formula. Captions, notes and diagrams stop the script if they would overflow.
"""

import html
import json
import math
import os
import sys
import textwrap
import xml.etree.ElementTree as ET

from theme import FONT, GROUP_ORDER, MONO_ADV, TECH_ICONS, THEMES, group_colors, grouped, tech_label

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "code-stats.json")
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "figures")

W = 1000
PAD = 40
PLOT_L, PLOT_R = PAD, 605          # plot / diagram column
PLOT_TOP, PLOT_BOTTOM = 150, 380
NOTE_Y = 414
CAP_X, CAP_R = 640, W - PAD         # side caption column
CAP_SIZE, CAP_LINE = 18, 26
CAP_BOTTOM = 440                    # last caption baseline
BAR_BLOCK = 100                     # height added for the language bar
BODY_H = 460                        # figure height without the language bar

PROJECTS = [
    {
        "slug": "nazar", "repo": "NAZAR", "name": "NAZAR", "honour": "Finalist",
        "context": "Nari Kavach 2026 · IEEE WIE, University of Delhi",
        "problem": "Hidden cameras in rented rooms stream over encrypted Wi-Fi, so you can't read their traffic to find them.",
        "solution": "Flash a coded light pattern at the room. A camera that sees it shifts its bitrate, and a cheap Wi-Fi chip catches the rhythm in packet timing.",
        "plot": "nazar",
        "note": ["captured on ", ("ESP32",), " · permutation test in ", ("SciPy",)],
    },
    {
        "slug": "ignissense", "repo": "IGNISSENSE", "name": "IGNISSENSE", "honour": "0.55 macro-F1",
        "context": "Smart India Hackathon 2026",
        "problem": "Satellites flag thousands of heat spots across India but can't tell a wildfire from crop burning or a factory flare.",
        "solution": "Join each alert with 341k mapped facilities and land use, then let a gradient-boosted model say what's really burning.",
        "plot": "ignissense",
        "note": ["12.9k alerts × 341k sites · train 2023, test 2024"],
    },
    {
        "slug": "nyaya-sahayak", "repo": "Nyaya-Sahayak-Core", "name": "Nyaya-Sahayak", "honour": "Top 15",
        "context": "Hack-4-Viksit Bharat · GeeksforGeeks × Google Cloud",
        "problem": "Most people can't afford a lawyer just to learn which law applies to their problem.",
        "solution": "Describe it by voice, photo or text and get the exact sections of Indian law plus a cited first-draft petition.",
        "flow": [[["voice"], ["photo"], ["text"]], [["Vertex AI", "statutes"]],
                 [["Gemini", "drafting"]], [["cited", "petition"]]],
        "note": ["OCR + speech in · BNS/IPC, CrPC, CPC · on ", ("Cloud Run",)],
    },
    {
        "slug": "multi-ocular", "repo": "multi-ocular-disease-detection", "name": "Multi-Ocular", "honour": "4 diseases, 1 photo",
        "context": "Retinal screening research prototype · not a medical device",
        "problem": "One eye photo can show several diseases, but most screening models look for only one.",
        "solution": "One model checks a retinal photo for myopia, cataract, glaucoma and diabetic retinopathy at once.",
        "flow": [[["retinal", "photo"]], [["PyTorch", "EfficientNet-B0"]],
                 [["myopia"], ["cataract"], ["glaucoma"], ["diabetic", "retinopathy"]]],
        "note": ["masked loss for unlabelled diseases · demo in ", ("Gradio",)],
    },
    {
        "slug": "presently", "repo": "Presently", "name": "Presently", "honour": "offline iOS app",
        "context": "Native iPhone app with Live Activities and widgets",
        "problem": "Students slip below 75% attendance because nothing tracks how many classes they can actually skip.",
        "solution": "An offline iPhone app that does the math, with Live Activities and widgets. No account, no server.",
        "plot": "presently",
        "note": ["worked out on-device in ", ("Swift",), " · no network calls"],
    },
    {
        "slug": "censorra", "repo": "Censorra", "name": "Censorra", "honour": "real-time",
        "context": "Browser extension for safer shared screens",
        "problem": "Unsafe content pops up on classroom and shared screens before anyone can react.",
        "solution": "A browser extension that classifies images and text with AI as pages load and closes unsafe windows.",
        "flow": [[["page", "loads"]], [["images", "+ text"]], [["Hugging Face", "classifier"]],
                 [["safe:", "keep"], ["unsafe:", "close"]]],
        "note": ["runs as a ", ("Chrome",), " Manifest V3 extension"],
    },
    {
        "slug": "authenticity-validator", "repo": None, "name": "Authenticity Validator", "honour": "SIH 2025",
        "context": "Smart India Hackathon 2025 · Team Encrypted",
        "problem": "Forged degrees are easy to print and slow to check.",
        "solution": "OCR reads paper certificates, signed QR codes verify digital ones, both matched against university records.",
        "flow": [[["paper", "certificate"], ["digital", "certificate"]], [["OpenCV", "+ EasyOCR"], ["signed", "QR check"]],
                 [["Node.js", "match records"]], [["valid /", "forged"]]],
        "note": ["deployed on ", ("AWS Lambda",), " + ", ("AWS S3",)],
    },
    {
        "slug": "early-disease-detection", "repo": None, "name": "Early Disease Detection", "honour": "CODESLAYER2k25",
        "context": "Hackathon build · Team Decypher",
        "problem": "Early symptoms get missed until a disease turns serious, in people and animals alike.",
        "solution": "A symptom checker that predicts likely diseases and explains each prediction.",
        "flow": [[["symptoms"]], [["scikit-learn", "model"]], [["likely", "diseases"], ["why it", "thinks so"]]],
        "note": ["served with ", ("Flask",), " · for people and animals"],
    },
]


def esc(s):
    return html.escape(s, quote=False)


def text(x, y, s, size, color, weight="400", anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def inline(parts, x, y, size, t, color=None):
    """Runs of plain text and (tech,) tuples on one line; tech names get their logo. Returns (svg, end x)."""
    color = color or t["muted"]
    out = []
    for part in parts:
        if isinstance(part, tuple):
            svg, w = tech_label(part[0], x, y, size, color)
        else:
            svg, w = text(x, y, part, size, color, extra=' xml:space="preserve"'), len(part) * size * MONO_ADV
        out.append(svg)
        x += w
    return "".join(out), x


def h_bars(p, t, rows, x_max, ticks, threshold=None, axis_label=""):
    """Horizontal bars with the label above each bar. rows: (label, value, color, annotation)."""
    left, right = PLOT_L + 10, PLOT_R - 200
    scale = (right - left) / x_max
    base = PLOT_BOTTOM - 28
    bar_h = 30
    y = PLOT_TOP + 34
    for label, value, color, note in rows:
        p.append(text(left, y - 9, label, 17, t["fg"]))
        p.append(f'<rect x="{left}" y="{y}" width="{value * scale:.1f}" height="{bar_h}" fill="{color}"/>')
        p.append(text(left + value * scale + 12, y + bar_h * 0.7, note, 17, t["fg"], weight="700"))
        y += bar_h + 50
    p.append(f'<line x1="{left}" y1="{base}" x2="{right}" y2="{base}" stroke="{t["muted"]}"/>')
    for v, lab in ticks:
        tx = left + v * scale
        p.append(f'<line x1="{tx:.1f}" y1="{base}" x2="{tx:.1f}" y2="{base + 5}" stroke="{t["muted"]}"/>')
        p.append(text(tx, base + 22, lab, 15, t["muted"], anchor="middle"))
    if threshold:
        v, lab = threshold
        tx = left + v * scale
        p.append(f'<line x1="{tx:.1f}" y1="{PLOT_TOP}" x2="{tx:.1f}" y2="{base}" stroke="{t["accent2"]}" stroke-dasharray="5 4"/>')
        p.append(text(tx + 6, PLOT_TOP + 2, lab, 15, t["accent2"]))
    if axis_label:
        mid = left + (ticks[-2][0] + ticks[-1][0]) / 2 * scale
        p.append(text(mid, base + 22, axis_label, 15, t["muted"], anchor="middle"))


def plot_nazar(p, t):
    rows = [("hidden camera", -math.log10(0.0055), t["series"][0], "p = 0.0055 detected"),
            ("control laptop", -math.log10(0.4748), t["other"], "p = 0.47 no signal")]
    h_bars(p, t, rows, 3.0, [(0, "0"), (1, "1"), (2, "2"), (3, "3")],
           threshold=(-math.log10(0.05), "p = 0.05"), axis_label="−log₁₀ p")


def plot_ignissense(p, t):
    rows = [("rule baseline", 0.41, t["other"], "0.41"),
            ("XGBoost", 0.55, t["series"][1], "0.55 (+0.14)")]
    h_bars(p, t, rows, 1.0, [(0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1, "1")], axis_label="macro-F1")


def plot_presently(p, t):
    # Example: 45 of 50 classes attended; each skipped class adds one to the total.
    attended, held, minimum = 45, 50, 0.75
    safe = math.floor((attended - minimum * held) / minimum)  # the app's safe-bunk formula
    ks = list(range(0, 15))
    pct = [attended / (held + k) * 100 for k in ks]
    left, right = PLOT_L + 56, PLOT_R - 10
    top, base = PLOT_TOP + 8, PLOT_BOTTOM - 28
    y_lo, y_hi = 70, 92

    def px(k):
        return left + (right - left) * k / ks[-1]

    def py(v):
        return base - (base - top) * (v - y_lo) / (y_hi - y_lo)

    p.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{base}" stroke="{t["muted"]}"/>')
    p.append(f'<line x1="{left}" y1="{base}" x2="{right}" y2="{base}" stroke="{t["muted"]}"/>')
    for v in (70, 75, 80, 85, 90):
        p.append(text(left - 10, py(v) + 5, f"{v}%", 15, t["muted"], anchor="end"))
    for k in (0, 5, 10, 14):
        p.append(text(px(k), base + 22, str(k), 15, t["muted"], anchor="middle"))
    p.append(text((px(5) + px(10)) / 2, base + 22, "classes skipped", 15, t["muted"], anchor="middle"))
    p.append(f'<line x1="{left}" y1="{py(75):.1f}" x2="{right}" y2="{py(75):.1f}" stroke="{t["accent2"]}" stroke-dasharray="5 4"/>')
    p.append(text(right, py(75) - 9, "75% minimum", 15, t["accent2"], anchor="end"))
    ok = " ".join(f"{px(k):.1f},{py(v):.1f}" for k, v in zip(ks, pct) if k <= safe)
    bad = " ".join(f"{px(k):.1f},{py(v):.1f}" for k, v in zip(ks, pct) if k >= safe)
    p.append(f'<polyline points="{ok}" fill="none" stroke="{t["series"][0]}" stroke-width="3"/>')
    p.append(f'<polyline points="{bad}" fill="none" stroke="{t["muted"]}" stroke-width="2" stroke-dasharray="3 4"/>')
    p.append(f'<circle cx="{px(safe):.1f}" cy="{py(pct[safe]):.1f}" r="6" fill="{t["series"][0]}" stroke="{t["bg"]}" stroke-width="2"/>')
    p.append(text(px(safe) - 14, py(pct[safe]) + 32, f"{safe} safe skips", 18, t["fg"], weight="700", anchor="end"))
    p.append(text(left + 14, top + 16, f"example: {attended} of {held} attended", 15, t["muted"]))


PLOTS = {"nazar": plot_nazar, "ignissense": plot_ignissense, "presently": plot_presently}


def node_size(lines, size):
    widths = []
    for i, line in enumerate(lines):
        logo = i == 0 and line in TECH_ICONS
        widths.append(len(line) * size * MONO_ADV + (size * 1.4 if logo else 0))
    return max(widths) + 24, len(lines) * (size + 6) + 16


def flow(p, t, columns, slug):
    size = 16
    sizes = [[node_size(n, size) for n in col] for col in columns]
    col_w = [max(w for w, _ in col) for col in sizes]
    gap = (PLOT_R - PLOT_L - sum(col_w)) / (len(columns) - 1)
    if gap < 28:
        sys.exit(f"{slug}: diagram is too wide for the plot column; shorten a node")
    mid = (PLOT_TOP + PLOT_BOTTOM) / 2
    boxes = []
    x = PLOT_L
    for ci, (col, col_sizes) in enumerate(zip(columns, sizes)):
        total_h = sum(h for _, h in col_sizes) + 12 * (len(col) - 1)
        y = mid - total_h / 2
        col_boxes = []
        last = ci == len(columns) - 1
        for lines, (w, h) in zip(col, col_sizes):
            bx = x + (col_w[ci] - w) / 2
            stroke = t["accent"] if last else t["muted"]
            p.append(f'<rect x="{bx:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{t["bg"]}" stroke="{stroke}"/>')
            ty = y + 8 + size
            for i, line in enumerate(lines):
                color = t["accent"] if last else (t["fg"] if i == 0 else t["muted"])
                if i == 0 and line in TECH_ICONS:
                    lw = node_size([line], size)[0] - 24
                    p.append(tech_label(line, bx + (w - lw) / 2, ty, size, color, weight="700")[0])
                else:
                    p.append(text(bx + w / 2, ty, line, size, color, weight="700" if i == 0 else "400", anchor="middle"))
                ty += size + 6
            col_boxes.append((bx, y, w, h))
            y += h + 12
        boxes.append(col_boxes)
        x += col_w[ci] + gap
    # equal-sized neighbouring columns connect one-to-one (paper -> OCR, digital -> QR); otherwise fan in/out
    for a, b in zip(boxes, boxes[1:]):
        pairs = zip(a, b) if len(a) == len(b) else [(na, nb) for na in a for nb in b]
        for (ax, ay, aw, ah), (bx, by, bw, bh) in pairs:
            p.append(f'<line x1="{ax + aw:.1f}" y1="{ay + ah / 2:.1f}" x2="{bx - 3:.1f}" y2="{by + bh / 2:.1f}" '
                     f'stroke="{t["muted"]}" marker-end="url(#arrow)"/>')


def caption(p, t, label, body, y, color, slug):
    width = int((CAP_R - CAP_X) / (CAP_SIZE * MONO_ADV))
    lines = textwrap.wrap(f"{label} {body}", width, break_on_hyphens=False)
    for i, line in enumerate(lines):
        if i == 0:
            rest = line[len(label):]
            p.append(f'<text x="{CAP_X}" y="{y}" font-size="{CAP_SIZE}" fill="{t["fg"]}" xml:space="preserve">'
                     f'<tspan font-weight="700" fill="{color}">{esc(label)}</tspan>{esc(rest)}</text>')
        else:
            p.append(text(CAP_X, y, line, CAP_SIZE, t["fg"]))
        y += CAP_LINE
    if y - CAP_LINE > CAP_BOTTOM:
        sys.exit(f"{slug}: caption is too long for the side column; shorten it")
    return y


def language_bar(p, t, langs, top):
    """GitHub-style language bar with logo + name + % labels. Draws nothing without data."""
    if not langs:
        return
    y = top + 30
    left, right = PAD, W - PAD
    p.append(f'<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" stroke="{t["frame"]}"/>')
    p.append(text(left, y, "code by language", 15, t["muted"]))
    y += 14
    colors = group_colors(t)
    g = grouped(langs)
    total = sum(g.values())
    x = left
    for k in GROUP_ORDER:
        if not g[k]:
            continue
        seg = (right - left) * g[k] / total
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{max(seg - 2, 1):.1f}" height="12" fill="{colors[k]}">'
                 f'<title>{esc(k)}: {g[k] / total * 100:.0f}%</title></rect>')
        x += seg
    # Labels: big segments first, small ones merged into one muted run, all with logos
    lx, ly = left, y + 44
    shares = [(k, g[k] / total * 100) for k in GROUP_ORDER if g[k]]
    for k, pct in sorted([s for s in shares if s[1] >= 10], key=lambda s: -s[1]):
        p.append(f'<rect x="{lx:.1f}" y="{ly - 12}" width="12" height="12" fill="{colors[k]}"/>')
        svg, w = tech_label(k, lx + 20, ly, 17, t["fg"], suffix=f" {pct:.0f}%")
        p.append(svg)
        lx += 20 + w + 28
    small = sorted([s for s in shares if s[1] < 10], key=lambda s: -s[1])
    if small:
        parts = ["+ "]
        for i, (k, pct) in enumerate(small):
            parts += [(k,), f" {max(pct, 1):.0f}%" + (" · " if i < len(small) - 1 else "")]
        p.append(inline(parts, lx, ly, 15, t)[0])


def build(t, idx, proj, langs):
    h = BODY_H + (BAR_BLOCK if langs else 0)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="{FONT}">']
    p.append(f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             f'<path d="M0 0 L10 5 L0 10 z" fill="{t["muted"]}"/></marker></defs>')
    p.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" fill="{t["bg"]}" stroke="{t["frame"]}"/>')

    # Header
    p.append(text(PAD, 48, f"FIG. {idx + 1}", 15, t["muted"], weight="700", extra=' letter-spacing="3"'))
    name_w = len(proj["name"]) * 32 * MONO_ADV
    p.append(text(PAD, 92, proj["name"], 32, t["head"], weight="700"))
    p.append(text(PAD + name_w + 16, 92, f"— {proj['honour']}", 22, t["accent"], weight="700"))
    p.append(text(PAD, 122, proj["context"], 17, t["muted"]))
    if proj["repo"]:
        p.append(text(W - PAD, 92, "repo →", 18, t["accent"], anchor="end"))

    # Left column: plot or diagram, then its note line
    if "plot" in proj:
        PLOTS[proj["plot"]](p, t)
    else:
        flow(p, t, proj["flow"], proj["slug"])
    note, end_x = inline(proj["note"], PLOT_L, NOTE_Y, 15, t)
    if end_x > PLOT_R + 10:
        sys.exit(f"{proj['slug']}: note line is wider than the plot column; shorten it")
    p.append(note)

    # Right column: side caption
    p.append(f'<line x1="{CAP_X - 22}" y1="{PLOT_TOP - 6}" x2="{CAP_X - 22}" y2="{CAP_BOTTOM}" stroke="{t["frame"]}"/>')
    y = caption(p, t, "Problem.", proj["problem"], PLOT_TOP + 12, t["problem"], proj["slug"])
    caption(p, t, "Solution.", proj["solution"], y + 14, t["solution"], proj["slug"])

    language_bar(p, t, langs, BODY_H - 4)
    p.append("</svg>")
    return "".join(p)


with open(DATA) as f:
    by_repo = {r["repo"]: r["languages"] for r in json.load(f)["projects"]}

os.makedirs(OUT_DIR, exist_ok=True)
for idx, proj in enumerate(PROJECTS):
    for theme in THEMES:
        svg = build(theme, idx, proj, by_repo.get(proj["repo"]))
        ET.fromstring(svg)
        with open(os.path.join(OUT_DIR, f"{proj['slug']}{theme['suffix']}.svg"), "w") as f:
            f.write(svg)
print(f"Generated {len(PROJECTS) * len(THEMES)} figures in {os.path.abspath(OUT_DIR)}")
