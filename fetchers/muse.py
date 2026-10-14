import requests

MAX_PAGES = 10


def fetch():
    jobs = []
    url = "https://www.themuse.com/api/public/jobs"

    # TheMuse API - fetch Technology + Remote jobs, paginated
    # Let main.py handle keyword filtering via CATEGORIES
    for page in range(MAX_PAGES):
        params = {"category": "Technology", "location": "Remote", "page": page}
        try:
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  TheMuse page {page}: {e}")
            break

        for item in data.get("results", []):
            jobs.append({
                "title": item.get("name", ""),
                "company": item.get("company", {}).get("name", ""),
                "location": ", ".join(l.get("name", "") for l in item.get("locations", [])),
                "url": item.get("refs", {}).get("landing_page", ""),
                "posted": item.get("publication_date", ""),
                "tags": [],
                "source": "TheMuse",
            })

        if page + 1 >= data.get("page_count", 0):
            break

    print(f"    ✓ TheMuse: {len(jobs)} jobs")
    return jobs
