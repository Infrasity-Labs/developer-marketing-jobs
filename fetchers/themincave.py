import urllib.request
import json
import ssl
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch(categories=None):
    url = "https://jobs.themincave.com"
    print(f"Fetching data from: {url}\n")
    jobs_found = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            html = response.read().decode('utf-8')
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # JobBoardly structure: ul role="list" > li > a href="/jobs/..."
        # Or look for all 'a' tags with href containing '/jobs/' and a h3 title
        job_links = soup.find_all('a', href=True)
        
        for a in job_links:
            href = a['href']
            if '/jobs/' in href:
                h3 = a.find('h3')
                if h3:
                    title = h3.get_text(strip=True)
                    
                    company = "Unknown"
                    location = "Unknown"
                    
                    # Company is often in a specific p tag
                    # In JobBoardly, there's <p class="text-sm truncate" ...>Company</p> directly after the h3
                    parent_div = h3.parent
                    if parent_div:
                        company_p = parent_div.find('p', class_='truncate')
                        if company_p:
                            company = company_p.get_text(strip=True)
                    
                    # Location is usually in a span inside a flex div below, or simply the next text elements
                    # We can grab all text from the card to find 'Remote' or other locations
                    all_text = a.get_text(separator='|', strip=True)
                    parts = all_text.split('|')
                    for i, part in enumerate(parts):
                        if part.lower() in ['remote', 'hybrid', 'on-site']:
                            location = part
                            break
                        if "remote" in part.lower() or "worldwide" in part.lower() or "global" in part.lower():
                            location = part
                            break

                    if location == "Unknown" and len(parts) >= 3:
                        # Fallback heuristic: Location is often one of the last few items
                        location = parts[-1]
                        if location == company or len(location.split()) > 4:
                            location = "Unknown"
                    
                    # Build full apply link
                    if href.startswith('/'):
                        parsed_url = urlparse(url)
                        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        apply_link = base_url + href
                    else:
                        apply_link = href
                        
                    # Filter out obvious footer or navigation blocks
                    lower_text = all_text.lower()
                    if "privacy policy" in lower_text or "got questions" in lower_text or "t&cs" in lower_text:
                        continue
                        
                    # Avoid duplicates
                    if not any(j['title'] == title and j['company'] == company for j in jobs_found):
                        jobs_found.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": apply_link
                        })
                        
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")
        
    return jobs_found
