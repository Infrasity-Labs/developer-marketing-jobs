import requests

def fetch():
    jobs = []
    
    try:
        # Himalayas API endpoint
        url = "https://himalayas.app/api/jobs"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        
        data = r.json()
        
        # The response structure might be different - handle both possible formats
        job_list = data.get("data", data.get("jobs", []))
        
        for item in job_list:
            # Handle nested company object
            company = item.get("company", {})
            company_name = company.get("name", "") if isinstance(company, dict) else company
            
            jobs.append({
                "title": item.get("title", ""),
                "company": company_name,
                "location": item.get("location", "Remote"),
                "url": item.get("url", item.get("apply_url", "")),
                "posted": item.get("published_at", item.get("created_at", "")),
                "tags": item.get("tags", []),
                "source": "Himalayas",
            })
            
    except Exception as e:
        print(f"  Himalayas: {e}")
        return []
    
    print(f"    ✓ Himalayas: {len(jobs)} jobs")
    return jobs