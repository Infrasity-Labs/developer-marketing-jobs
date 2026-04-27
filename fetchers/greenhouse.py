import requests

# Expanded list of devtool/SaaS companies using Greenhouse
# Focus: companies likely to hire for DevRel, Product Marketing, Growth, and Marketing leadership
COMPANIES = [
    # Developer Tools & Infrastructure
    "vercel", "netlify", "stripe", "mongodb", "twilio", "gitlab", "elastic",
    "cloudflare", "databricks", "temporal", "algolia", "sentry", "figma",
    
    # DevOps & Cloud
    "datadog", "newrelic", "pagerduty", "launchdarkly", "circleci",
    "cockroachdb", "planetscale", "neon", "railway", "fly",
    
    # Security & Auth
    "snyk", "ory", "workos", "stytch", "descope",
    
    # AI/ML Platforms
    "huggingface", "replicate", "modal", "weights-and-biases", "cohere",
    "anthropic", "scale", "labelbox",
    
    # Analytics & Product
    "segment", "amplitude", "mixpanel", "heap", "fullstory", "logrocket",
    "posthog", "june", "koala",
    
    # Collaboration & Productivity
    "notion", "coda", "airtable", "miro", "loom", "linear", "height",
    "cal", "meetgeek",
    
    # API & Integration
    "twilio", "plaid", "algolia", "mapbox", "sendgrid", "postman",
    
    # Payments & Fintech
    "stripe", "adyen", "square", "checkout", "marqeta",
    
    # Sales & Marketing Tech
    "hubspot", "intercom", "drift", "clearbit", "apollo", "outreach",
    
    # No-Code / Low-Code
    "retool", "bubble", "webflow", "zapier", "make",
    
    # Data & AI Infrastructure
    "airbyte", "fivetran", "dbt-labs", "dagster", "prefect", "astronomer",
    
    # Observability
    "honeycomb", "lightstep", "chronosphere", "grafana",
    
    # Communication
    "slack", "discord", "sendbird", "stream", "daily",
    
    # Design & Creative
    "figma", "canva", "miro", "whimsical", "pitch",
]

def fetch():
    jobs = []
    successful = 0
    failed = 0
    
    for company in COMPANIES:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
        try:
            r = requests.get(url, timeout=10)
            
            # Skip 404s silently (company doesn't use Greenhouse)
            if r.status_code == 404:
                failed += 1
                continue
                
            r.raise_for_status()
            data = r.json().get("jobs", [])
            
            if data:
                successful += 1
            
            for item in data:
                location = ""
                if item.get("location"):
                    location = item["location"].get("name", "")

                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": location or "Remote",
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse",
                })
                
        except Exception as e:
            failed += 1
            continue
    
    if successful > 0:
        print(f"    ✓ Greenhouse: {successful}/{len(COMPANIES)} companies returned jobs")
    
    return jobs