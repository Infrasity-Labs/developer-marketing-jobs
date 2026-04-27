import requests

def fetch():
    jobs = []
    
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        
        # Make multiple searches for different keywords
        keywords_list = [
            "developer relations",
            "technical writer",
            "content marketing",
            "devrel",
        ]
        
        for keyword in keywords_list:
            params = {
                "search": keyword,
            }
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            
            for item in data.get("data", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("company_name", ""),
                    "location": item.get("job_geo_location", ""),
                    "url": item.get("url", ""),
                    "posted": item.get("posted_on", ""),
                    "tags": [],
                    "source": "Arbeitnow",
                })
    except Exception as e:
        print(f"  Arbeitnow: fetch failed: {e}")
    
    return jobs