import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch(categories=None):
    """Fetch jobs from We Work Remotely RSS feed - no auth needed."""
    jobs = []
    categories = categories or []

    print(f"    🔍 Fetching from We Work Remotely...")

    # Multiple RSS feeds by category
    feeds = [
        "https://weworkremotely.com/remote-jobs.rss",
        "https://weworkremotely.com/categories/remote-marketing-jobs.rss",
        "https://weworkremotely.com/categories/remote-copywriting-jobs.rss",
        "https://weworkremotely.com/categories/remote-management-finance-jobs.rss",
    ]

    seen_urls = set()

    for feed_url in feeds:
        try:
            response = requests.get(
                feed_url,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            if response.status_code != 200:
                continue

            root = ET.fromstring(response.content)

            for item in root.findall('.//item'):
                title_el = item.find('title')
                link_el = item.find('link')
                pub_date_el = item.find('pubDate')
                region_el = item.find('{https://weworkremotely.com}region')
                company_el = item.find('{https://weworkremotely.com}company')

                title = title_el.text if title_el is not None else ''
                link = link_el.text if link_el is not None else ''
                pub_date = pub_date_el.text if pub_date_el is not None else ''
                region = region_el.text if region_el is not None else 'Remote'
                company = company_el.text if company_el is not None else ''

                # WWR titles often have format "Company: Job Title"
                if ': ' in title and not company:
                    parts = title.split(': ', 1)
                    company = parts[0].strip()
                    title = parts[1].strip()

                if not title or link in seen_urls:
                    continue

                seen_urls.add(link)

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': region or 'Remote',
                    'url': link,
                    'posted': pub_date,
                    'tags': [],
                    'source': 'WeWorkRemotely',
                })

        except Exception as e:
            print(f"    ✗ WWR feed error ({feed_url}): {e}")
            continue

    print(f"    ✓ We Work Remotely: {len(jobs)} jobs")
    return jobs