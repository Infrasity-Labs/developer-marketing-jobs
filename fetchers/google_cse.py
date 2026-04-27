import requests
import re
import os

def fetch():
    # Get credentials from environment variables
    api_key = os.getenv("GOOGLE_CSE_API_KEY", "")
    search_engine_id = os.getenv("GOOGLE_CSE_ID", "c2baa0cc4fc164553")
    
    if not api_key:
        print("  Google CSE: API key not configured, skipping")
        return []
    
    jobs = []
    
    # Queries to find companies hiring for your roles
    queries = [
        'site:boards.greenhouse.io "developer advocate"',
        'site:boards.greenhouse.io "technical writer"',
        'site:boards.greenhouse.io "product marketing manager"',
        'site:boards.greenhouse.io "head of growth"',
        'site:boards.greenhouse.io "vp marketing"',
        'site:jobs.lever.co "developer advocate"',
        'site:jobs.lever.co "technical writer"',
        'site:jobs.lever.co "product marketing"',
        'site:jobs.ashbyhq.com "developer relations"',
        'site:jobs.ashbyhq.com "technical writer"',
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
            
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            
            # Extract company slugs from URLs
            for item in data.get("items", []):
                link = item.get("link", "")
                
                # Greenhouse: https://boards.greenhouse.io/cloudflare/jobs/123
                if "boards.greenhouse.io" in link:
                    match = re.search(r"boards\.greenhouse\.io/([^/]+)", link)
                    if match:
                        discovered_companies["greenhouse"].add(match.group(1))
                
                # Lever: https://jobs.lever.co/stripe/abc123
                elif "jobs.lever.co" in link:
                    match = re.search(r"jobs\.lever\.co/([^/]+)", link)
                    if match:
                        discovered_companies["lever"].add(match.group(1))
                
                # Ashby: https://jobs.ashbyhq.com/ramp
                elif "ashbyhq.com" in link:
                    match = re.search(r"ashbyhq\.com/([^/]+)", link)
                    if match:
                        discovered_companies["ashby"].add(match.group(1))
        
        except Exception as e:
            continue
    
    total_companies = sum(len(c) for c in discovered_companies.values())
    print(f"    📊 Discovered {total_companies} companies: {len(discovered_companies['greenhouse'])} GH, {len(discovered_companies['lever'])} Lever, {len(discovered_companies['ashby'])} Ashby")
    
    # Now fetch jobs from discovered companies
    
    # Greenhouse
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
    
    # Lever
    for company in discovered_companies["lever"]:
        try:
            url = f"https://api.lever.co/v0/postings/{company}"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json():
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company.capitalize(),
                    "location": item.get("categories", {}).get("location", "Remote"),
                    "url": item.get("hostedUrl", ""),
                    "posted": item.get("createdAt", ""),
                    "tags": [],
                    "source": "Lever (CSE)",
                })
        except:
            continue
    
    # Ashby
    for company in discovered_companies["ashby"]:
        try:
            url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json().get("jobs", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("locationName", "Remote"),
                    "url": item.get("jobUrl", ""),
                    "posted": item.get("publishedDate", ""),
                    "tags": [],
                    "source": "Ashby (CSE)",
                })
        except:
            continue
    
    print(f"    ✓ Google CSE: {len(jobs)} jobs from {total_companies} companies")
    return jobs