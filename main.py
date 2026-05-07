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
    greenhouse_commoncrawl,
    yc_workatastartup,
    lever,          # NEW
    workable,       # NEW
    remotefront, 
    jobicy,           # NEW
    himalayas,        # NEW
    weworkremotely,   # NEW
    
)

# Remove these broken fetchers:
# lever, workable, recruitee, himalayas, wellfound, remoteok_extended, greenhouse_autodiscovery,

# --- CONFIG ---
CATEGORIES = [
    {
        "label": "🎤 Developer Advocate / DevRel",
        "keywords": [
            "api evangelist",
            "community evangelist",
            "developer advocate",
            "developer community manager",
            "developer educator",
            "developer evangelist",
            "developer experience",
            "developer experience engineer",
            "developer marketing",
            "developer outreach manager",
            "developer programs manager",
            "developer relations",
            "developer relations engineer",
            "developer relations manager",
            "developer success",
            "developer success engineer",
            "devrel",
            "devrel engineer",
            "devrel lead",
            "devrel manager",
            "dx engineer",
            "field engineer devrel",
            "head of developer relations",
            "head of devrel",
            "lead developer advocate",
            "open source advocate",
            "platform evangelist",
            "principal developer advocate",
            "senior developer advocate",
            "staff developer advocate",
            "technical advocate",
            "technical community manager",
            "technical evangelist",
            "vp devrel",
            "vp of developer relations",
        ],
    },
    {
        "label": "✍️ Technical Writing & Documentation",
        "keywords": [
            "api documentation writer",
            "api writer",
            "content engineer",
            "developer documentation",
            "developer documentation manager",
            "docs engineer",
            "docs lead",
            "docs manager",
            "docs platform engineer",
            "documentation architect",
            "documentation engineer",
            "documentation lead",
            "documentation manager",
            "documentation specialist",
            "documentation strategist",
            "documentation writer",
            "head of documentation",
            "information architect",
            "knowledge base manager",
            "lead technical writer",
            "principal technical writer",
            "senior technical writer",
            "staff technical writer",
            "technical author",
            "technical communication",
            "technical content",
            "technical content writer",
            "technical documentation lead",
            "technical editor",
            "technical writer",
        ],
    },
    {
        "label": "📣 Developer Marketing",
        "keywords": [
            "api marketing manager",
            "brand marketing",
            "content director",
            "content lead",
            "content manager",
            "content marketing",
            "content marketing manager",
            "content strategist",
            "developer brand manager",
            "developer content creator",
            "developer content manager",
            "developer education manager",
            "developer growth marketer",
            "developer marketing",
            "developer marketing lead",
            "developer marketing specialist",
            "developer programs manager",
            "director of developer marketing",
            "github led growth",
            "github marketing",
            "head of content",
            "head of developer marketing",
            "inbound marketing",
            "marketing content",
            "senior developer marketing manager",
            "technical content",
            "technical content lead",
            "technical content strategist",
            "technical marketing manager",
            "vp developer marketing",
        ],
    },
    {
        "label": "📦 Product Marketing",
        "keywords": [
            "competitive intelligence manager",
            "director of product marketing",
            "director product marketing",
            "go to market",
            "go-to-market manager",
            "gtm",
            "gtm lead",
            "gtm manager",
            "gtm strategist",
            "head of product marketing",
            "lead product marketer",
            "market intelligence manager",
            "pmm",
            "principal pmm",
            "principal product marketing manager",
            "product launch",
            "product launch manager",
            "product marketer",
            "product marketing",
            "product marketing analyst",
            "product marketing director",
            "product marketing lead",
            "product marketing leadership",
            "product marketing manager",
            "product messaging",
            "product positioning",
            "senior product marketing",
            "senior product marketing manager",
            "solutions marketing",
            "solutions marketing lead",
            "solutions marketing manager",
            "staff product marketing manager",
            "technical marketing",
            "technical product marketing manager",
            "vp product marketing",
        ],
    },
    {
        "label": "📈 Head of Growth",
        "keywords": [
            "acquisition marketing manager",
            "chief growth marketing",
            "demand generation manager",
            "director growth marketing",
            "director of growth",
            "growth analyst",
            "growth director",
            "growth hacker",
            "growth lead",
            "growth manager",
            "growth marketing",
            "growth marketing manager",
            "growth operations",
            "growth operations manager",
            "growth product manager",
            "growth strategist",
            "head of growth",
            "head of growth marketing",
            "lifecycle marketing",
            "lifecycle marketing manager",
            "performance marketing",
            "performance marketing manager",
            "retention marketing manager",
            "senior growth manager",
            "senior growth marketing",
            "senior lifecycle marketing manager",
            "senior performance marketing manager",
            "user acquisition manager",
            "vp growth",
            "vp growth marketing",
        ],
    },
    {
        "label": "👔 VP Marketing",
        "keywords": [
            "brand marketing director",
            "chief marketing",
            "chief marketing officer",
            "cmo",
            "deputy cmo",
            "director of marketing",
            "evp marketing",
            "fractional cmo",
            "global head of marketing",
            "group marketing director",
            "head of brand marketing",
            "head of global marketing",
            "head of marketing",
            "interim cmo",
            "marketing chief",
            "marketing director",
            "marketing executive",
            "marketing lead",
            "marketing leadership",
            "marketing operations director",
            "marketing vp",
            "part time cmo",
            "regional marketing director",
            "senior director marketing",
            "svp marketing",
            "svp of marketing",
            "vice president marketing",
            "vice president of marketing",
            "vp marketing",
            "vp of marketing",
        ],
    },
    {
        "label": "👥 Community",
        "keywords": [
            "ambassador program manager",
            "community advocate",
            "community builder",
            "community director",
            "community engagement",
            "community engagement manager",
            "community evangelist",
            "community growth",
            "community growth manager",
            "community lead",
            "community manager",
            "community marketing manager",
            "community operations",
            "community operations manager",
            "community programs manager",
            "community strategist",
            "community success manager",
            "developer community manager",
            "director of community",
            "discord community manager",
            "forum manager",
            "head of community",
            "head of community engagement",
            "lead community manager",
            "online community manager",
            "principal community manager",
            "senior community manager",
            "slack community manager",
            "technical community manager",
            "vp community",
        ],
    },


]
MAX_AGE_DAYS = 90
MAX_JOBS_PER_CATEGORY = 1000
README_PATH = Path("README.md")
# --------------

