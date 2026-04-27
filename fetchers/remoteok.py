import requests
from datetime import datetime

def fetch():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get("https://remoteok.com/api", headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()[1:]  # first item is metadata, skip it

    jobs = []
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
    return jobs