import requests
import os

def fetch():
    app_id = os.getenv("ADZUNA_APP_ID", "1aa7baa7")
    app_key = os.getenv("ADZUNA_APP_KEY", "48e9c89e392779ea85d58304a56dcf6e")
    
    if not app_id or not app_key:
        print("  Adzuna: API credentials not configured, skipping")
        return []

    jobs = []
    
    # Search multiple countries for better coverage
    countries = ["us", "gb", "ca", "au"]
    
    # Generic search terms that cover most job types
    search_terms = [
        "marketing",
        "developer",
        "technical",
        "content",
        "growth",
        "community",
    ]
    
    seen_urls = set()  # Dedupe across countries and keywords
    
    for country in countries:
        for term in search_terms:
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
                params = {
                    "app_id": app_id,
                    "app_key": app_key,
                    "results_per_page": 50,
                    "what": term,
                    "sort_by": "date",
                    "max_days_old": 90,
                }
                
                r = requests.get(url, params=params, timeout=15)
                
                if r.status_code != 200:
                    continue
                
                r.raise_for_status()
                data = r.json()
                
                for item in data.get("results", []):
                    job_url = item.get("redirect_url", "")
                    if job_url in seen_urls:
                        continue
                    seen_urls.add(job_url)
                    
                    jobs.append({
                        "title": item.get("title", ""),
                        "company": item.get("company", {}).get("display_name", ""),
                        "location": item.get("location", {}).get("display_name", ""),
                        "url": job_url,
                        "posted": item.get("created", ""),
                        "tags": [],
                        "source": "Adzuna",
                    })
            
            except Exception:
                continue
    
    print(f"    ✓ Adzuna: {len(jobs)} jobs from {len(countries)} countries")
    return jobs