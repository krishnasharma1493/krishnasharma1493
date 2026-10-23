#!/usr/bin/env python3
"""
Downloads the tech logos used across the profile SVGs from Simple Icons (CC0) and stores
their 24x24 path data in scripts/icons.json, so the generators run offline.
GitHub renders README SVGs sandboxed (no external images), which is why the logos are
inlined as paths instead of linked. Re-run after adding a slug to TECH_ICONS in theme.py.
"""

import json
import os
import re
import urllib.error
import urllib.request

from theme import TECH_ICONS

VERSION = "13.21.0"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "icons.json")

paths, missing = {}, []
for slug in sorted(set(TECH_ICONS.values())):
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@{VERSION}/icons/{slug}.svg"
    try:
        with urllib.request.urlopen(url) as r:
            svg = r.read().decode()
    except urllib.error.HTTPError:
        missing.append(slug)
        continue
    paths[slug] = re.search(r' d="([^"]+)"', svg).group(1)

with open(OUT, "w") as f:
    json.dump(paths, f, indent=0, sort_keys=True)
print(f"Wrote {OUT} ({len(paths)} icons)")
if missing:
    print("Not in Simple Icons (chips show text only):", ", ".join(missing))
