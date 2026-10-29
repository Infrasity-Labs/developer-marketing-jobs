import re
import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://devtooljobs.com/marketing/rss.xml"


def fetch():
    jobs = []
    try:
        r = requests.get(FEED_URL, timeout=20)
        r.raise_for_status()
        root = ET.fromstring(r.content)
    except Exception as e:
        print(f"    ✗ DevToolJobs: {e}")
        return jobs

    for item in root.iter("item"):
        raw_title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        if not raw_title or not url:
            continue

        # Feed titles look like "Product Marketing Manager II at Mollie"
        m = re.match(r"^(.*)\s+at\s+(.+)$", raw_title)
        title, company = (m.group(1).strip(), m.group(2).strip()) if m else (raw_title, "")

        posted = ""
        pub = item.findtext("pubDate")
        if pub:
            try:
                posted = parsedate_to_datetime(pub).isoformat()
            except Exception:
                pass

        jobs.append({
            "title": title,
            "company": company,
            "location": "Remote",
            "url": url,
            "posted": posted,
            "tags": [],
            "source": "DevToolJobs",
        })

    print(f"    ✓ DevToolJobs: {len(jobs)} jobs")
    return jobs
