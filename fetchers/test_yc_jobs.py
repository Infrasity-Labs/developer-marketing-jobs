from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

print("Testing workatastartup.com with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False so you can see it
    page = browser.new_page()
    
    # Capture API calls
    api_calls = []
    
    def log_request(request):
        if 'api' in request.url or '.json' in request.url or 'graphql' in request.url:
            api_calls.append(request.url)
            print(f"📡 API call: {request.url}")
    
    page.on('request', log_request)
    
    # Go to the jobs page
    page.goto("https://www.workatastartup.com/jobs", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(5000)
    
    # Scroll to trigger more API calls
    for i in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
    
    # Get the HTML
    html = page.content()
    
    # Check for React data
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for __NEXT_DATA__
    next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
    if next_data_script:
        print("\n✅ Found __NEXT_DATA__ script!")
        data = json.loads(next_data_script.string)
        
        # Try to find job data
        print("\nKeys in __NEXT_DATA__:")
        print(json.dumps(list(data.keys()), indent=2))
        
        # Save for inspection
        with open('next_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("💾 Saved to next_data.json")
    
    # Look for data-page attribute
    data_page_div = soup.find('div', {'data-page': True})
    if data_page_div:
        print("\n✅ Found data-page div!")
        data = json.loads(data_page_div['data-page'])
        with open('data_page.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("💾 Saved to data_page.json")
    
    print(f"\n📊 Total API calls captured: {len(api_calls)}")
    for url in set(api_calls):
        print(f"  - {url}")
    
    browser.close()

print("\n✅ Check next_data.json or data_page.json for job listings!")