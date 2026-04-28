import requests
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_greenhouse_companies.json")
CACHE_DAYS = 7  # Re-discover weekly

def scrape_builtwith():
    """Use BuiltWith's free tier to find companies using Greenhouse."""
    companies = set()
    
    try:
        # BuiltWith has a public API (limited free tier)
        # This finds companies using Greenhouse ATS
        url = "https://api.builtwith.com/free1/api.json"
        params = {
            "KEY": "free",  # Free tier
            "LOOKUP": "greenhouse.io",
        }
        
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        
        # Extract company names from the response
        for domain in data.get("Results", []):
            # Try to convert domain to greenhouse slug
            # e.g., stripe.com → stripe
            slug = domain.split(".")[0]
            companies.add(slug)
            
    except Exception as e:
        print(f"  BuiltWith scrape failed: {e}")
    
    return companies

def scrape_google_jobs():
    """Use Google Jobs search to find Greenhouse boards."""
    companies = set()
    
    try:
        # Google Jobs has indexed many Greenhouse job postings
        # We can search for "site:boards.greenhouse.io" and extract company slugs
        
        # Use a simple HTTP request to Google (this might get blocked, but worth trying)
        url = "https://www.google.com/search"
        params = {
            "q": 'site:boards.greenhouse.io "developer advocate" OR "technical writer" OR "product marketing"',
            "num": 100,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Extract all greenhouse URLs from the HTML
        greenhouse_urls = re.findall(r'boards\.greenhouse\.io/([^/\s"]+)', r.text)
        companies.update(greenhouse_urls)
        
    except Exception as e:
        print(f"  Google scrape failed: {e}")
    
    return companies

def brute_force_discovery():
    """Test common company name patterns to find Greenhouse boards."""
    companies = set()
    
    # Common patterns for tech company names
    prefixes = ["", "get", "use", "try", "join", "my"]
    suffixes = ["", "io", "ai", "app", "dev", "tech", "labs", "hq"]
    
    # Common tech company keywords
    keywords = [
        "data", "cloud", "security", "api", "platform", "analytics",
        "payment", "commerce", "social", "mobile", "web", "app",
        "ai", "ml", "dev", "code", "git", "deploy", "host",
    ]
    
    # Generate potential company slugs
    candidates = []
    for prefix in prefixes:
        for keyword in keywords:
            for suffix in suffixes:
                slug = f"{prefix}{keyword}{suffix}".replace(" ", "")
                if 3 < len(slug) < 20:  # Reasonable slug length
                    candidates.append(slug.lower())
    
    # Test each candidate (limit to avoid taking forever)
    print(f"    Testing {len(candidates[:500])} potential company names...")
    
    for i, slug in enumerate(candidates[:500]):
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            r = requests.get(url, timeout=3)
            
            if r.status_code == 200:
                data = r.json()
                if data.get("jobs"):
                    companies.add(slug)
                    print(f"      ✓ Found: {slug}")
            
            # Rate limiting
            if i % 50 == 0:
                print(f"      Tested {i}/500...")
                
        except:
            continue
    
    return companies

def load_cache():
    """Load previously discovered companies from cache."""
    if not CACHE_FILE.exists():
        return None
    
    data = json.loads(CACHE_FILE.read_text())
    cache_date = datetime.fromisoformat(data["updated_at"])
    
    # Refresh if cache is older than CACHE_DAYS
    if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
        return None
    
    return data["companies"]

def save_cache(companies):
    """Save discovered companies to cache."""
    data = {
        "updated_at": datetime.now().isoformat(),
        "companies": list(companies),
    }
    CACHE_FILE.write_text(json.dumps(data, indent=2))

def fetch():
    """Auto-discover Greenhouse companies and fetch their jobs."""
    
    # Try to load from cache first
    companies = load_cache()
    
    if not companies:
        print("    🔍 Auto-discovering Greenhouse companies (weekly refresh)...")
        
        all_companies = set()
        
        # Method 1: Scrape BuiltWith
        all_companies.update(scrape_builtwith())
        
        # Method 2: Scrape Google results
        all_companies.update(scrape_google_jobs())
        
        # Method 3: Brute force common patterns
        # all_companies.update(brute_force_discovery())  # Uncomment if you want this
        
        companies = list(all_companies)
        save_cache(companies)
        print(f"    📍 Discovered {len(companies)} companies (cached for {CACHE_DAYS} days)")
    else:
        print(f"    ✓ Using cached list of {len(companies)} companies")
    
    # Now fetch jobs from all discovered companies
    jobs = []
    successful = 0
    
    for company in companies:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            data = r.json().get("jobs", [])
            if data:
                successful += 1
            
            for item in data:
                location = item.get("location", {}).get("name", "Remote")
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse (Auto)",
                })
        except:
            continue
    
    print(f"    ✓ Greenhouse Auto: {len(jobs)} jobs from {successful}/{len(companies)} companies")
    return jobs