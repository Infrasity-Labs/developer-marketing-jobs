import requests

# Add company slugs here. Find them by visiting a company's careers page —
# if it's hosted on Greenhouse, the URL looks like boards.greenhouse.io/COMPANY
COMPANIES = [
    "vercel",
    "hashicorp",
    "stripe",
    "mongodb",
    "twilio",
    "auth0",
    "gitlab",
    "elastic",
    "cloudflare",
    "render",
    "netlify",
    "airbyte",
    "posthog",
    "supabase",
    "replit",
    "linear",
    "notion",
    "figma",
    "databricks",
    "temporal",
    "algolia",
    "confluent",
    "dbtlabs",
    "sentry",
    "gitpod",
    "clerk",
    "pinecone",
    "weaviate"
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json().get("jobs", [])
        except Exception as e:
            print(f"  Greenhouse: failed to fetch {company}: {e}")
            continue

        for item in data:
            location = ""
            if item.get("location"):
                location = item["location"].get("name", "")

            jobs.append({
                "title": item.get("title", ""),
                "company": company.capitalize(),
                "location": location or "Not specified",
                "url": item.get("absolute_url", ""),
                "posted": item.get("updated_at", ""),
                "tags": [],  # Greenhouse doesn't expose tags via this endpoint
                "source": "Greenhouse",
            })
    return jobs