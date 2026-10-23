# Regenerating the profile images

```sh
pip install -r scripts/requirements.txt
python3 scripts/prep_photo.py          # source-photo.jpg -> source-prepped.png (only when the photo changes)
python3 scripts/make_ascii_svg.py      # -> krishna-ascii.svg
python3 scripts/make_info_card.py      # -> info-card.svg
python3 scripts/fetch_icons.py         # tech logos -> scripts/icons.json (only when TECH_ICONS changes)
python3 scripts/fetch_code_stats.py    # GitHub language bytes -> data/code-stats.json (no token needed)
python3 scripts/make_code_stats.py     # -> code-stats.svg
python3 scripts/make_figures.py        # -> figures/<project>.svg
```

- Info card text: edit `make_info_card.py` directly. It stops if a line would run past the card edge.
- Project figures: `PROJECTS` in `make_figures.py`. Then update the matching `alt` text in the README.
- Colors for code-stats and the figures, and the tech-name → logo map (`TECH_ICONS`), live in `theme.py`.
  Logos are from [Simple Icons](https://simpleicons.org) (CC0).
- After pushing a new project, re-run the fetch + code-stats steps.
