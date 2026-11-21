"""Render the README banner (an SVG) from live job stats.

Called by build_readme.py on every nightly run. Flat, system-font only, so it
renders identically inside GitHub's <img> sandbox (no web fonts, no scripts).
"""
import re
from pathlib import Path
from xml.sax.saxutils import escape

BANNER_PATH = Path(".github/assets/banner.svg")

W, H = 1280, 412
PAD = 56
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
ACCENT = "#7b6bff"

SHORT = [  # (substring of category label, short legend name)
    ("advocate", "DevRel"), ("technical writing", "Docs"),
    ("developer marketing", "Dev Marketing"), ("product marketing", "Product Mktg"),
    ("growth", "Growth"), ("vp", "VP Marketing"), ("community", "Community"),
    ("full stack", "Full Stack"), ("seo", "SEO / GEO"), ("y combinator", "YC"),
]

def _short(label):
    plain = re.sub(r"[^\w\s/&]", "", label).strip()
    low = plain.lower()
    for key, name in SHORT:
        if key in low:
            return name
    return plain[:14]

def render(total, added, when, categories, ats=5, boards=14):
    """categories: list of (label, count). Returns the SVG as a string."""
    cats = [(_short(l), c) for l, c in categories if c > 0]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">',
        '  <title id="t">Developer Marketing Jobs</title>',
        f'  <desc id="d">{total:,} open developer marketing, DevRel and technical writing roles, updated {escape(when)}.</desc>',
        '  <defs>',
        '    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1b1f2b"/></pattern>',
        f'    <clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        '  </defs>',
        '  <g clip-path="url(#c)">',
        f'    <rect width="{W}" height="{H}" fill="#0c0e14"/>',
        f'    <rect width="{W}" height="{H}" fill="url(#dots)"/>',
        f'    <rect x="0" y="0" width="6" height="{H}" fill="#7b6bff"/>',
        # live marker
        f'    <circle cx="{PAD + 4}" cy="58" r="5" fill="#3ddc97"><animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/></circle>',
        f'    <text x="{PAD + 20}" y="63" font-family="{MONO}" font-size="14" letter-spacing="1" fill="#8b93a7">LIVE · UPDATED {escape(when.upper())}</text>',
        # headline
        f'    <text x="{PAD}" y="140" font-family="{SANS}" font-size="56" font-weight="700" letter-spacing="-1.5" fill="#f4f5f8">Developer Marketing Jobs</text>',
        f'    <text x="{PAD}" y="182" font-family="{SANS}" font-size="19" fill="#9aa1b4">DevRel, docs, developer marketing, growth and community roles, pulled nightly from company ATS feeds.</text>',
    ]
    stats = [(f"{total:,}", "open roles", "#f4f5f8"), (f"+{added:,}", "added last run", "#3ddc97"),
             (str(ats), "ATS platforms", "#f4f5f8"), (f"{boards}", "job boards", "#f4f5f8")]
    for i, (num, label, color) in enumerate(stats):
        x = PAD + i * 230
        out.append(f'    <text x="{x}" y="256" font-family="{MONO}" font-size="46" font-weight="700" fill="{color}">{escape(num)}</text>')
        out.append(f'    <text x="{x}" y="282" font-family="{MONO}" font-size="13" letter-spacing="1.4" fill="#7a8194">{escape(label.upper())}</text>')
    # stacked category bar
    total_c = sum(c for _, c in cats) or 1
    rank = {n: r for r, (n, _) in enumerate(sorted(cats, key=lambda t: -t[1]))}
    def shade(name):  # biggest slice = full accent, smaller slices fade
        return f'fill="{ACCENT}" fill-opacity="{max(1 - 0.09 * rank[name], 0.3):.2f}"'
    bar_w, gap, y = W - 2 * PAD, 3, 314
    usable = bar_w - gap * (len(cats) - 1)
    x = float(PAD)
    for i, (name, c) in enumerate(cats):
        w = max(usable * c / total_c, 3)
        out.append(f'    <rect x="{x:.1f}" y="{y}" width="0" height="10" rx="2" {shade(name)}><animate attributeName="width" from="0" to="{w:.1f}" begin="{0.15 * i:.2f}s" dur="0.7s" fill="freeze"/></rect>')
        x += w + gap
    # legend: fixed 5-column grid, two rows, so it never depends on text measurement
    cols = 5
    slot = bar_w / cols
    for i, (name, c) in enumerate(cats):
        lx = PAD + (i % cols) * slot
        ly = 349 + (i // cols) * 26
        out.append(f'    <rect x="{lx:.1f}" y="{ly - 9}" width="9" height="9" rx="2" {shade(name)}/>')
        out.append(f'    <text x="{lx + 16:.1f}" y="{ly}" font-family="{MONO}" font-size="13" fill="#b4bacb">{escape(name)} <tspan fill="#6c7488">{c}</tspan></text>')
    out += ['  </g>', f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#242938"/>', '</svg>', '']
    return "\n".join(out)

def write(total, added, when, categories):
    BANNER_PATH.parent.mkdir(parents=True, exist_ok=True)
    BANNER_PATH.write_text(render(total, added, when, categories), encoding="utf-8")
