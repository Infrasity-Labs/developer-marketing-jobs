import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from fetchers import (
    remoteok, 
    remotive, 
    adzuna,  # Make sure fetchers/adzuna.py exists!
    arbeitnow, 
    greenhouse,
    ashby, 
    yc_ats,
    greenhouse_commoncrawl
)

# Remove these broken fetchers:
# lever, workable, recruitee, himalayas, wellfound, remoteok_extended, greenhouse_autodiscovery,

# --- CONFIG ---
CATEGORIES = [
    {
        "label": "🎤 Developer Advocate / DevRel",
        "keywords": [
            "developer advocate", "developer relations", "devrel",
            "developer evangelist", "developer experience",
            "technical evangelist", "community evangelist",
            "developer marketing", "technical advocate", "developer success"
        ],
    },
    {
        "label": "✍️ Technical Writing & Documentation",
        "keywords": [
            "technical writer", "developer documentation", "docs engineer",
            "content engineer", "technical author", "api writer",
            "technical communication", "documentation manager",
            "technical content"
        ],
    },
    {
        "label": "📣 Developer Marketing",
        "keywords": [
            "developer marketing", "content marketing", "content manager",
            "content strategist", "marketing content", "content lead",
            "technical content", "content director","head of content ", "github marketing","github led growth", "inbound marketing", "brand marketing",
        ],
    },
    {
        "label": "📦 Product Marketing",
        "keywords": [
            "product marketing", "product marketer", "pmm",
            "solutions marketing", "technical marketing", "go to market",
            "gtm", "product launch", "product messaging", "product positioning",
             "product marketing manager","product marketing director", "head of product marketing", "vp product marketing", "director of product marketing", "product marketing leadership","product marketing manager", "senior product marketing"
        ],
    },
    {
        "label": "📈 Head of Growth",
        "keywords": [
            "head of growth", "growth lead", "director of growth",
            "vp growth", "growth marketing",
            "performance marketing", "growth manager", 
            "lifecycle marketing", "growth hacker", "growth strategist", "growth operations", "growth marketing manager", "senior growth marketing", "head of growth marketing", "vp growth marketing", "director growth marketing", "chief growth marketing"
        ],
    },
    {
        "label": "👔 VP Marketing",
        "keywords": [
            "vp marketing", "vice president marketing", "chief marketing",
            "cmo", "head of marketing", "director of marketing",
            "marketing director", "marketing leadership","fractional cmo", "part time cmo", "interim cmo"
        ],
    },
    {
        "label": "👥 Community",
        "keywords": [
            "community manager", "community lead", "community advocate",
            "community director", "community builder", "community growth",
            "community operations", "community engagement",
        ],
    },
    
    {
        "label": "🎯 Product Led Growth",
        "keywords": [
            "product led growth",
            "plg",
            "product growth",
            "self serve growth",
            "product adoption",
            
        ],
    },
]
MAX_AGE_DAYS = 90
MAX_JOBS_PER_CATEGORY = 1000
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
    """Check if job was posted within MAX_AGE_DAYS."""
    posted = job.get("posted", "")
    
    # Handle empty/missing dates
    if not posted:
        return True
    
    # Handle integer timestamps (Unix epoch)
    if isinstance(posted, int):
        try:
            dt = datetime.fromtimestamp(posted, tz=timezone.utc)
        except:
            return True
    
    # Handle string dates
    elif isinstance(posted, str):
        try:
            # Remove 'Z' and replace with '+00:00' for ISO format
            posted_cleaned = posted.replace("Z", "+00:00")
            dt = datetime.fromisoformat(posted_cleaned)
        except:
            # Try parsing as timestamp string
            try:
                dt = datetime.fromtimestamp(int(posted), tz=timezone.utc)
            except:
                return True
    else:
        return True
    
    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    age = (datetime.now(timezone.utc) - dt).days
    return age <= MAX_AGE_DAYS

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
        return "_No open roles in the last 90 days._\n"
    
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

def sort_key(job):
    """Convert posted date to comparable format for sorting."""
    posted = job.get("posted", "")
    
    # Handle integer timestamps
    if isinstance(posted, int):
        return posted
    
    # Handle string dates
    if isinstance(posted, str) and posted:
        try:
            dt = datetime.fromisoformat(posted.replace("Z", "+00:00"))
            return int(dt.timestamp())
        except:
            return 0
    
    # Default for missing dates
    return 0

def main():
    all_jobs = []
    
    # Only include working fetchers
    fetchers = [
        remoteok, 
        remotive, 
        adzuna, 
        arbeitnow,
        greenhouse,
        ashby, 
        yc_ats,
        greenhouse_commoncrawl
    ]
    
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
    deduped.sort(key=sort_key, reverse=True)

    print(f"\nTotal fetched: {len(all_jobs)}")
    print(f"Categorized: {len(filtered)}")
    print(f"After dedup: {len(deduped)}")
    
    content_md, total = build_sections(deduped)
    
    update_readme(content_md)
    print(f"📊 Total jobs in README: {total}")

if __name__ == "__main__":
    main()