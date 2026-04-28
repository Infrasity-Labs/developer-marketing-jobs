import requests
from bs4 import BeautifulSoup
import time

def discover_companies():
    """Scrape Greenhouse's customer directory to find all companies using their ATS."""
    companies = set()
    
    try:
        # Greenhouse doesn't have a public directory page, but we can use Google
        # to find companies by searching site:boards.greenhouse.io
        
        # Alternative: use a known list of tech companies and test each one
        # This is a starter list of ~200 known tech companies
        potential_companies = [
            # AI/ML
            "openai", "anthropic", "huggingface", "scale", "cohere", "replicate",
            "modal", "weights-and-biases", "labelbox", "snorkel",
            
            # DevTools
            "vercel", "netlify", "railway", "render", "fly", "cloudflare",
            "datadog", "newrelic", "sentry", "honeycomb", "lightstep",
            "launchdarkly", "split", "statsig", "posthog", "amplitude",
            
            # Infra
            "stripe", "plaid", "twilio", "sendgrid", "segment", "algolia",
            "mongodb", "planetscale", "neon", "cockroachdb", "supabase",
            
            # Productivity
            "notion", "linear", "height", "coda", "airtable", "retool",
            "zapier", "webflow", "framer", "figma", "canva", "miro",
            
            # Security
            "snyk", "vanta", "drata", "secureframe", "ory", "workos",
            "clerk", "auth0", "stytch", "descope", "frontegg",
            
            # Data
            "airbyte", "fivetran", "hightouch", "census", "rudderstack",
            "dbt-labs", "dagster", "prefect", "astronomer", "mage",
            
            # Communication
            "slack", "discord", "sendbird", "stream", "daily", "whereby",
            "intercom", "drift", "clearbit", "apollo", "clay",
            
            # Sales/CRM
            "hubspot", "salesforce", "pipedrive", "close", "attio",
            "apollo", "outreach", "salesloft",
            
            # Finance
            "brex", "ramp", "mercury", "gusto", "rippling", "deel",
            "remote", "oyster", "multiplier", "papaya",
            
            # Add more here...
        ]
        
        # Test each company to see if they have a Greenhouse board
        for company in potential_companies:
            try:
                url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
                r = requests.get(url, timeout=5)
                
                if r.status_code == 200:
                    data = r.json()
                    if data.get("jobs"):
                        companies.add(company)
                
                time.sleep(0.1)  # Be nice to their servers
                
            except:
                continue
        
    except Exception as e:
        print(f"  Discovery error: {e}")
    
    return list(companies)

def fetch():
    """Fetch jobs from all discovered Greenhouse companies."""
    jobs = []
    
    # Discover companies (this could be cached to avoid running every time)
    companies = discover_companies()
    
    if not companies:
        print("  Greenhouse Discovery: No companies found")
        return []
    
    print(f"    📍 Discovered {len(companies)} active Greenhouse companies")
    
    # Now fetch jobs from each
    for company in companies:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            for item in r.json().get("jobs", []):
                location = item.get("location", {}).get("name", "Remote")
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "url": item.get("absolute_url", ""),
                    "posted": item.get("updated_at", ""),
                    "tags": [],
                    "source": "Greenhouse (Auto)",
                })
        except:
            continue
    
    print(f"    ✓ Greenhouse Discovery: {len(jobs)} jobs from {len(companies)} companies")
    return jobs