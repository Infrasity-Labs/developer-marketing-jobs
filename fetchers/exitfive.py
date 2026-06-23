import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

def fetch(categories=None):
    url = "https://jobs.exitfive.com"
    print(f"Fetching data from: {url}\n")
    jobs_found = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)
        
        # Scroll to bottom to trigger lazy loading
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        
        seen = set()
        
        # Niceboard specific selector
        cards = page.locator('.jobs li').all()
        
        for card in cards:
            text = card.inner_text().strip()
            lines = [line.strip() for line in text.split('\n') if line.strip() and line.strip() != "Save job"]
            
            if len(lines) >= 3:
                title = lines[0]
                company = lines[1]
                
                # Default values
                location = "Unknown"
                
                # Get the link
                a_tag = card.locator('a').first
                link = ""
                if a_tag:
                    href = a_tag.get_attribute('href')
                    if href:
                        if href.startswith('/'):
                            # Ensure we have the base url
                            parsed_url = urlparse(url)
                            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                            link = base_url + href
                        else:
                            link = href
                
                # Parse remaining lines
                for idx in range(2, len(lines)):
                    line = lines[idx]
                    if "$" in line or "£" in line or "€" in line or "k" in line.lower() and bool(re.search(r'\d', line)):
                        pass
                    elif idx == 2:
                        location = line
                
                if title not in seen:
                    seen.add(title)
                    jobs_found.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": link
                    })

        browser.close()
        
    return jobs_found
