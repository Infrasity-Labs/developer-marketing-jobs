import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

def fetch(categories=None):
    url = "https://jobs.superpath.co"
    print(f"Fetching dynamic data from: {url}\n")
    jobs_found = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set User Agent
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Navigate and wait for network activity to settle
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)
        
        # Scroll to bottom to trigger any lazy loaded items
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        
        seen = set()
        
        # Find elements that could be list items
        # On Softr, list items often have classes like "list-item" or are contained in a div with "list" in the class
        # On Niceboard, list items are usually under ul.jobs > li
        cards = page.locator('.list-item, [role="listitem"], .jobs li').all()
        
        # Fallback to general div wrappers if specific list-item class is missing
        if not cards:
            cards = page.locator('div[class*="sw-border-style-solid"], section div[class*="MuiGrid-item"]').all()

        if not cards:
            h3s = page.locator('h3').all()
            cards = [h3.locator('..') for h3 in h3s]
            
        if not cards:
            # Super fallback: extract lines manually
            body_text = page.locator('body').inner_text()
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            for i in range(len(lines)):
                if "Lead" in lines[i] or "Manager" in lines[i] or "Editor" in lines[i] or "Writer" in lines[i]:
                    title = lines[i]
                    company = lines[i+3] if i+3 < len(lines) else "Unknown"
                    if title not in seen:
                        seen.add(title)
                        jobs_found.append({
                            "title": title, 
                            "company": company, 
                            "location": "Unknown",
                            "url": url
                        })

        else:
            for card in cards:
                text = card.inner_text().strip()
                lines = [line.strip() for line in text.split('\n') if line.strip() and line.strip() != "Save job"]
                
                # A job card typically has more than 1 line (title, company, maybe salary, date)
                if len(lines) >= 2:
                    title = lines[0]
                    
                    company = "Unknown"
                    location = "Unknown"
                    
                    for line in reversed(lines):
                        if "Inc" in line or "LLC" in line or len(line.split()) < 4:
                            if line != title and not any(char.isdigit() for char in line):
                                company = line
                                break
                    
                    if company == "Unknown":
                        company = lines[-1] if len(lines) > 1 else "Unknown"
                    
                    # Try to extract location (often the 3rd line)
                    if len(lines) >= 3:
                        location = lines[2]
                        if location == company or "time" in location.lower() or "$" in location or "£" in location:
                            location = "Unknown"

                    # Get apply link
                    a_tag = card.locator('a').first
                    link = url
                    if a_tag:
                        try:
                            href = a_tag.get_attribute('href')
                            if href:
                                if href.startswith('/'):
                                    parsed_url = urlparse(url)
                                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                                    link = base_url + href
                                else:
                                    link = href
                        except Exception:
                            pass
                        
                    if title not in seen and len(title) > 3:
                        seen.add(title)
                        jobs_found.append({
                            "title": title, 
                            "company": company, 
                            "location": location, 
                            "url": link
                        })

        browser.close()
        
    return jobs_found
