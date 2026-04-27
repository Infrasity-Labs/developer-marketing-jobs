import requests

def fetch():
    jobs = []
    keywords = ["developer advocate", "technical writer", "product marketing", "growth marketing"]
    
    for keyword in keywords:
        try:
            # Wellfound/AngelList has a search endpoint
            url = f"https://api.wellfound.com/public/jobs?search={keyword}"
            r = requests.get(url, timeout=15)
            
            # May need different parsing
            # ...
        except Exception:
            continue
    
    return jobs