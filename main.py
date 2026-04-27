import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from fetchers import remoteok, remotive, adzuna, arbeitnow, greenhouse

# --- CONFIG ---
CATEGORIES = [
    {
        "label": "🎤 Developer Advocate / DevRel",
        "keywords": [
            "developer advocate",
            "developer relations",
            "devrel",
            "developer evangelist",
            "developer experience",
            "advocacy",
        ],
    },
    {
        "label": "✍️ Technical Writing & Documentation",
        "keywords": [
            "technical writer",
            "documentation",
            "docs engineer",
            "content engineer",
            "technical author",
            "writer",
        ],
    },
    {
        "label": "📣 Developer Marketing",
        "keywords": [
            "developer marketing",
            "content marketing",
            "content manager",
            "content strategist",
            "marketing content",
            "content lead",
        ],
    },
    {
        "label": "📦 Product Marketing",
        "keywords": [
            "product marketing",
            "product marketer",
            "pmm",
        ],
    },
    {
        "label": "📈 Head of Growth",
        "keywords": [
            "head of growth",
            "growth lead",
            "director of growth",
            "vp growth",
            "vp of growth",
        ],
    },
    {
        "label": "👔 VP Marketing",
        "keywords": [
            "vp marketing",
            "vp of marketing",
            "vice president marketing",
            "chief marketing",
            "cmo",
        ],
    },
    {
        "label": "👥 Community",
        "keywords": [
            "community manager",
            "community lead",
            "community advocate",
            "community director",
        ],
    },
]
MAX_AGE_DAYS = 30
MAX_JOBS_PER_CATEGORY = 8
README_PATH = Path("README.md")
# --------------

def categorize(job):
    """Return the first category label this job matches, or None."""
    text = (job["title"] + " " + " ".join(job.get("tags", []))).lower()
    for cat in CATEGORIES:
        if any(kw in text for kw in cat["keywords"]):
            return cat["label"]
    return None

def is_recent(job):
    posted = job.get("posted", "")
    if not posted:
        return True
    try:
        dt = datetime.fromisoformat(posted.replace("Z", "+00:00"))
    except ValueError:
        return True
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    age = datetime.now(timezone.utc) - dt
    return age <= timedelta(days=MAX_AGE_DAYS)

def dedupe(jobs):
    seen = set()
    out = []
    for j in jobs:
        key = (j["company"].lower().strip(), j["title"].lower().strip())
        if key in seen:
            continue
        seen.add(key)
        out.append(j)
    return out

def format_table(jobs):
    """Format a list of jobs as a markdown table."""
    if not jobs:
        return "_No open roles in the last 30 days._\n"
    
    lines = [
        "| Role | Company | Location | Apply |",
        "|------|---------|----------|-------|",
    ]
    for j in jobs[:MAX_JOBS_PER_CATEGORY]:
        title = (j.get("title", "") or "").replace("|", "/")[:80]
        company = (j.get("company", "") or "").replace("|", "/")[:40]
        location = (j.get("location", "") or "").replace("|", "/")[:30]
        url = j.get("url", "#")
        
        lines.append(f"| {title} | {company} | {location} | [→]({url}) |")
    
    return "\n".join(lines) + "\n"

def build_sections(jobs):
    """Group jobs by category and build markdown for each section."""
    # Bucket jobs by category
    buckets = {cat["label"]: [] for cat in CATEGORIES}
    for j in jobs:
        label = categorize(j)
        if label:
            buckets[label].append(j)

    # Build markdown sections
    sections = []
    total = 0
    
    for cat in CATEGORIES:
        label = cat["label"]
        cat_jobs = buckets[label]
        
        sections.append(f"## {label}\n")
        sections.append(format_table(cat_jobs))
        
        if cat_jobs:
            total += len(cat_jobs[:MAX_JOBS_PER_CATEGORY])
    
    return "\n".join(sections), total

def update_readme(content_md):
    """Replace job section in README between markers."""
    content = README_PATH.read_text(encoding="utf-8")
    
    start_marker = "<!-- JOBS:START -->"
    end_marker = "<!-- JOBS:END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("❌ ERROR: Job markers not found in README.md")
        print(f"  Looking for: {start_marker}")
        print(f"  and: {end_marker}")
        return
    
    # Rebuild: keep before + new jobs + keep after
    new_content = (
        content[:start_idx + len(start_marker)] +
        "\n\n" + content_md + "\n" +
        content[end_idx:]
    )
    
    README_PATH.write_text(new_content, encoding="utf-8")
    size_kb = len(new_content) / 1024
    print(f"✅ Updated README.md ({size_kb:.1f} KB)")

def main():
    all_jobs = []
    fetchers = [remoteok, remotive, adzuna, arbeitnow,greenhouse]
    
    for fetcher in fetchers:
        try:
            jobs = fetcher.fetch()
            all_jobs.extend(jobs)
            print(f"✓ Fetched from {fetcher.__name__}: {len(jobs)} jobs")
        except Exception as e:
            print(f"✗ Failed {fetcher.__name__}: {e}")

    # Filter: must match a category AND be recent
    filtered = [j for j in all_jobs if categorize(j) and is_recent(j)]
    deduped = dedupe(filtered)
    deduped.sort(key=lambda j: j.get("posted", ""), reverse=True)

    print(f"\nTotal fetched: {len(all_jobs)}")
    print(f"Categorized: {len(filtered)}")
    print(f"After dedup: {len(deduped)}")
    
    content_md, total = build_sections(deduped)
    
    update_readme(content_md)
    print(f"📊 Total jobs in README: {total}")

if __name__ == "__main__":
    main()