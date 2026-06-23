import urllib.request
import json
import ssl
import re
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

def fetch(categories=None):
    url = "https://www.devreljobs.com"
    jobs_found = []
    try:
        # Adding a User-Agent header as some websites block requests without it
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        req = urllib.request.Request(url, headers=headers)
        
        print(f"Fetching data from: {url}\n")
        with urllib.request.urlopen(req) as response:
            data = response.read()
            text_data = data.decode('utf-8')
            
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Strategy 1: Find all json-ld scripts (works for devreljob.com)
            script_pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.IGNORECASE | re.DOTALL)
            scripts = script_pattern.findall(text_data)
            
            for script in scripts:
                try:
                    parsed = json.loads(script)
                    # Support for standard ItemList containing JobPosting objects
                    if parsed.get('@type') == 'ItemList' and 'itemListElement' in parsed:
                        for element in parsed['itemListElement']:
                            item = element.get('item', {})
                            if item.get('@type') == 'JobPosting':
                                title = item.get('title', 'No Title')
                                company = item.get('hiringOrganization', {}).get('name', 'Unknown')
                                
                                # Extract location
                                location = "Unknown"
                                job_loc = item.get('jobLocation', [])
                                if isinstance(job_loc, list) and len(job_loc) > 0:
                                    loc_obj = job_loc[0]
                                    addr = loc_obj.get('address', {})
                                    parts = []
                                    if addr.get('addressLocality'): parts.append(addr.get('addressLocality'))
                                    if addr.get('addressRegion'): parts.append(addr.get('addressRegion'))
                                    if addr.get('addressCountry'): parts.append(addr.get('addressCountry'))
                                    if parts: location = ", ".join(parts)
                                elif isinstance(job_loc, dict):
                                    addr = job_loc.get('address', {})
                                    parts = []
                                    if addr.get('addressLocality'): parts.append(addr.get('addressLocality'))
                                    if addr.get('addressRegion'): parts.append(addr.get('addressRegion'))
                                    if addr.get('addressCountry'): parts.append(addr.get('addressCountry'))
                                    if parts: location = ", ".join(parts)
                                    
                                apply_url = item.get('url', url)
                                jobs_found.append({
                                    "title": title, 
                                    "company": company, 
                                    "location": location,
                                    "url": apply_url
                                })
                except json.JSONDecodeError:
                    continue
            
            # Strategy 2: HTML Parsing via BeautifulSoup (works for devreljobs.com)
            if not jobs_found and BeautifulSoup is not None:
                soup = BeautifulSoup(text_data, 'html.parser')
                # Look for anchor tags going to a job detail page
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if '/jobs/' in href:
                        h3 = a_tag.find('h3')
                        if h3:
                            title = h3.get_text(strip=True)
                            # Looking for the company name, usually nearby or in a span with font-medium
                            company_span = a_tag.find('span', class_='font-medium')
                            company = company_span.get_text(strip=True) if company_span else 'Unknown Company'
                            
                            # Location might be in another span
                            spans = a_tag.find_all('span')
                            location = "Unknown"
                            for span in spans:
                                txt = span.get_text(strip=True)
                                if txt and txt != company and txt != "•" and len(txt) > 3:
                                    location = txt
                            
                            apply_link = href
                            if apply_link.startswith('/'):
                                apply_link = base_url + apply_link
                            
                            # Avoid duplicates
                            if not any(j['title'] == title and j['company'] == company for j in jobs_found):
                                jobs_found.append({
                                    "title": title, 
                                    "company": company, 
                                    "location": location,
                                    "url": apply_link
                                })
            
    except urllib.error.URLError as e:
        print(f"Failed to reach the server. Reason: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return jobs_found
