import requests
import xml.etree.ElementTree as ET
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_personio_companies.json")
CACHE_DAYS = 7

def discover_personio_companies():
    """Discover companies using Personio via Google search."""
    companies = set()
    
    try:
        url = "https://www.google.com/search"
        params = {
            "q": 'site:jobs.personio.de/xml "developer" OR "marketing"',
            "num": 100,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Extract company slugs: company.jobs.personio.de
        personio_slugs = re.findall(r'([a-zA-Z0-9-]+)\.jobs\.personio\.de', r.text)
        companies.update(personio_slugs)
        
    except Exception as e:
        print(f"  Personio discovery failed: {e}")
    
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
    companies = load_cache()
    
    if not companies:
        print("    🔍 Auto-discovering Personio companies...")
        companies = discover_personio_companies()
        
        if not companies:
            return []
        
        save_cache(companies)
        print(f"    📍 Discovered {len(companies)} Personio companies")
    
    jobs = []
    
    for company in companies:
        url = f"https://{company}.jobs.personio.de/xml"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            # Parse XML
            root = ET.fromstring(r.content)
            
            for item in root.findall(".//position"):
                title = item.findtext("name", "")
                office = item.findtext("office", "")
                
                jobs.append({
                    "title": title,
                    "company": company.capitalize(),
                    "location": office or "Remote",
                    "url": item.findtext("url", ""),
                    "posted": item.findtext("createdAt", ""),
                    "tags": [],
                    "source": "Personio",
                })
        except Exception:
            continue
    
    print(f"    ✓ Personio: {len(jobs)} jobs")
    return jobs