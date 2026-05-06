import requests
import re
import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("discovered_workable_companies.json")
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
    """Auto-discover Workable companies via Common Crawl."""
    companies = set()

    indexes = [
        "https://index.commoncrawl.org/CC-MAIN-2024-51-index",
        "https://index.commoncrawl.org/CC-MAIN-2024-46-index",
        "https://index.commoncrawl.org/CC-MAIN-2024-42-index",
    ]

    skip = {
        '', 'j', 'jobs', 'api', 'static', 'assets',
        'careers', 'about', 'terms', 'privacy', 'login',
        'signup', 'register', 'auth', 'oauth'
    }

    for cc_url in indexes:
        try:
            print(f"      Fetching Workable companies from Common Crawl...")
            response = requests.get(
                cc_url,
                params={
                    "url": "apply.workable.com/*",
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

            for line in lines:
                try:
                    data = json.loads(line)
                    url = data.get('url', '')
                    path = url.replace('https://apply.workable.com/', '').replace('http://apply.workable.com/', '')
                    slug = path.split('/')[0].split('?')[0].strip().lower()
                    if slug and len(slug) > 1 and slug not in skip and '%' not in slug:
                        companies.add(slug)
                except:
                    continue

            if companies:
                print(f"      ✓ Common Crawl: {len(companies)} Workable companies")
                return companies

        except Exception as e:
            print(f"      Common Crawl error: {e}")
            continue

    return companies


def discover_via_dataforseo(categories):
    """Auto-discover Workable companies via DataForSEO using category keywords."""
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
                queries.append(f'site:apply.workable.com "{keyword}"')

    queries = list(set(queries))
    print(f"      Running {len(queries)} DataForSEO queries for Workable...")

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

            skip = {'j', 'jobs', 'api', 'static', ''}

            for task in data.get('tasks', []):
                for result in task.get('result', []):
                    for item in result.get('items', []):
                        url = item.get('url', '')
                        if 'apply.workable.com/' not in url:
                            continue
                        path = url.replace('https://apply.workable.com/', '').replace('http://apply.workable.com/', '')
                        slug = path.split('/')[0].split('?')[0].strip().lower()
                        if slug and len(slug) > 1 and slug not in skip and '%' not in slug:
                            companies.add(slug)

            if (i + 1) % 10 == 0:
                print(f"      Progress: {i + 1}/{len(queries)} queries, {len(companies)} companies found")

        except Exception:
            continue

    print(f"      ✓ DataForSEO: {len(companies)} Workable companies")
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

    cached = load_cache()
    if cached:
        print(f"    ✓ Using cached {len(cached)} Workable companies")
        companies = set(cached)
    else:
        print("    🔍 Discovering Workable companies...")
        companies = set()

        # Primary: DataForSEO
        if categories and os.getenv("DATAFORSEO_LOGIN"):
            dfs_companies = discover_via_dataforseo(categories)
            companies.update(dfs_companies)
            print(f"      DataForSEO total: {len(dfs_companies)}")

        # Fallback: Common Crawl
        if len(companies) < 50:
            print("      DataForSEO found few companies, adding Common Crawl...")
            cc_companies = discover_via_commoncrawl()
            new_from_cc = cc_companies - companies
            companies.update(cc_companies)
            print(f"      Common Crawl added: {len(new_from_cc)} new companies")

        if not companies:
            print("    ⚠️ No Workable companies discovered")
            return []

        print(f"    📍 Total: {len(companies)} Workable companies")
        save_cache(companies)

    # Fetch jobs
    jobs = []
    successful = 0
    failed_404 = 0
    company_list = list(companies)

    print(f"    🔍 Fetching jobs from {len(company_list)} Workable companies...")

    for i, slug in enumerate(company_list):
        try:
            url = f"https://apply.workable.com/api/v3/accounts/{slug}/jobs"
            response = requests.post(
                url,
                json={
                    "query": "",
                    "location": [],
                    "department": [],
                    "worktype": [],
                    "remote": False
                },
                timeout=10
            )

            if response.status_code == 404:
                failed_404 += 1
                continue

            if response.status_code in [401, 403]:
                continue

            if response.status_code != 200:
                continue

            data = response.json()
            results = data.get('results', [])

            if not results:
                continue

            successful += 1
            company_name = (
                data.get('company', {}).get('name', '')
                or slug.replace('-', ' ').title()
            )

            for post in results:
                location_obj = post.get('location', {}) or {}
                city = location_obj.get('city', '')
                country = location_obj.get('country', '')
                remote = post.get('remote', False)

                location_str = 'Remote' if remote else (
                    ', '.join(filter(None, [city, country])) or 'Remote'
                )

                department = post.get('department', '')
                employment_type = post.get('employment_type', '')
                tags = [t for t in [department, employment_type] if t]

                jobs.append({
                    'title': post.get('title', ''),
                    'company': company_name,
                    'location': location_str,
                    'url': f"https://apply.workable.com/{slug}/j/{post.get('shortcode', '')}/",
                    'posted': post.get('published', ''),
                    'tags': tags,
                    'source': 'Workable',
                })

            if (i + 1) % 50 == 0:
                print(f"      Progress: {i + 1}/{len(company_list)}, {successful} with jobs, {len(jobs)} total")

            time.sleep(0.05)

        except Exception:
            continue

    print(f"    ✓ Workable: {len(jobs)} jobs from {successful}/{len(company_list)} companies ({failed_404} not found)")
    return jobs