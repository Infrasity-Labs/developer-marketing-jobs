import requests

COMPANIES = [
    "docker", "kong", "gitlab", "grammarly", "miro", "typeform",
    "contentful", "prismic", "storyblok", "sanity",
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://apply.workable.com/api/v1/widget/accounts/{company}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            data = r.json()
            for item in data.get("jobs", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("location", {}).get("city", "Remote"),
                    "url": item.get("url", ""),
                    "posted": item.get("created_at", ""),
                    "tags": [],
                    "source": "Workable",
                })
        except Exception:
            continue
    
    print(f"    ✓ Workable: {len(jobs)} jobs")
    return jobs