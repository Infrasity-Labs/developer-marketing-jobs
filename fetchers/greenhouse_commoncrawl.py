import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("greenhouse_all_companies.json")
CACHE_DAYS = 30  # Refresh monthly

def discover_all_greenhouse_companies():
    """Use Common Crawl to find ALL Greenhouse job boards."""
    companies = set()
    
    try:
        # Common Crawl Index API
        # Query for all URLs matching boards.greenhouse.io
        url = "https://index.commoncrawl.org/CC-MAIN-2024-10-index"
        params = {
            "url": "boards.greenhouse.io/*",
            "output": "json",
            "limit": 10000,  # Get up to 10k results
        }
        
        r = requests.get(url, params=params, timeout=60)
        
        # Parse JSONL response (one JSON object per line)
        for line in r.text.strip().split('\n'):
            if not line:
                continue
            
            try:
                record = json.loads(line)
                url_found = record.get('url', '')
                
                # Extract company slug from boards.greenhouse.io/COMPANY/...
                if 'boards.greenhouse.io/' in url_found:
                    parts = url_found.split('boards.greenhouse.io/')[1].split('/')
                    if parts and parts[0]:
                        companies.add(parts[0])
            except:
                continue
        
        print(f"    📍 Found {len(companies)} Greenhouse companies via Common Crawl")
        
    except Exception as e:
        print(f"  Common Crawl error: {e}")
    
    return list(companies)

def load_cache():
    if not CACHE_FILE.exists():
        return None
    
    data = json.loads(CACHE_FILE.read_text())
    cache_date = datetime.fromisoformat(data["updated_at"])
    
    if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
        return None
    
    return data["companies"]

def save_cache(companies):
    data = {
        "updated_at": datetime.now().isoformat(),
        "companies": companies,
    }
    CACHE_FILE.write_text(json.dumps(data, indent=2))

def fetch():
    jobs = []
    
    # Try cache first
    companies = load_cache()
    
    if not companies:
        print("    🔍 Discovering ALL Greenhouse companies (monthly refresh)...")
        companies = discover_all_greenhouse_companies()
        
        if not companies:
            print("  Greenhouse: Discovery failed")
            return []
        
        save_cache(companies)
    else:
        print(f"    ✓ Using cached {len(companies)} Greenhouse companies")
    
    # Fetch jobs from all companies
    successful = 0
    
    for i, company in enumerate(companies):
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            company_jobs = r.json().get("jobs", [])
            if company_jobs:
                successful += 1
            
            for item in company_jobs:
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("location", {}).get("name", "Remote"),
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse",
                })
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"      Progress: {i + 1}/{len(companies)}, {successful} with jobs, {len(jobs)} total jobs")
        
        except:
            continue
    
    print(f"    ✓ Greenhouse (All): {len(jobs)} jobs from {successful}/{len(companies)} companies")
    return jobs