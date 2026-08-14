import requests
import time

def fetch():
    jobs = []

    try:
        # TheMuse API - fetch all Software Engineering + Remote jobs
        # (TheMuse no longer has a "Technology" category - it returns 0 results)
        # Let main.py handle keyword filtering via CATEGORIES
        url = "https://www.themuse.com/api/public/jobs"

        page = 0
        max_pages = 20

        while page < max_pages:
            params = {
                "category": "Software Engineering",
                "location": "Remote",
                "page": page,
            }
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()

            results = data.get("results", [])
            if not results:
                break

            for item in results:
                jobs.append({
                    "title": item.get("name", ""),
                    "company": item.get("company", {}).get("name", ""),
                    "location": ", ".join([l.get("name", "") for l in item.get("locations", [])]),
                    "url": item.get("refs", {}).get("landing_page", ""),
                    "posted": item.get("publication_date", ""),
                    "tags": [],
                    "source": "TheMuse",
                })

            # page_count tells us how many pages exist in total
            page_count = data.get("page_count", 0)
            if page + 1 >= page_count:
                break

            page += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"  TheMuse: {e}")

    print(f"    ✓ TheMuse: {len(jobs)} jobs")
    return jobs
