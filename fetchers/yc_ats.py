from playwright.sync_api import sync_playwright
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import urllib.parse
from bs4 import BeautifulSoup

CACHE_FILE = Path("yc_all_companies.json")
CACHE_DAYS = 7

ALGOLIA_URL = "https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.16.1)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=NzllNTY5MzJiZGM2OTY2ZTQwMDEzOTNhYWZiZGRjODlhYzVkNjBmOGRjNzJiMWM4ZTU0ZDlhYTZjOTJiMjlhMWFuYWx5dGljc1RhZ3M9eWNkYyZyZXN0cmljdEluZGljZXM9WUNDb21wYW55X3Byb2R1Y3Rpb24lMkNZQ0NvbXBhbnlfQnlfTGF1bmNoX0RhdGVfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVE"
ALGOLIA_HEADERS = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://www.ycombinator.com",
    "Referer": "https://www.ycombinator.com/"
}


def get_all_yc_companies():
    """Get all YC company slugs using Algolia API."""
    slugs = set()

    # All YC batches from 2005 to 2026
    batches = []
    seasons = ["Winter", "Spring", "Summer", "Fall"]
    for year in range(2005, 2027):
        for season in seasons:
            batches.append(f"{season} {year}")
    batches.reverse()  # Newest first

    print(f"    🔍 Fetching all YC companies via Algolia ({len(batches)} batches)...")

    for batch in batches:
        try:
            page_num = 0

            while True:
                raw_filter = f'[["batch:{batch}"]]'
                encoded_filter = urllib.parse.quote(raw_filter)
                params = f"query=&hitsPerPage=100&page={page_num}&facetFilters={encoded_filter}"

                payload = {
                    "requests": [{
                        "indexName": "YCCompany_production",
                        "params": params
                    }]
                }

                response = requests.post(
                    ALGOLIA_URL,
                    headers=ALGOLIA_HEADERS,
                    json=payload,
                    timeout=10
                )

                if response.status_code != 200:
                    break

                data = response.json()
                hits = data['results'][0].get('hits', [])

                if not hits:
                    break

                batch_new = 0
                for company in hits:
                    slug = company.get('slug', '').strip()
                    if slug and slug not in slugs:
                        slugs.add(slug)
                        batch_new += 1

                # Check if more pages
                total_pages = data['results'][0].get('nbPages', 1)
                if page_num >= total_pages - 1:
                    break

                page_num += 1
                time.sleep(0.2)

            if batch_new > 0:
                print(f"      {batch}: +{batch_new} (total: {len(slugs)})")

        except Exception as e:
            continue

    print(f"    📍 Found {len(slugs)} total YC companies")
    return list(slugs)


def scrape_all_jobs(company_slugs):
    """Scrape jobs from all companies using a single browser instance."""
    all_jobs = []
    companies_with_jobs = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, slug in enumerate(company_slugs):
            try:
                url = f"https://www.ycombinator.com/companies/{slug}/jobs"
                response = page.goto(url, wait_until="domcontentloaded", timeout=10000)

                if response and response.status == 404:
                    continue

                page.wait_for_timeout(1000)

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                data_div = soup.find('div', {'data-page': True})

                if data_div:
                    data = json.loads(data_div['data-page'])
                    props = data.get('props', {})
                    job_postings = props.get('jobPostings', [])

                    if job_postings:
                        companies_with_jobs += 1
                        company_name = props.get('company', {}).get('name', slug.capitalize())

                        for job in job_postings:
                            all_jobs.append({
                                'title': job.get('title', ''),
                                'url': f"https://www.ycombinator.com{job.get('url', '')}",
                                'location': job.get('location', 'Remote'),
                                'company': company_name,
                                'posted': job.get('createdAt', ''),
                            })

                if (i + 1) % 100 == 0:
                    print(f"      Progress: {i + 1}/{len(company_slugs)}, {companies_with_jobs} with jobs, {len(all_jobs)} jobs")

                time.sleep(0.1)

            except Exception as e:
                continue

        browser.close()

    return all_jobs, companies_with_jobs


def load_cache():
    if not CACHE_FILE.exists():
        return None
    try:
        data = json.loads(CACHE_FILE.read_text())
        cache_date = datetime.fromisoformat(data["updated_at"])
        if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
            return None
        return data["companies"]
    except:
        return None


def save_cache(companies):
    CACHE_FILE.write_text(json.dumps({
        "updated_at": datetime.now().isoformat(),
        "companies": companies,
    }, indent=2))


def fetch():
    cached_companies = load_cache()

    if cached_companies:
        print(f"    ✓ Using cached {len(cached_companies)} YC companies")
        company_slugs = cached_companies
    else:
        company_slugs = get_all_yc_companies()
        if not company_slugs:
            print("  YC: No companies found")
            return []
        save_cache(company_slugs)
        print(f"    💾 Cached {len(company_slugs)} company slugs")

    print(f"    🔍 Fetching jobs from {len(company_slugs)} YC companies...")
    all_jobs, companies_with_jobs = scrape_all_jobs(company_slugs)

    jobs = []
    for job in all_jobs:
        jobs.append({
            "title": job['title'],
            "company": job['company'],
            "location": job['location'],
            "url": job['url'],
            "posted": job.get('posted', ''),
            "tags": [],
            "source": "YC",
        })

    print(f"    ✓ YC: {len(jobs)} jobs from {companies_with_jobs}/{len(company_slugs)} companies")
    return jobs