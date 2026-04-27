import requests

def fetch():
    jobs = []
    try:
        url = "https://himalayas.app/jobs/api"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        
        for item in r.json().get("data", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company", {}).get("name", ""),
                "location": item.get("location", "Remote"),
                "url": item.get("url", ""),
                "posted": item.get("published_at", ""),
                "tags": item.get("tags", []),
                "source": "Himalayas",
            })
    except Exception as e:
        print(f"  Himalayas: {e}")
    
    print(f"    ✓ Himalayas: {len(jobs)} jobs")
    return jobs