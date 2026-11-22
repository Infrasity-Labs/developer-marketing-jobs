import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, ".")
from main import README_PATH, categorize, is_recent, dedupe, update_readme, sort_key
import readme_assets
from report import build_report

# Apply links in the job tables, in both the current and the old table format
APPLY_RE = re.compile(r"\[(?:Apply ↗|→)\]\((https?://[^)\s]+)\)")

def job_urls(readme_text):
    """Set of job URLs inside the JOBS section of a README."""
    start = readme_text.find("<!-- JOBS:START -->")
    end = readme_text.find("<!-- JOBS:END -->")
    if start == -1 or end == -1:
        return set()
    return set(APPLY_RE.findall(readme_text[start:end]))

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

    # URLs already in the README (previous run), so new roles can be tagged
    previous_urls = job_urls(Path(README_PATH).read_text(encoding="utf-8"))

    when = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    content_md, total, stats = build_report(deduped, yc_deduped, when, previous_urls)

    update_readme(content_md)
    readme_assets.write_all(stats)
    print(f"📊 Total jobs in README: {total} (+{stats['added']} new, {stats['companies']} companies)")

if __name__ == "__main__":
    main()
