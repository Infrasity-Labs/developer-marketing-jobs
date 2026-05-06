import requests
import re
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# RemoteFront is a job board - no company discovery needed
# It has a public API that returns all jobs directly

def fetch(categories=None):
    """
    Fetch jobs from RemoteFront.
    RemoteFront is a remote job board with a public API.
    No auth needed.
    """
    jobs = []
    categories = categories or []

    # Build keyword list from categories
    keywords = []
    if categories:
        for cat in categories:
            keywords.extend(cat.get("keywords", []))
        keywords = list(set(keywords))
    
    print(f"    🔍 Fetching from RemoteFront...")

    try:
        # RemoteFront public job listing endpoint
        page = 1
        total_fetched = 0

        while True:
            url = "https://remotefront.io/api/jobs"
            params = {
                "page": page,
                "per_page": 100,
            }

            response = requests.get(url, params=params, timeout=15)

            if response.status_code != 200:
                break

            data = response.json()

            # Handle different response formats
            if isinstance(data, list):
                items = data
                has_more = len(items) == 100
            elif isinstance(data, dict):
                items = data.get('jobs', data.get('data', data.get('results', [])))
                has_more = data.get('has_more', False) or data.get('next_page', None)
            else:
                break

            if not items:
                break

            total_fetched += len(items)

            for item in items:
                title = item.get('title', '') or item.get('position', '')
                company = item.get('company', '') or item.get('company_name', '')
                location = item.get('location', '') or item.get('region', 'Remote')
                url_job = item.get('url', '') or item.get('apply_url', '') or item.get('link', '')
                posted = item.get('published_at', '') or item.get('created_at', '') or item.get('date', '')

                # Extract tags
                tags = []
                if item.get('category'):
                    tags.append(item['category'])
                if item.get('job_type'):
                    tags.append(item['job_type'])

                if title and company:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location or 'Remote',
                        'url': url_job,
                        'posted': posted,
                        'tags': tags,
                        'source': 'RemoteFront',
                    })

            if not has_more:
                break

            page += 1
            time.sleep(0.2)

    except Exception as e:
        # Try alternative RemoteFront endpoint
        try:
            print(f"      Primary endpoint failed, trying alternative...")
            response = requests.get(
                "https://remotefront.io/jobs.json",
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                items = data if isinstance(data, list) else data.get('jobs', [])

                for item in items:
                    title = item.get('title', '') or item.get('position', '')
                    company = item.get('company', '') or item.get('company_name', '')

                    if title and company:
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': item.get('location', 'Remote'),
                            'url': item.get('url', ''),
                            'posted': item.get('published_at', ''),
                            'tags': [],
                            'source': 'RemoteFront',
                        })

        except Exception as e2:
            print(f"      RemoteFront failed: {e2}")

    print(f"    ✓ RemoteFront: {len(jobs)} jobs")
    return jobs