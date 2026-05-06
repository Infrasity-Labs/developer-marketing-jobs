from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Test which batch codes actually work
test_batches = [
    # Old format
    "W05", "S05", "W06", "S06", "W07", "S07",
    "W08", "S08", "W09", "S09", "W10", "S10",
    "W11", "S11", "W12", "S12", "W13", "S13",
    "W14", "S14", "W15", "S15", "W16", "S16",
    "W17", "S17", "W18", "S18", "W19", "S19",
    "W20", "S20", "W21", "S21", "W22", "S22",
    "W23", "S23", "W24", "S24", "W25", "S25",
    # New 4-batch format
    "F24", "X24", "F25", "X25",
    # Alternative formats
    "W2024", "S2024", "W2025", "S2025",
    "Winter2024", "Summer2024",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for batch in test_batches:
        url = f"https://www.ycombinator.com/companies?batch={batch}"
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(1500)
        
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        count = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/companies/') and '/jobs' not in href:
                slug = href.replace('/companies/', '').strip('/')
                if slug and slug != 'companies':
                    count += 1
        
        if count > 0:
            print(f"✅ {batch}: {count} companies - URL: {url}")
        else:
            print(f"❌ {batch}: 0 companies")
    
    browser.close()