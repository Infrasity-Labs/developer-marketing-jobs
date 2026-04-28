import requests

def fetch():
    jobs = []
    
    try:
        # Arbeitnow API - get ALL jobs (no keyword filtering)
        # Let main.py CATEGORIES handle the filtering
        url = "https://www.arbeitnow.com/api/job-board-api"
        
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("job_geo_location", ""),
                "url": item.get("url", ""),
                "posted": item.get("posted_on", ""),
                "tags": item.get("tags", []),
                "source": "Arbeitnow",
            })
            
    except Exception as e:
        print(f"  Arbeitnow: {e}")
    
    print(f"    ✓ Arbeitnow: {len(jobs)} jobs")
    return jobs