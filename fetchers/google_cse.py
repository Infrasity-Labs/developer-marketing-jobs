import requests
import re
import os

def fetch():
    # Get credentials from environment variables
    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CSE_ID", "c2baa0cc4fc164553")
    
    if not api_key:
        print("  Google CSE: API key not configured, skipping")
        return []
    
    print(f"    🔑 Using API key: {api_key[:10]}... and CSE ID: {search_engine_id}")
    
    jobs = []
    
    # Start with just ONE query for debugging
    queries = [
        'site:boards.greenhouse.io "developer advocate"',
    ]
    
    discovered_companies = {
        "greenhouse": set(),
        "lever": set(),
        "ashby": set(),
    }
    
    print(f"    🔍 Running Google CSE to discover companies...")
    
    for query in queries:
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": search_engine_id,
                "q": query,
                "num": 10,
            }
            
            print(f"      Searching: {query}")
            r = requests.get(url, params=params, timeout=15)
            
            # Show the actual response
            print(f"      Status: {r.status_code}")
            
            if r.status_code != 200:
                print(f"      Error response: {r.text[:200]}")
                continue
            
            r.raise_for_status()
            data = r.json()
            
            print(f"      Found {len(data.get('items', []))} results")
            
            # Extract company slugs from URLs
            for item in data.get("items", []):
                link = item.get("link", "")
                print(f"        - {link}")
                
                # Greenhouse: https://boards.greenhouse.io/cloudflare/jobs/123
                if "boards.greenhouse.io" in link:
                    match = re.search(r"boards\.greenhouse\.io/([^/]+)", link)
                    if match:
                        company = match.group(1)
                        discovered_companies["greenhouse"].add(company)
                        print(f"          → Found company: {company}")
        
        except Exception as e:
            print(f"      ❌ Query failed: {e}")
            continue
    
    total_companies = sum(len(c) for c in discovered_companies.values())
    print(f"    📊 Discovered {total_companies} companies: {len(discovered_companies['greenhouse'])} GH")
    
    # Fetch jobs from discovered companies
    for company in discovered_companies["greenhouse"]:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json().get("jobs", []):
                location = item.get("location", {}).get("name", "Remote")
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse (CSE)",
                })
        except:
            continue
    
    print(f"    ✓ Google CSE: {len(jobs)} jobs from {total_companies} companies")
    return jobs