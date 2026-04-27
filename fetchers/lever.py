import requests

COMPANIES = [
    "stripe", "sourcegraph", "make", "deel", "canva", "superhuman",
    "retool", "zapier", "loom", "grammarly", "miro", "airtable",
    "figma", "linear", "pitch", "webflow", "framer", "coda",
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://api.lever.co/v0/postings/{company}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            
            for item in r.json():
                categories = item.get("categories", {})
                location = categories.get("location", "Remote")
                
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "url": item.get("hostedUrl", ""),
                    "posted": item.get("createdAt", ""),
                    "tags": [categories.get("team", ""), categories.get("department", "")],
                    "source": "Lever",
                })
        except Exception:
            continue
    
    print(f"    ✓ Lever: {len(jobs)} jobs from {len(COMPANIES)} companies")
    return jobs