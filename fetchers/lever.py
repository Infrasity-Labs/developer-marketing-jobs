import requests
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_lever_companies.json")
CACHE_DAYS = 7

def discover_lever_companies():
    """Discover companies using Lever via Google search."""
    companies = set()
    
    try:
        url = "https://www.google.com/search"
        params = {
            "q": 'site:jobs.lever.co "developer" OR "marketing" OR "growth"',
            "num": 100,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Extract company slugs from URLs
        # Format: jobs.lever.co/company/job-id
        lever_slugs = re.findall(r'jobs\.lever\.co/([^/\s"]+)', r.text)
        companies.update(lever_slugs)
        
    except Exception as e:
        print(f"  Lever discovery failed: {e}")
    
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
    # Try cache first
    companies = load_cache()
    
    if not companies:
        print("    🔍 Auto-discovering Lever companies...")
        companies = discover_lever_companies()
        
        if not companies:
            print("  Lever: No companies discovered")
            return []
        
        save_cache(companies)
        print(f"    📍 Discovered {len(companies)} Lever companies")
    else:
        print(f"    ✓ Using cached {len(companies)} Lever companies")
    
    jobs = []
    successful = 0
    
    for company in companies:
        url = f"https://api.lever.co/v0/postings/{company}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            
            data = r.json()
            if data:
                successful += 1
            
            for item in data:
                categories = item.get("categories", {})
                location = categories.get("location", "Remote")
                
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "url": item.get("hostedUrl", ""),
                    "posted": item.get("createdAt", ""),
                    "tags": [categories.get("team", ""), categories.get("department", "")],
                    "source": "Lever",
                })
        except Exception:
            continue
    
    print(f"    ✓ Lever: {len(jobs)} jobs from {successful}/{len(companies)} companies")
    return jobs