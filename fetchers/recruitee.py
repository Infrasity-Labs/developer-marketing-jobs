import requests

COMPANIES = [
    "bunq", "mollie", "adyen", "messagebird", "elastic",
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://{company}.recruitee.com/api/offers"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            data = r.json()
            for item in data.get("offers", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("location", "Remote"),
                    "url": item.get("careers_url", ""),
                    "posted": item.get("created_at", ""),
                    "tags": [],
                    "source": "Recruitee",
                })
        except Exception:
            continue
    
    print(f"    ✓ Recruitee: {len(jobs)} jobs")
    return jobs