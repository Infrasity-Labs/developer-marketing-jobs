from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Show browser so you can see
    page = browser.new_page()
    
    # Intercept all network requests to find the real API
    api_calls = []
    
    def capture(request):
        if any(x in request.url for x in ['api', 'algolia', 'search', 'companies', 'graphql']):
            print(f"📡 {request.method} {request.url}")
            if request.post_data:
                print(f"   Body: {request.post_data[:200]}")
            api_calls.append(request.url)
    
    page.on('request', capture)
    
    page.goto("https://www.ycombinator.com/companies", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    print("\n🔍 Now look at the page - find the batch filter dropdown and click it...")
    print("Waiting 15 seconds for you to interact with the page...")
    page.wait_for_timeout(15000)
    
    # Save all API calls
    with open('api_calls.json', 'w') as f:
        json.dump(list(set(api_calls)), f, indent=2)
    
    print("\n✅ API calls saved to api_calls.json")
    browser.close()