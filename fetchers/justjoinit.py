import requests

def fetch():
    jobs = []
    
    # JustJoinIT API — free, no auth
    try:
        url = "https://api.justjoinit.pl/v2/search"
        params = {
            "keyword": "developer relations",
            "limit": 100,
        }
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        for item in data.get("results", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("city", ""),
                "url": item.get("url", ""),
                "posted": item.get("published_at", ""),
                "tags": item.get("skills", []),
                "source": "JustJoinIT",
            })
    except Exception as e:
        print(f"  JustJoinIT: fetch failed: {e}")
    
    return jobs