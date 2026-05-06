import requests
import time

def fetch(categories=None):
    """Fetch jobs from Himalayas public API - no auth needed."""
    jobs = []
    categories = categories or []

    print(f"    🔍 Fetching from Himalayas...")

    try:
        page = 1
        max_pages = 20

        while page <= max_pages:
            url = "https://himalayas.app/jobs/api"
            params = {
                "limit": 100,
                "offset": (page - 1) * 100,
            }

            response = requests.get(url, params=params, timeout=15)

            if response.status_code != 200:
                break

            data = response.json()
            job_list = data.get('jobs', [])

            if not job_list:
                break

            for item in job_list:
                # Extract location
                location = 'Remote'
                if item.get('locations'):
                    location = ', '.join(item['locations'][:2])
                elif item.get('locationRestrictions'):
                    location = ', '.join(item['locationRestrictions'][:2])

                # Extract tags
                tags = []
                if item.get('categories'):
                    tags.extend(item['categories'][:3])
                if item.get('jobType'):
                    tags.append(item['jobType'])

                # Get company name
                company = ''
                if item.get('company'):
                    company = item['company'].get('name', '')
                company = company or item.get('companyName', '')

                jobs.append({
                    'title': item.get('title', ''),
                    'company': company,
                    'location': location,
                    'url': item.get('applicationLink', '') or item.get('url', ''),
                    'posted': item.get('createdAt', '') or item.get('pubDate', ''),
                    'tags': tags,
                    'source': 'Himalayas',
                })

            # Check if more pages
            total = data.get('total', 0)
            if page * 100 >= total:
                break

            page += 1
            time.sleep(0.2)

    except Exception as e:
        print(f"    ✗ Himalayas error: {e}")

    print(f"    ✓ Himalayas: {len(jobs)} jobs")
    return jobs