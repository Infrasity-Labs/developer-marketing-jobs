import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Import only the categorize, dedupe, format functions from main.py
import sys
sys.path.insert(0, '.')
from main import (
    CATEGORIES, MAX_AGE_DAYS, MAX_JOBS_PER_CATEGORY, 
    README_PATH, categorize, is_recent, dedupe, 
    format_table, build_sections, update_readme, sort_key
)


JOB_URL_RE = re.compile(r"\]\((https?://[^)\s]+)\)")

def job_urls(readme_text):
    """Set of job URLs inside the JOBS section of a README."""
    start = readme_text.find("<!-- JOBS:START -->")
    end = readme_text.find("<!-- JOBS:END -->")
    if start == -1 or end == -1:
        return set()
    return set(JOB_URL_RE.findall(readme_text[start:end]))

def _slug(heading):
    """GitHub-style anchor for a heading (emoji dropped, spaces to hyphens)."""
    text = re.sub(r"[^\w\- ]", "", heading.lower(), flags=re.UNICODE)
    return text.replace(" ", "-")

def build_toc(jobs_text):
    """Linked table of contents with per-category counts."""
    lines = []
    section = None
    count = 0
    def flush():
        if section:
            lines.append(f"| [{section}](#{_slug(section)}) | {count} |")
    for line in jobs_text.splitlines():
        if line.startswith("## "):
            flush()
            section, count = line[3:].strip(), 0
        elif section and line.startswith("| ") and not line.startswith(("| Role", "| ---")):
            count += 1
    flush()
    if not lines:
        return ""
    return "\n".join(["| Category | Open roles |", "|----------|-----------:|"] + lines)

def _replace_block(text, name, body):
    s, e = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    si, ei = text.find(s), text.find(e)
    if si == -1 or ei == -1:
        print(f"⚠️ {name} markers not found in README.md, skipping")
        return text
    return text[:si + len(s)] + body + text[ei:]

BANNER_PATH = Path(".github/assets/banner-1920x1080.svg")

def update_banner(total, added, when):
    """Write the live stat cards into the banner SVG between LIVE markers."""
    if not BANNER_PATH.exists():
        return
    svg = BANNER_PATH.read_text(encoding="utf-8")
    s, e = "<!-- LIVE:START -->", "<!-- LIVE:END -->"
    si, ei = svg.find(s), svg.find(e)
    if si == -1 or ei == -1:
        print("⚠️ LIVE markers not found in banner SVG, skipping")
        return
    cards = [(f"{total:,}", "Open roles"), (f"+{added:,}", "Added last run"), ("5 + 14", "ATS + job boards")]
    w, gap, y, h = 420, 40, 800, 150
    x0 = (1920 - (3 * w + 2 * gap)) // 2
    out = []
    for i, (num, label) in enumerate(cards):
        x = x0 + i * (w + gap)
        cx = x + w // 2
        out.append(
            f'    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{1.0 + i * 0.25}s" dur="0.9s" fill="freeze"/>\n'
            f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.22" stroke-width="2"/>\n'
            f'      <text x="{cx}" y="{y + 76}" text-anchor="middle" class="num">{num}</text>\n'
            f'      <text x="{cx}" y="{y + 118}" text-anchor="middle" class="lbl">{label}</text>\n'
            f'    </g>'
        )
    stamp = f"Updated {when}"
    tx = 960 + 18
    out.append(
        f'    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.8s" dur="0.9s" fill="freeze"/>\n'
        f'      <circle cx="{tx - int(len(stamp) * 7.4) - 26}" cy="995" r="8" fill="#3dffa0">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>\n'
        f'      <text x="{tx}" y="1004" text-anchor="middle" class="live">{stamp}</text>\n'
        f'    </g>'
    )
    BANNER_PATH.write_text(svg[:si + len(s)] + "\n" + "\n".join(out) + "\n    " + svg[ei:], encoding="utf-8")

