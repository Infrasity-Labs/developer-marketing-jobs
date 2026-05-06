import requests
import re
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("dataforseo_discovered.json")
CACHE_DAYS = 30

# ATS site patterns
ATS_CONFIG = {
    "lever": {
        "site": "site:jobs.lever.co",
        "pattern": r'jobs\.lever\.co/([a-zA-Z0-9][a-zA-Z0-9\-]+)',
    },
    "workable": {
        "site": "site:apply.workable.com",
        "pattern": r'apply\.workable\.com/([a-zA-Z0-9][a-zA-Z0-9\-]+)',
    },
    "ashby": {
        "site": "site:jobs.ashbyhq.com",
        "pattern": r'jobs\.ashbyhq\.com/([a-zA-Z0-9][a-zA-Z0-9\-]+)',
    },
    "greenhouse": {
        "site": "site:boards.greenhouse.io",
        "pattern": r'boards\.greenhouse\.io/([a-zA-Z0-9][a-zA-Z0-9\-]+)',
    },
}


def build_queries_from_categories(ats_type, categories):
    """
    Build search queries dynamically from main.py CATEGORIES.
    Uses actual keywords instead of hardcoded ones.
    """
    site = ATS_CONFIG[ats_type]["site"]
    queries = []

    for cat in categories:
        # Use first 3 keywords from each category
        # (too many keywords = too many API calls)
        keywords = cat.get("keywords", [])[:3]

        for keyword in keywords:
            # Skip very generic keywords that would return noise
            if len(keyword) < 6:
                continue

            query = f'{site} "{keyword}"'
            queries.append(query)

    # Deduplicate
    queries = list(set(queries))

    print(f"      Built {len(queries)} queries from {len(categories)} categories")
    return queries


def discover_companies(ats_type, categories):
    """
    Discover companies on any ATS using DataForSEO SERP API.
    Uses categories from main.py instead of hardcoded keywords.
    """
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")

    if not login or not password:
        print(f"  DataForSEO: credentials not set, skipping {ats_type} discovery")
        return set()

    if ats_type not in ATS_CONFIG:
        print(f"  Unknown ATS type: {ats_type}")
        return set()

    pattern = ATS_CONFIG[ats_type]["pattern"]

    # Build queries from actual categories
    queries = build_queries_from_categories(ats_type, categories)

    companies = set()
    print(f"      Running {len(queries)} DataForSEO queries for {ats_type}...")

    for i, query in enumerate(queries):
        try:
            response = requests.post(
                "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
                auth=(login, password),
                json=[{
                    "keyword": query,
                    "location_code": 2840,  # United States
                    "language_code": "en",
                    "depth": 100,
                }],
                timeout=30,
            )

            if response.status_code != 200:
                continue

            data = response.json()

            new_found = 0
            for task in data.get('tasks', []):
                for result in task.get('result', []):
                    for item in result.get('items', []):
                        url = item.get('url', '')
                        match = re.search(pattern, url, re.IGNORECASE)
                        if match:
                            slug = match.group(1).lower()
                            if len(slug) > 2:
                                if slug not in companies:
                                    companies.add(slug)
                                    new_found += 1

            if new_found > 0:
                print(f"      Query {i+1}/{len(queries)}: +{new_found} companies (total: {len(companies)})")

        except Exception as e:
            print(f"      Query failed: {e}")
            continue

    print(f"    📍 {ats_type}: {len(companies)} companies discovered")
    return companies


def load_cache():
    if not CACHE_FILE.exists():
        return None
    try:
        data = json.loads(CACHE_FILE.read_text())
        cache_date = datetime.fromisoformat(data["updated_at"])
        if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
            return None
        return data
    except:
        return None


def save_cache(data):
    cache_data = {
        "updated_at": datetime.now().isoformat(),
        **data
    }
    CACHE_FILE.write_text(json.dumps(cache_data, indent=2))


def get_discovered_companies(categories):
    """
    Returns dict of discovered companies per ATS.
    Uses cache if available, otherwise runs DataForSEO discovery.

    Args:
        categories: CATEGORIES list from main.py
    """
    cached = load_cache()
    if cached:
        print(f"    ✓ Using cached DataForSEO discoveries:")
        print(f"      Lever:    {len(cached.get('lever', []))} companies")
        print(f"      Workable: {len(cached.get('workable', []))} companies")
        print(f"      Ashby:    {len(cached.get('ashby', []))} companies")
        return cached

    print("    🔍 Running DataForSEO discovery using your categories...")

    lever    = discover_companies("lever", categories)
    workable = discover_companies("workable", categories)
    ashby    = discover_companies("ashby", categories)

    print(f"\n    📊 Discovery complete:")
    print(f"      Lever:    {len(lever)} companies")
    print(f"      Workable: {len(workable)} companies")
    print(f"      Ashby:    {len(ashby)} companies")

    result = {
        "lever":    list(lever),
        "workable": list(workable),
        "ashby":    list(ashby),
    }

    save_cache(result)
    return result