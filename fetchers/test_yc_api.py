from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Show browser
    page = browser.new_page()
    
    # Capture all network requests
    requests = []
    
    def capture_request(request):
        if 'job' in request.url.lower() or 'search' in request.url.lower() or 'api' in request.url.lower():
            requests.append({
                'url': request.url,
                'method': request.method,
                'post_data': request.post_data
            })
            print(f"📡 {request.method} {request.url}")
    
    page.on('request', capture_request)
    
    page.goto("https://www.workatastartup.com/jobs", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(5000)
    
    # Try interacting with filters
    print("\n🔍 Looking for filters or search...")
    
    # Check if there are filter options
    filters = page.locator('select, input[type="checkbox"], button[role="tab"]').all()
    print(f"Found {len(filters)} interactive elements")
    
    # Save all requests
    with open('yc_requests.json', 'w') as f:
        json.dump(requests, f, indent=2)
    
    input("Press Enter to close browser...")
    browser.close()

print("\n✅ Check yc_requests.json for API endpoints")