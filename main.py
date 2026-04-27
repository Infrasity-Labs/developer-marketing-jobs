import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from fetchers import remoteok, remotive, greenhouse

# --- CONFIG ---
ROLE_KEYWORDS = [
    "developer advocate",
    "developer relations",
    "devrel",
    "technical writer",
    "content marketing",
    "documentation",
    "content manager",
]
MAX_AGE_DAYS = 30
MAX_JOBS_IN_README = 20
README_PATH = Path("README.md")
# --------------

def matches_role(job):
    text = (job["title"] + " " + " ".join(job["tags"])).lower()
    return any(kw in text for kw in ROLE_KEYWORDS)

def is_recent(job):
    posted = job.get("posted", "")
    if not posted:
        return True  # keep if unknown
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
    if not jobs:
        return "_No matching jobs found today._"
    lines = ["| Role | Company | Location | Source | Link |",
             "|------|---------|----------|--------|------|"]
    for j in jobs:
        title = j["title"].replace("|", "/")
        company = j["company"].replace("|", "/")
        location = j["location"].replace("|", "/")
        lines.append(f"| {title} | {company} | {location} | {j['source']} | [Apply]({j['url']}) |")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"\n_Last updated: {stamp}_")
    return "\n".join(lines)

def update_readme(table_md):
    content = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"<!-- JOBS:START -->.*?<!-- JOBS:END -->", re.DOTALL)
    replacement = f"<!-- JOBS:START -->\n{table_md}\n<!-- JOBS:END -->"
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

    filtered = [j for j in all_jobs if matches_role(j) and is_recent(j)]
    deduped = dedupe(filtered)
    deduped.sort(key=lambda j: j.get("posted", ""), reverse=True)  # newest first
    final = deduped[:MAX_JOBS_IN_README]

    print(f"Total: {len(all_jobs)} → filtered: {len(filtered)} → final: {len(final)}")
    update_readme(format_table(final))

if __name__ == "__main__":
    main()