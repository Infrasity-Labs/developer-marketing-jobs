import requests
import re
import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_lever_companies.json")
CACHE_DAYS = 30


def load_env():
    """Load .env file manually."""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def discover_via_commoncrawl():
    """Auto-discover Lever companies via Common Crawl."""
    companies = set()

    indexes = [
        "https://index.commoncrawl.org/CC-MAIN-2024-51-index",
        "https://index.commoncrawl.org/CC-MAIN-2024-46-index",
        "https://index.commoncrawl.org/CC-MAIN-2024-42-index",
    ]

    for cc_url in indexes:
        try:
            print(f"      Fetching Lever companies from Common Crawl...")
            response = requests.get(
                cc_url,
                params={
                    "url": "jobs.lever.co/*",
                    "output": "json",
                    "limit": 100000,
                    "fl": "url"
                },
                timeout=120
            )

            if response.status_code != 200:
                continue

            lines = [l for l in response.text.strip().split('\n') if l]
            print(f"      Got {len(lines)} URLs from Common Crawl")

            skip = {'', 'jobs', 'api', 'static', 'assets'}

            for line in lines:
                try:
                    data = json.loads(line)
                    url = data.get('url', '')
                    path = url.replace('https://jobs.lever.co/', '').replace('http://jobs.lever.co/', '')
                    slug = path.split('/')[0].split('?')[0].strip().lower()
                    if slug and len(slug) > 1 and slug not in skip and '%' not in slug:
                        companies.add(slug)
                except:
                    continue

            if companies:
                print(f"      ✓ Common Crawl: {len(companies)} Lever companies")
                return companies

        except Exception as e:
            print(f"      Common Crawl error: {e}")
            continue

    return companies


def discover_via_dataforseo(categories):
    """Auto-discover Lever companies via DataForSEO using category keywords."""
    load_env()

    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")

    if not login or not password:
        print("      DataForSEO credentials not found")
        return set()

    companies = set()

    # Build queries from ALL category keywords
    queries = []
    for cat in categories:
        for keyword in cat.get("keywords", []):
            if len(keyword) > 5:
                queries.append(f'site:jobs.lever.co "{keyword}"')

    queries = list(set(queries))
    print(f"      Running {len(queries)} DataForSEO queries for Lever...")

    for i, query in enumerate(queries):
        try:
            response = requests.post(
                "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
                auth=(login, password),
                json=[{
                    "keyword": query,
                    "location_code": 2840,
                    "language_code": "en",
                    "depth": 100,
                }],
                timeout=30,
            )

            if response.status_code != 200:
                continue

            data = response.json()

            for task in data.get('tasks', []):
                for result in task.get('result', []):
                    for item in result.get('items', []):
                        url = item.get('url', '')
                        if 'jobs.lever.co/' not in url:
                            continue
                        path = url.replace('https://jobs.lever.co/', '').replace('http://jobs.lever.co/', '')
                        slug = path.split('/')[0].split('?')[0].strip().lower()
                        if slug and len(slug) > 1 and '%' not in slug:
                            companies.add(slug)

            if (i + 1) % 10 == 0:
                print(f"      Progress: {i + 1}/{len(queries)} queries, {len(companies)} companies found")

        except Exception:
            continue

    print(f"      ✓ DataForSEO: {len(companies)} Lever companies")
    return companies


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
        "companies": list(companies),
    }, indent=2))


def fetch(categories=None):
    categories = categories or []
    load_env()

    # Load from cache
    cached = load_cache()
    if cached:
        print(f"    ✓ Using cached {len(cached)} Lever companies")
        companies = set(cached)
    else:
        print("    🔍 Discovering Lever companies...")
        companies = set()

        # Primary: DataForSEO (targeted, relevant companies only)
        if categories and os.getenv("DATAFORSEO_LOGIN"):
            dfs_companies = discover_via_dataforseo(categories)
            companies.update(dfs_companies)
            print(f"      DataForSEO total: {len(dfs_companies)}")

        # Fallback: Common Crawl (free, broader coverage)
        if len(companies) < 50:
            print("      DataForSEO found few companies, adding Common Crawl...")
            cc_companies = discover_via_commoncrawl()
            new_from_cc = cc_companies - companies
            companies.update(cc_companies)
            print(f"      Common Crawl added: {len(new_from_cc)} new companies")

        if not companies:
            print("    ⚠️ No Lever companies discovered")
            return []

        print(f"    📍 Total: {len(companies)} Lever companies")
        save_cache(companies)

    # Fetch jobs
    jobs = []
    successful = 0
    failed_404 = 0
    company_list = list(companies)

    print(f"    🔍 Fetching jobs from {len(company_list)} Lever companies...")

    for i, slug in enumerate(company_list):
        try:
            url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                failed_404 += 1
                continue

            if response.status_code != 200:
                continue

            postings = response.json()

            if not isinstance(postings, list) or not postings:
                continue

            successful += 1

            for post in postings:
                cats = post.get('categories', {}) or {}
                all_locations = cats.get('allLocations', [])
                location = (
                    all_locations[0] if all_locations
                    else cats.get('location', 'Remote')
                ) or 'Remote'

                company_name = (
                    post.get('company', '')
                    or slug.replace('-', ' ').title()
                )

                team = cats.get('team', '')
                commitment = cats.get('commitment', '')
                tags = [t for t in [team, commitment] if t]

                jobs.append({
                    'title': post.get('text', ''),
                    'company': company_name,
                    'location': location,
                    'url': post.get('hostedUrl', ''),
                    'posted': post.get('createdAt', 0),
                    'tags': tags,
                    'source': 'Lever',
                })

            if (i + 1) % 50 == 0:
                print(f"      Progress: {i + 1}/{len(company_list)}, {successful} with jobs, {len(jobs)} total")

            time.sleep(0.05)

        except Exception:
            continue

    print(f"    ✓ Lever: {len(jobs)} jobs from {successful}/{len(company_list)} companies ({failed_404} not found)")
    return jobs