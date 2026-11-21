"""Render the README banner (an SVG) from live job stats.

Called by build_readme.py on every nightly run. Flat graphite, system fonts
only, so it renders the same inside GitHub's <img> sandbox.
"""
from pathlib import Path
from xml.sax.saxutils import escape

BANNER_PATH = Path(".github/assets/banner.svg")

W, H = 1280, 260
PAD = 64
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

BG, BORDER = "#1f2023", "#33353a"
TEXT, MUTED, DIM = "#ececee", "#9a9ca3", "#6f7178"

def render(total, added, when, categories=None, ats=5, boards=14):
    """Return the banner SVG. `categories` is accepted but unused (kept simple)."""
    stats = f"{total:,} open roles   ·   +{added:,} added last run   ·   updated {when}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">Developer Marketing Jobs</title>
  <desc id="d">{total:,} open developer marketing, DevRel and technical writing roles, updated {escape(when)}.</desc>
  <rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{BORDER}"/>
  <text x="{PAD}" y="112" font-family="{SANS}" font-size="58" font-weight="700" letter-spacing="-1.5" fill="{TEXT}">Developer Marketing Jobs</text>
  <text x="{PAD}" y="156" font-family="{SANS}" font-size="20" fill="{MUTED}">DevRel, docs, developer marketing, growth and community roles, pulled nightly from company ATS feeds.</text>
  <text x="{PAD}" y="208" font-family="{MONO}" font-size="15" fill="{DIM}">{escape(stats)}</text>
</svg>
'''

def write(total, added, when, categories=None):
    BANNER_PATH.parent.mkdir(parents=True, exist_ok=True)
    BANNER_PATH.write_text(render(total, added, when, categories), encoding="utf-8")
