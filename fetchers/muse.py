import requests

def fetch():
    jobs = []
    
    try:
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
            # Filter for your keywords in title
            keywords = ["developer relations", "devrel", "technical writer", "content marketing"]
            if not any(kw in item.get("name", "").lower() for kw in keywords):
                continue
            
            jobs.append({
                "title": item.get("name", ""),
                "company": item.get("company", {}).get("name", ""),
                "location": ", ".join([l.get("name", "") for l in item.get("locations", [])]),
                "url": item.get("refs", {}).get("landing_page", ""),
                "posted": item.get("published_at", ""),
                "tags": [],
                "source": "TheMuse",
            })
    except Exception as e:
        print(f"  TheMuse: fetch failed: {e}")
    
    return jobs