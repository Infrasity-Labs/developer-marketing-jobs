"""Generate every SVG the README uses (banner, bars, charts, pipeline).

Each graphic is written twice, light and dark, and embedded with a <picture>
element so GitHub shows the one that matches the reader's theme. Only system
fonts are used, so the files render the same inside GitHub's <img> sandbox.
All numbers come from the stats dict built by report.py on every nightly run.
"""
from pathlib import Path
from xml.sax.saxutils import escape

import hero_banner

ASSET_DIR = Path(".github/assets")
REPO_SLUG = "infrasity-labs / developer-marketing-jobs"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(panel="#f6f8fa", line="#d1d9e0", card="#ffffff", fg="#1f2328", muted="#59636e",
                  dim="#818b98", accent="#6a5af0", accent_bg="#ece9ff", track="#eef1f4",
                  green="#1a7f37"),
    "dark": dict(panel="#151b23", line="#30363d", card="#0d1117", fg="#f0f6fc", muted="#9198a1",
                 dim="#6e7681", accent="#8b7dff", accent_bg="#262046", track="#1d242d",
                 green="#3fb950"),
}

# README section label -> file stem for its bar graphic
BAR_KEYS = {
    "Developer Advocate / DevRel": "devrel",
    "Technical Writing & Documentation": "docs",
    "Developer Marketing": "devmkt",
    "Product Marketing": "pmm",
    "Growth & Demand Generation": "growth",
    "Marketing Leadership": "leadership",
    "Community": "community",
    "Full Stack Marketing": "fullstack",
    "SEO / GEO / AEO": "seo",
    "Y Combinator Startups": "yc",
}

def bar_key(label):
    return BAR_KEYS.get(label) or "".join(c for c in label.lower() if c.isalnum())[:12]

def _t(x, y, text, size, fill, weight=None, anchor=None, family=SANS, spacing=None, tabular=False):
    attrs = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if tabular:
        attrs.append('style="font-variant-numeric:tabular-nums"')
    return f'<text {" ".join(attrs)}>{escape(str(text))}</text>'

def _svg(w, h, label, body, desc=None):
    d = f'<desc id="d">{escape(desc)}</desc>\n' if desc else ""
    aria = 'aria-labelledby="t d"' if desc else f'aria-label="{escape(label)}"'
    title = f'<title id="t">{escape(label)}</title>\n' if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" {aria}>\n{title}{d}{body}\n</svg>\n')

def _panel(w, h, c, rx=14):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{c["panel"]}" stroke="{c["line"]}"/>'

# --------------------------------------------------------------------------- banner

def banner(s, c):
    tiles = [
        (f"{s['total']:,}", "open roles", False),
        (f"+{s['added']:,}", "new since last run", True),
        (f"{s['companies']:,}", "companies hiring", False),
        (f"{s['remote_pct']}%", "remote-friendly", False),
    ]
    out = [_panel(1280, 360, c, 16),
           f'<rect x="64" y="56" width="34" height="34" rx="8" fill="{c["accent"]}"/>',
           '<path d="M73 66 l7 7 l-7 7" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
           '<rect x="83" y="78" width="8" height="3" rx="1.5" fill="#ffffff"/>',
           _t(112, 82, REPO_SLUG.replace(" / ", " / "), 15, c["muted"], family=MONO),
           _t(64, 138, "Developer Marketing Jobs", 50, c["fg"], 700, spacing=-1.2),
           _t(64, 172, "DevRel, docs, developer marketing, growth and community roles at devtool companies. Refreshed nightly.", 19, c["muted"])]
    for i, (num, label, hot) in enumerate(tiles):
        x = 64 + i * 286
        if hot:
            out.append(f'<rect x="{x}" y="200" width="266" height="96" rx="12" fill="{c["accent_bg"]}" stroke="{c["accent"]}" stroke-opacity="0.55"/>')
        else:
            out.append(f'<rect x="{x}" y="200" width="266" height="96" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>')
        out.append(_t(x + 22, 252, num, 36, c["accent"] if hot else c["fg"], 700, spacing=-0.8, tabular=True))
        out.append(_t(x + 22, 278, label, 15, c["muted"]))
    out.append(f'<circle cx="70" cy="328" r="4" fill="{c["green"]}"/>')
    out.append(_t(82, 333, f"last run {s['when']}  ·  next run 06:00 UTC  ·  {s['ats']} ATS platforms + {s['boards']} job boards", 13, c["dim"], family=MONO))
    desc = (f"{s['total']:,} open developer marketing, DevRel and technical writing roles; "
            f"{s['added']:,} new since the last run; updated {s['when']}.")
    return _svg(1280, 360, "Developer Marketing Jobs", "\n".join(out), desc)

# --------------------------------------------------------------------------- per-role bars

def bar(count, new, scale_max, c):
    w = 240
    total_w = round(count / scale_max * w) if scale_max else 0
    if count:
        total_w = max(total_w, 6)
    new_w = round(new / scale_max * w) if scale_max else 0
    if new:
        new_w = max(min(new_w, total_w), 5)
    body = f'<rect x="0" y="0" width="{w}" height="12" rx="4" fill="{c["track"]}"/>'
    if total_w:
        body += f'<rect x="0" y="0" width="{total_w}" height="12" rx="4" fill="{c["accent"]}" fill-opacity="0.45"/>'
    if new_w:
        body += f'<rect x="0" y="0" width="{new_w}" height="12" rx="4" fill="{c["accent"]}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="12" viewBox="0 0 {w} 12">{body}</svg>\n'

def new_tag(c):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="38" height="18" viewBox="0 0 38 18">'
            f'<rect width="38" height="18" rx="9" fill="{c["accent"]}"/>'
            f'<text x="19" y="12.6" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="700" '
            'letter-spacing="0.6" fill="#ffffff">NEW</text></svg>\n')

