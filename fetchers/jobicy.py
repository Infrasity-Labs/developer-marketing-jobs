import requests
import time

def fetch(categories=None):
    """Fetch jobs from Jobicy public API - no auth needed."""
    jobs = []
    categories = categories or []

    print(f"    🔍 Fetching from Jobicy...")

    try:
        # Jobicy supports up to 50 per request
        url = "https://jobicy.com/api/v2/remote-jobs"
        params = {
            "count": 50,
            "geo": "anywhere",
        }

        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            print(f"    ✗ Jobicy: {response.status_code}")
            return []

        data = response.json()
        job_list = data.get('jobs', [])

        for item in job_list:
            title = item.get('jobTitle', '')
            company = item.get('companyName', '')
            location = item.get('jobGeo', 'Remote')
            url_job = item.get('url', '')
            posted = item.get('pubDate', '')
            tags = item.get('jobType', [])
            industry = item.get('jobIndustry', [])

            if isinstance(tags, str):
                tags = [tags]
            if isinstance(industry, str):
                industry = [industry]

            jobs.append({
                'title': title,
                'company': company,
                'location': location or 'Remote',
                'url': url_job,
                'posted': posted,
                'tags': tags + industry,
                'source': 'Jobicy',
            })

    except Exception as e:
        print(f"    ✗ Jobicy error: {e}")

    print(f"    ✓ Jobicy: {len(jobs)} jobs")
    return jobs