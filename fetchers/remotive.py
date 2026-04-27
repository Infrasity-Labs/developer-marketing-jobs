import requests

def fetch():
    r = requests.get("https://remotive.com/api/remote-jobs", timeout=15)
    r.raise_for_status()
    data = r.json().get("jobs", [])

    jobs = []
    for item in data:
        jobs.append({
            "title": item.get("title", ""),
            "company": item.get("company_name", ""),
            "location": item.get("candidate_required_location", "Remote"),
            "url": item.get("url", ""),
            "posted": item.get("publication_date", ""),
            "tags": [t.lower() for t in item.get("tags", [])],
            "source": "Remotive",
        })
    return jobs