import requests

COMPANIES = [
    "contentful", "adjust", "aircall", "personio", "sennder",
]

def fetch():
    jobs = []
    for company in COMPANIES:
        url = f"https://{company}.jobs.personio.de/xml"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            
            # Personio returns XML, would need parsing
            # Skip for now or add xml parsing
            continue
        except Exception:
            continue
    
    return jobs