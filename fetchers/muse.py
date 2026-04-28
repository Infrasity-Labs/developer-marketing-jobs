import requests

def fetch():
    jobs = []
    
    try:
        # TheMuse API - fetch all Technology + Remote jobs
        # Let main.py handle keyword filtering via CATEGORIES
        url = "https://www.themuse.com/api/public/jobs"
        params = {
            "category": "Technology",
            "location": "Remote",
            "page": 0,
        }
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        for item in data.get("results", []):
            jobs.append({
                "title": item.get("name", ""),
                "company": item.get("company", {}).get("name", ""),
                "location": ", ".join([l.get("name", "") for l in item.get("locations", [])]),
                "url": item.get("refs", {}).get("landing_page", ""),
                "posted": item.get("publication_date", ""),
                "tags": [],
                "source": "TheMuse",
            })
    except Exception as e:
        print(f"  TheMuse: {e}")
    
    print(f"    ✓ TheMuse: {len(jobs)} jobs")
    return jobs