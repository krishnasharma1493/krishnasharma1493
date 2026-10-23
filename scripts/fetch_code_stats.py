#!/usr/bin/env python3
"""
Fetches per-language byte counts (GitHub linguist) for every public, non-fork repo
and writes data/code-stats.json for make_code_stats.py.
Uses the public REST API with no token (60 requests/hour is plenty).
Re-run whenever you push a new project, then regenerate the SVGs.
"""

import datetime
import json
import os
import sys
import urllib.request

USER = "krishnasharma1493"
SKIP = {USER}  # the profile repo itself

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "code-stats.json")


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
projects = []
for repo in repos:
    if repo["fork"] or repo["private"] or repo["name"] in SKIP:
        continue
    langs = get(repo["languages_url"])
    if langs:
        projects.append({"repo": repo["name"], "languages": langs})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump({"user": USER, "fetched": datetime.date.today().isoformat(), "projects": projects}, f, indent=2)
print(f"Wrote {OUT} ({len(projects)} repos)")
