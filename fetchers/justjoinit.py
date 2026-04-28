import requests

def fetch():
    jobs = []
    
    # JustJoinIT API - European tech job board
    # Search multiple keywords to cover all categories
    keywords = [
        "developer advocate",
        "developer relations",
        "technical writer",
        "product marketing",
        "growth marketing",
        "community manager",
    ]
    
    seen_urls = set()  # Dedupe across keywords
    
    for keyword in keywords:
        try:
            url = "https://api.justjoinit.pl/v2/search"
            params = {
                "keyword": keyword,
                "limit": 100,
            }
            # Disable SSL verification as a workaround for cert issues
            r = requests.get(url, params=params, timeout=15, verify=False)
            r.raise_for_status()
            data = r.json()
            
            for item in data.get("results", []):
                job_url = item.get("url", "")
                if job_url in seen_urls:
                    continue
                seen_urls.add(job_url)
                
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("company_name", ""),
                    "location": item.get("city", ""),
                    "url": job_url,
                    "posted": item.get("published_at", ""),
                    "tags": item.get("skills", []),
                    "source": "JustJoinIT",
                })
        except Exception as e:
            continue  # Skip failed keywords silently
    
    print(f"    ✓ JustJoinIT: {len(jobs)} jobs")
    return jobs