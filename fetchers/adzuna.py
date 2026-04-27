import requests
import os

def fetch():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        print("  Adzuna: API credentials not configured, skipping")
        return []

    jobs = []
    
    # Search multiple countries for better coverage
    countries = ["us", "gb", "ca", "au", "de", "fr", "nl"]
    
    # Broader keywords to match more jobs
    keywords = [
        "developer advocate OR developer relations OR devrel",
        "technical writer OR documentation engineer",
        "product marketing manager OR product marketer",
        "head of growth OR growth marketing",
        "vp marketing OR director of marketing",
        "community manager",
    ]
    
    for country in countries:
        for keyword in keywords:
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
                params = {
                    "app_id": app_id,
                    "app_key": app_key,
                    "results_per_page": 50,
                    "what": keyword,
                    "sort_by": "date",
                    "max_days_old": 30,
                }
                
                r = requests.get(url, params=params, timeout=15)
                r.raise_for_status()
                data = r.json()
                
                for item in data.get("results", []):
                    jobs.append({
                        "title": item.get("title", ""),
                        "company": item.get("company", {}).get("display_name", ""),
                        "location": item.get("location", {}).get("display_name", ""),
                        "url": item.get("redirect_url", ""),
                        "posted": item.get("created", ""),
                        "tags": [],
                        "source": "Adzuna",
                    })
            
            except Exception as e:
                # Skip failed country/keyword combinations silently
                continue
    
    print(f"    ✓ Adzuna: {len(jobs)} jobs from {len(countries)} countries")
    return jobs