import requests

COMPANIES = [
    "retool", "zapier", "loom", "deel", "canva", "clipboard-health",
    "ramp", "merge", "vanta", "watershed", "anthropic",
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://jobs.ashbyhq.com/{company}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            
            # Ashby returns HTML, need to parse differently
            # For now, try the API endpoint
            api_url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"
            r = requests.get(api_url, timeout=10)
            if r.status_code != 200:
                continue
                
            data = r.json()
            for item in data.get("jobs", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("locationName", "Remote"),
                    "url": item.get("jobUrl", ""),
                    "posted": item.get("publishedDate", ""),
                    "tags": [],
                    "source": "Ashby",
                })
        except Exception:
            continue
    
    print(f"    ✓ Ashby: {len(jobs)} jobs")
    return jobs