from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

CACHE_FILE = Path("yc_all_companies.json")
CACHE_DAYS = 7

def get_all_yc_companies():
    """Get all YC companies from the YC directory."""
    companies = set()
    
    try:
        print("    🔍 Fetching all YC companies from directory...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto("https://www.ycombinator.com/companies", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)
            
            # Aggressive scrolling to load ALL companies
            previous_count = 0
            no_change_count = 0
            
            for scroll_num in range(500):  # Up to 200 scrolls
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)  # Wait longer for content to load
                
                # Check current count every 10 scrolls
                if scroll_num % 10 == 0:
                    html = page.content()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    current_companies = set()
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('/companies/') and '/jobs' not in href:
                            slug = href.replace('/companies/', '').strip('/')
                            if slug and slug != 'companies':
                                current_companies.add(slug)
                    
                    current_count = len(current_companies)
                    print(f"      Scroll {scroll_num + 1}: {current_count} companies loaded...")
                    
                    if current_count == previous_count:
                        no_change_count += 1
                        if no_change_count >= 3:
                            print(f"      ✓ Stopped at {current_count} companies (no new ones)")
                            companies = current_companies
                            break
                    else:
                        no_change_count = 0
                        companies = current_companies
                        previous_count = current_count
            
            browser.close()
        
        print(f"    📍 Found {len(companies)} YC companies from directory")
        
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
    
    return list(companies)


def scrape_all_jobs(company_slugs):
    """Scrape jobs from all companies using a single browser instance."""
    all_jobs = []
    companies_with_jobs = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, slug in enumerate(company_slugs):
            try:
                url = f"https://www.ycombinator.com/companies/{slug}/jobs"
                
                response = page.goto(url, wait_until="domcontentloaded", timeout=10000)
                
                if response and response.status == 404:
                    continue
                
                page.wait_for_timeout(1000)  # Reduced wait time
                
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                data_div = soup.find('div', {'data-page': True})
                
                if data_div:
                    data_page_json = data_div['data-page']
                    data = json.loads(data_page_json)
                    
                    props = data.get('props', {})
                    job_postings = props.get('jobPostings', [])
                    
                    if job_postings:
                        companies_with_jobs += 1
                        company_name = props.get('company', {}).get('name', slug.capitalize())
                        
                        for job in job_postings:
                            all_jobs.append({
                                'title': job.get('title', ''),
                                'url': f"https://www.ycombinator.com{job.get('url', '')}",
                                'location': job.get('location', 'Remote'),
                                'company': company_name,
                                'posted': job.get('createdAt', ''),
                            })
                
                if (i + 1) % 50 == 0:
                    print(f"      Progress: {i + 1}/{len(company_slugs)}, {companies_with_jobs} with jobs, {len(all_jobs)} jobs")
                
                time.sleep(0.1)  # Small delay to avoid rate limiting
                
            except Exception as e:
                continue
        
        browser.close()
    
    return all_jobs, companies_with_jobs

def load_cache():
    if not CACHE_FILE.exists():
        return None
    
    try:
        data = json.loads(CACHE_FILE.read_text())
        cache_date = datetime.fromisoformat(data["updated_at"])
        
        if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
            return None
        
        return data["companies"]
    except:
        return None

def save_cache(companies):
    data = {
        "updated_at": datetime.now().isoformat(),
        "companies": companies,
    }
    CACHE_FILE.write_text(json.dumps(data, indent=2))

def fetch():
    cached_companies = load_cache()
    
    if cached_companies:
        print(f"    ✓ Using cached {len(cached_companies)} YC companies")
        company_slugs = cached_companies
    else:
        company_slugs = get_all_yc_companies()
        
        if not company_slugs:
            print("  YC: No companies found")
            return []
        
        save_cache(company_slugs)
    
    print(f"    🔍 Fetching jobs from {len(company_slugs)} YC companies...")
    
    all_jobs, companies_with_jobs = scrape_all_jobs(company_slugs)
    
    jobs = []
    for job in all_jobs:
        jobs.append({
            "title": job['title'],
            "company": job['company'],
            "location": job['location'],
            "url": job['url'],
            "posted": job.get('posted', ''),
            "tags": [],
            "source": "YC",
        })
    
    print(f"    ✓ YC: {len(jobs)} jobs from {companies_with_jobs}/{len(company_slugs)} companies")
    return jobs