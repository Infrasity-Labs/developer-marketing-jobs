from playwright.sync_api import sync_playwright
import json
from bs4 import BeautifulSoup
import time

def fetch():
    """Scrape all jobs from workatastartup.com by clicking Load More."""
    all_jobs = []
    
    try:
        print("    🔍 Fetching YC jobs from workatastartup.com...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto("https://www.workatastartup.com/jobs", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            click_count = 0
            max_clicks = 100
            
            while click_count < max_clicks:
                # Try to find and click "Load More" or "Show More" button
                try:
                    # Look for common button texts
                    load_more_button = page.locator('button:has-text("Load"), button:has-text("Show"), button:has-text("More")').first
                    
                    if load_more_button.is_visible(timeout=2000):
                        load_more_button.click()
                        page.wait_for_timeout(1500)
                        click_count += 1
                        
                        if click_count % 10 == 0:
                            # Check current job count
                            html = page.content()
                            soup = BeautifulSoup(html, 'html.parser')
                            data_div = soup.find('div', {'data-page': True})
                            if data_div:
                                data = json.loads(data_div['data-page'])
                                jobs = data.get('props', {}).get('jobs', [])
                                print(f"      Progress: Clicked {click_count} times, {len(jobs)} jobs loaded...")
                    else:
                        print(f"      ✓ No more 'Load More' button after {click_count} clicks")
                        break
                        
                except Exception as e:
                    # No button found or timeout
                    print(f"      ✓ Finished loading, clicked {click_count} times")
                    break
            
            # Get final data
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            data_div = soup.find('div', {'data-page': True})
            
            if data_div:
                data = json.loads(data_div['data-page'])
                jobs_data = data.get('props', {}).get('jobs', [])
                
                for job in jobs_data:
                    all_jobs.append({
                        'title': job.get('title', ''),
                        'company': job.get('companyName', ''),
                        'location': job.get('location', 'Remote'),
                        'url': job.get('applyUrl', ''),
                        'posted': '',
                        'tags': [job.get('roleType', '')],
                        'source': 'YC',
                    })
        
        print(f"    ✓ YC (workatastartup): {len(all_jobs)} jobs")
        
    except Exception as e:
        print(f"    ✗ YC workatastartup error: {e}")
        import traceback
        traceback.print_exc()
    
    return all_jobs