# --------------------------------------------------------------------------- charts

def _hbar_chart(title, subtitle, rows, c, label_max=24):
    n = max(len(rows), 1)
    h = 109 + 34 * (n - 1) + 45
    out = [_panel(620, h, c),
           _t(28, 44, title, 19, c["fg"], 650),
           _t(28, 68, subtitle, 13.5, c["muted"])]
    top = max((v for _, v in rows), default=1) or 1
    for i, (label, value) in enumerate(rows):
        y = 109 + 34 * i
        w = max(round(value / top * 360), 6)
        name = label if len(label) <= label_max else label[:label_max - 1].rstrip() + "…"
        out.append(_t(28, y, name, 14, c["fg"]))
        out.append(f'<rect x="190" y="{y - 12}" width="{w}" height="16" rx="4" fill="{c["accent"]}"/>')
        out.append(_t(190 + w + 8, y + 1, f"{value:,}", 13.5, c["muted"], 600, tabular=True))
    return _svg(620, h, title, "\n".join(out)), h

def top_companies(s, c):
    return _hbar_chart("Who is hiring most",
                       f"Open roles per company, top {len(s['top_companies'])} of {s['companies']:,}",
                       s["top_companies"], c)[0]

def regions(s, c):
    return _hbar_chart("Where the roles are", f"{s['total']:,} roles by location as posted", s["regions"], c)[0]

def source_mix(s, c):
    mix = [(l, v) for l, v in s["source_mix"] if v > 0]
    total = sum(v for _, v in mix) or 1
    gap = 2
    usable = 1222 - gap * (len(mix) - 1)
    opac = [1.0, 0.72, 0.48, 0.28, 0.18]
    out = [_panel(1280, 150, c), _t(28, 44, "Where today's listings come from", 19, c["fg"], 650)]
    x = 28.0
    lx = 28.0
    for i, (label, v) in enumerate(mix):
        o = opac[min(i, len(opac) - 1)]
        w = max(usable * v / total, 4)
        out.append(f'<rect x="{x:.1f}" y="70" width="{w:.1f}" height="22" rx="4" fill="{c["accent"]}" fill-opacity="{o}"/>')
        x += w + gap
        text = f"{label}  {v:,} · {round(v / total * 100)}%"
        out.append(f'<rect x="{lx:.1f}" y="114" width="12" height="12" rx="3" fill="{c["accent"]}" fill-opacity="{o}"/>')
        out.append(_t(f"{lx + 20:.1f}", 125, text, 14, c["fg"]))
        lx += 20 + len(text) * 7.3 + 36
    return _svg(1280, 150, "Where listings come from", "\n".join(out))

def pipeline(s, c):
    steps = [
        ("Fetch", f"{s['ats']} ATS platforms, {s['boards']} job", "boards, hand-picked roles"),
        ("Filter", "Role keywords match", "and posted ≤ 90 days ago"),
        ("Dedupe", "Same role on several", "sources merged into one"),
        ("Publish", "Tables, banner and charts", "rebuilt and committed"),
    ]
    out = [_panel(1280, 230, c), _t(28, 44, "Every night at 06:00 UTC", 19, c["fg"], 650),
           _t(1252, 44, ".github/workflows/update-jobs.yml", 13, c["dim"], anchor="end", family=MONO)]
    for i, (name, l1, l2) in enumerate(steps):
        x = 28 + i * 310
        last = i == len(steps) - 1
        if last:
            out.append(f'<rect x="{x}" y="70" width="266" height="120" rx="12" fill="{c["accent_bg"]}" stroke="{c["accent"]}" stroke-opacity="0.55"/>')
        else:
            out.append(f'<rect x="{x}" y="70" width="266" height="120" rx="12" fill="{c["card"]}" stroke="{c["line"]}"/>')
        out.append(f'<circle cx="{x + 30}" cy="102" r="13" fill="{c["accent"]}"/>')
        out.append(_t(x + 30, 107, i + 1, 13, "#ffffff", 700, anchor="middle"))
        out.append(_t(x + 54, 108, name, 18, c["fg"], 650))
        out.append(_t(x + 20, 146, l1, 14, c["muted"]))
        out.append(_t(x + 20, 167, l2, 14, c["muted"]))
        if not last:
            out.append(f'<path d="M{x + 274} 130 h28" stroke="{c["dim"]}" stroke-width="2" fill="none"/>')
            out.append(f'<path d="M{x + 296} 124 l7 6 l-7 6" stroke="{c["dim"]}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return _svg(1280, 230, "How the nightly run works", "\n".join(out))

# --------------------------------------------------------------------------- driver

def _write(name, text):
    path = ASSET_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def write_all(s):
    """Write every graphic. `s` is the stats dict from report.build_report."""
    scale = max((cat["count"] for cat in s["cats"]), default=1) or 1
    _write("hero.svg", hero_banner.render("jobs", ("Find your next", "marketing role"),
           f"{s['total']:,} open roles from {s['ats']} ATS platforms and {s['boards']} boards", f"{s['total']:,} open roles"))
    for theme, c in THEMES.items():
        _write(f"banner-{theme}.svg", banner(s, c))
        _write(f"top-companies-{theme}.svg", top_companies(s, c))
        _write(f"regions-{theme}.svg", regions(s, c))
        _write(f"source-mix-{theme}.svg", source_mix(s, c))
        _write(f"pipeline-{theme}.svg", pipeline(s, c))
        for cat in s["cats"]:
            _write(f"bars/{bar_key(cat['label'])}-{theme}.svg", bar(cat["count"], cat["new"], scale, c))
    _write("new.svg", new_tag(THEMES["light"]))
