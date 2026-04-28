import requests

def fetch():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # RemoteOK has tags we can use
    tags = ["marketing", "writing", "community", "growth"]
    
    for tag in tags:
        try:
            url = f"https://remoteok.com/api?tag={tag}"
            r = requests.get(url, headers=headers, timeout=15)
            data = r.json()[1:]  # Skip metadata
            
            for item in data:
                jobs.append({
                    "title": item.get("position", ""),
                    "company": item.get("company", ""),
                    "location": item.get("location") or "Remote",
                    "url": item.get("url", ""),
                    "posted": item.get("date", ""),
                    "tags": [t.lower() for t in item.get("tags", [])],
                    "source": "RemoteOK",
                })
        except:
            continue
    
    print(f"    ✓ RemoteOK Extended: {len(jobs)} jobs")
    return jobs