import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from fetchers import remoteok, remotive, greenhouse

# --- CONFIG ---
# Each category has a label (shown as heading) and keywords (any match = belongs there).
# Order matters: a job goes into the FIRST category it matches.
CATEGORIES = [
    {
        "label": "👑 DevRel Leadership",
        "keywords": [
            "head of developer",
            "head of devrel",
            "vp of devrel",
            "vp developer relations",
            "director of developer",
            "director of devrel",
            "chief developer advocate",
        ],
    },
    {
        "label": "🎤 Developer Advocate / DevRel",
        "keywords": ["developer advocate", "developer relations", "devrel", "community manager"],
    },
    {
        "label": "✍️ Technical Writing & Documentation",
        "keywords": ["technical writer", "documentation", "docs engineer", "content engineer"],
    },
    {
        "label": "📣 Content Marketing",
        "keywords": ["content marketing", "content manager", "content strategist", "content lead"],
    },
]

MAX_AGE_DAYS = 30
MAX_JOBS_PER_CATEGORY = 10
README_PATH = Path("README.md")
# --------------

def categorize(job):
    """Return the first category label this job matches, or None."""
    text = (job["title"] + " " + " ".join(job["tags"])).lower()
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
    lines = ["| Role | Company | Location | Source | Link |",
             "|------|---------|----------|--------|------|"]
    for j in jobs:
        title = j["title"].replace("|", "/")
        company = j["company"].replace("|", "/")
        location = j["location"].replace("|", "/")
        lines.append(f"| {title} | {company} | {location} | {j['source']} | [Apply]({j['url']}) |")
    return "\n".join(lines)

def build_sections(jobs):
    """Group jobs by category and build markdown for each section."""
    # Bucket jobs by category
    buckets = {cat["label"]: [] for cat in CATEGORIES}
    for j in jobs:
        label = categorize(j)
        if label:
            buckets[label].append(j)

    # Build markdown
    sections = []
    total = 0
    for cat in CATEGORIES:
        label = cat["label"]
        cat_jobs = buckets[label][:MAX_JOBS_PER_CATEGORY]
        sections.append(f"### {label}")
        sections.append("")
        if cat_jobs:
            sections.append(format_table(cat_jobs))
            total += len(cat_jobs)
        else:
            sections.append("_No matching jobs found this cycle._")
        sections.append("")  # blank line between sections

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections.append(f"_Last updated: {stamp} • Total: {total} jobs_")
    return "\n".join(sections)

def update_readme(content_md):
    content = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"<!-- JOBS:START -->.*?<!-- JOBS:END -->", re.DOTALL)
    replacement = f"<!-- JOBS:START -->\n{content_md}\n<!-- JOBS:END -->"
    new_content = pattern.sub(replacement, content)
    README_PATH.write_text(new_content, encoding="utf-8")

def main():
    all_jobs = []
    for fetcher in [remoteok, remotive, greenhouse]:
        try:
            all_jobs.extend(fetcher.fetch())
            print(f"Fetched from {fetcher.__name__}")
        except Exception as e:
            print(f"Failed {fetcher.__name__}: {e}")

    # Filter: must match a category AND be recent
    filtered = [j for j in all_jobs if categorize(j) and is_recent(j)]
    deduped = dedupe(filtered)
    deduped.sort(key=lambda j: j.get("posted", ""), reverse=True)

    print(f"Total: {len(all_jobs)} → categorized: {len(filtered)} → after dedupe: {len(deduped)}")
    update_readme(build_sections(deduped))

if __name__ == "__main__":
    main()