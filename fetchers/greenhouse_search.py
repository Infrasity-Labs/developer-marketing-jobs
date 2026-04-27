import requests

def fetch():
    jobs = []
    
    keywords = [
        "developer relations",
        "devrel",
        "technical writer",
        "content marketing",
    ]
    
    for keyword in keywords:
        try:
            # Greenhouse's public search API (no auth needed)
            url = "https://boards-api.greenhouse.io/v1/boards/job_board/jobs"
            params = {
                "query": keyword,
            }
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json().get("jobs", [])
            
            for item in data:
                location = ""
                if item.get("location"):
                    location = item["location"].get("name", "")
                
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("company", ""),
                    "location": location or "Remote",
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse",
                })
        except Exception as e:
            print(f"  Greenhouse Search: failed for '{keyword}': {e}")
            continue
    
    return jobs