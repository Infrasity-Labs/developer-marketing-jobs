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
    
    # Build sections
    content_md, total = build_sections(deduped, yc_deduped)
    
    # Update README
    update_readme(content_md)
    print(f"📊 Total jobs in README: {total}")

if __name__ == "__main__":
    main()