def update_stats(total, added):
    """Rewrite the STATS and TOC blocks of the README."""
    path = Path(README_PATH)
    text = path.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc)
    when = now.strftime("%d %b %Y, %H:%M UTC")
    stats = (
        f"\n<p align=\"center\">\n"
        f"  <img alt=\"Open roles\" src=\"https://img.shields.io/badge/open%20roles-{total}-brightgreen?style=for-the-badge\">\n"
        f"  <img alt=\"Added in last run\" src=\"https://img.shields.io/badge/added%20last%20run-%2B{added}-blue?style=for-the-badge\">\n"
        f"</p>\n\n"
        f"<p align=\"center\">\n"
        f"  <b>{total:,}</b> open roles tracked &nbsp;·&nbsp; "
        f"<b>+{added:,}</b> added in the last run &nbsp;·&nbsp; "
        f"last updated <b>{when}</b>\n"
        f"</p>\n"
    )
    text = _replace_block(text, "STATS", stats)
    update_banner(total, added, now.strftime("%d %b %Y, %H:%M UTC"))
    js, je = text.find("<!-- JOBS:START -->"), text.find("<!-- JOBS:END -->")
    if js != -1 and je != -1:
        toc = build_toc(text[js:je])
        text = _replace_block(text, "TOC", f"\n{toc}\n" if toc else "\n")
    path.write_text(text, encoding="utf-8")
    print(f"📈 Stats: total={total}, added={added}, run={when}")

def load_all_jobs():
    """Load jobs from all artifact JSON files."""
    all_jobs = []
    yc_jobs = []
    
    artifacts_dir = Path('artifacts')
    
    if not artifacts_dir.exists():
        print("❌ No artifacts directory found")
        return [], []
    
    # Find all JSON files in artifact subdirectories
    for json_file in artifacts_dir.rglob('*.json'):
        # Skip cache files
        if 'cache' in json_file.name or 'companies' in json_file.name:
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            
            print(f"✓ Loaded {len(jobs)} jobs from {json_file.name}")
            
            # Separate YC jobs
            for job in jobs:
                if job.get("source") == "YC":
                    yc_jobs.append(job)
                else:
                    all_jobs.append(job)
        
        except Exception as e:
            print(f"✗ Error loading {json_file}: {e}")
    
    # Hand-curated roles that no fetcher picks up yet
    manual_file = Path('manual_jobs.json')
    if manual_file.exists():
        try:
            manual = json.loads(manual_file.read_text(encoding='utf-8'))
            all_jobs.extend(manual)
            print(f"✓ Loaded {len(manual)} jobs from manual_jobs.json")
        except Exception as e:
            print(f"✗ Error loading manual_jobs.json: {e}")

    return all_jobs, yc_jobs

def main():
    print("📦 Loading jobs from artifacts...")
    all_jobs, yc_jobs = load_all_jobs()
    
    print(f"\nTotal non-YC jobs: {len(all_jobs)}")
    print(f"Total YC jobs: {len(yc_jobs)}")
    
    # Filter recent + categorized
    filtered = [j for j in all_jobs if categorize(j) and is_recent(j)]
    deduped = dedupe(filtered)
    deduped.sort(key=sort_key, reverse=True)
    
    # YC jobs (no recency filter, just dedup)
    yc_deduped = dedupe(yc_jobs)
    yc_deduped.sort(key=sort_key, reverse=True)
    
    print(f"Categorized: {len(filtered)}")
    print(f"After dedup: {len(deduped)}")
    print(f"YC jobs: {len(yc_deduped)}")
    
    # URLs already in the README (previous run), to count what this run added
    previous_urls = job_urls(Path(README_PATH).read_text(encoding="utf-8"))

    # Build sections
    content_md, total = build_sections(deduped, yc_deduped)
    
    # Update README
    update_readme(content_md)
    new_urls = job_urls(Path(README_PATH).read_text(encoding="utf-8"))
    update_stats(total, len(new_urls - previous_urls))
    print(f"📊 Total jobs in README: {total}")

if __name__ == "__main__":
    main()