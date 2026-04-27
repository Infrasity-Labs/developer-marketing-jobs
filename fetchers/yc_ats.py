import requests

# Map YC companies to their ATS platforms
# You can build this list programmatically or manually
YC_GREENHOUSE = [
    "stripe", "figma", "retool", "webflow", "plaid", "checkr",
    "airtable", "segment", "amplitude", "mixpanel", "cruise",
]

YC_LEVER = [
    "rippling", "brex", "deel", "zapier", "loom", "merge",
]

YC_ASHBY = [
    "ramp", "vanta", "watershed", "anthropic",
]

def fetch():
    jobs = []
    
    # Fetch from Greenhouse YC companies
    for company in YC_GREENHOUSE:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json().get("jobs", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("location", {}).get("name", "Remote"),
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "YC (Greenhouse)",
                })
        except:
            continue
    
    # Fetch from Lever YC companies
    for company in YC_LEVER:
        try:
            url = f"https://api.lever.co/v0/postings/{company}"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json():
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company.capitalize(),
                    "location": item.get("categories", {}).get("location", "Remote"),
                    "url": item.get("hostedUrl", ""),
                    "posted": item.get("createdAt", ""),
                    "tags": [],
                    "source": "YC (Lever)",
                })
        except:
            continue
    
    # Fetch from Ashby YC companies
    for company in YC_ASHBY:
        try:
            url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json().get("jobs", []):
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": item.get("locationName", "Remote"),
                    "url": item.get("jobUrl", ""),
                    "posted": item.get("publishedDate", ""),
                    "tags": [],
                    "source": "YC (Ashby)",
                })
        except:
            continue
    
    print(f"    ✓ YC: {len(jobs)} jobs from {len(YC_GREENHOUSE + YC_LEVER + YC_ASHBY)} companies")
    return jobs