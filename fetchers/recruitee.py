import requests
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_recruitee_companies.json")
CACHE_DAYS = 7

def discover_recruitee_companies():
    """Discover companies using Recruitee via Google search."""
    companies = set()
    
    try:
        url = "https://www.google.com/search"
        params = {
            "q": 'site:recruitee.com/api/offers "developer" OR "marketing" OR "growth"',
            "num": 100,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Extract company slugs from URLs
        # Format: company.recruitee.com
        recruitee_slugs = re.findall(r'([a-zA-Z0-9-]+)\.recruitee\.com', r.text)
        companies.update(recruitee_slugs)
        
        # Remove common non-company subdomains
        companies.discard("www")
        companies.discard("api")
        companies.discard("careers")
        
    except Exception as e:
        print(f"  Recruitee discovery failed: {e}")
    
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
        print("    🔍 Auto-discovering Recruitee companies...")
        companies = discover_recruitee_companies()
        
        if not companies:
            print("  Recruitee: No companies discovered")
            return []
        
        save_cache(companies)
        print(f"    📍 Discovered {len(companies)} Recruitee companies")
    else:
        print(f"    ✓ Using cached {len(companies)} Recruitee companies")
    
    jobs = []
    successful = 0
    
    for company in companies:
        url = f"https://{company}.recruitee.com/api/offers"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            data = r.json()
            offers = data.get("offers", [])
            
            if offers:
                successful += 1
            
            for item in offers:
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("location", "Remote"),
                    "url": item.get("careers_url", ""),
                    "posted": item.get("created_at", ""),
                    "tags": [],
                    "source": "Recruitee",
                })
        except Exception:
            continue
    
    print(f"    ✓ Recruitee: {len(jobs)} jobs from {successful}/{len(companies)} companies")
    return jobs