def categorize(job, cats=None):
    """Return the first category label this job matches, or None."""
    if cats is None:
        cats = CATEGORIES
    
    text = (job["title"] + " " + " ".join(job.get("tags", []))).lower()
    for cat in cats:
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

def build_sections(jobs, yc_jobs, active_categories=None):
    if active_categories is None:
        active_categories = CATEGORIES
    
    buckets = {cat["label"]: [] for cat in active_categories}
    for j in jobs:
        label = categorize(j, active_categories)
        if label:
            buckets[label].append(j)
    
    # YC buckets
    yc_buckets = {cat["label"]: [] for cat in active_categories}
    for j in yc_jobs:
        label = categorize(j, active_categories)
        if label:
            yc_buckets[label].append(j)

    # ... rest of build_sections stays the same

    # Build markdown sections
    sections = []
    total = 0
    
    # Regular categorized jobs
    for cat in CATEGORIES:
        label = cat["label"]
        cat_jobs = buckets[label]
        
        sections.append(f"## {label}\n")
        sections.append(format_table(cat_jobs))
        
        if cat_jobs:
            total += len(cat_jobs[:MAX_JOBS_PER_CATEGORY])
    
    # Add YC jobs section with categories
    sections.append(f"## 🚀 Y Combinator Jobs\n")
    
    yc_total = 0
    for cat in CATEGORIES:
        label = cat["label"]
        yc_cat_jobs = yc_buckets[label]
        
        if yc_cat_jobs:
            sections.append(f"### {label}\n")
            sections.append(format_table(yc_cat_jobs))
            yc_total += len(yc_cat_jobs[:MAX_JOBS_PER_CATEGORY])
    
    if yc_total == 0:
        sections.append("_No categorized YC jobs found in the last 90 days._\n")
    
    total += yc_total
    
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
    yc_jobs = []
    
    # Only include working fetchers
    fetchers = [
        remoteok, 
        remotive, 
        adzuna, 
        arbeitnow,
        greenhouse,
        ashby, 
        yc_ats,
        greenhouse_commoncrawl,
        yc_workatastartup,
        lever,          # NEW
        workable,       # NEW
        remotefront, 
        jobicy,           # NEW
        himalayas,        # NEW
        weworkremotely,   # NEW
        
    ]
    import os
    
    if os.getenv("ANTHROPIC_API_KEY"):
        print("🤖 Expanding job categories with Claude...")
        from skills.keyword_expander import get_expanded_categories
        active_categories = get_expanded_categories(CATEGORIES)
        print(f"✅ Using expanded categories")
    else:
        print("⚡ Using original categories (set ANTHROPIC_API_KEY for smarter matching)")
        active_categories = CATEGORIES
    
    for fetcher in fetchers:    
        try:
            jobs = fetcher.fetch()
            
            # Separate YC jobs
            for job in jobs:
                if job.get("source") == "YC":
                    yc_jobs.append(job)
                else:
                    all_jobs.append(job)
            
            print(f"✓ Fetched from {fetcher.__name__}: {len(jobs)} jobs")
        except Exception as e:
            print(f"✗ Failed {fetcher.__name__}: {e}")

    # Filter: must match a category AND be recent (non-YC jobs)
    filtered = [j for j in all_jobs if categorize(j) and is_recent(j)]
    deduped = dedupe(filtered)
    deduped.sort(key=sort_key, reverse=True)
    
    # Dedupe YC jobs separately
    yc_deduped = dedupe(yc_jobs)
    yc_deduped.sort(key=sort_key, reverse=True)

    print(f"\nTotal fetched: {len(all_jobs) + len(yc_jobs)}")
    print(f"Categorized: {len(filtered)}")
    print(f"After dedup: {len(deduped)}")
    print(f"YC jobs: {len(yc_deduped)}")
    
    content_md, total = build_sections(deduped, yc_deduped)
    
    update_readme(content_md)
    print(f"📊 Total jobs in README: {total}")

if __name__ == "__main__":
    main()