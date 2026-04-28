from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

CACHE_FILE = Path("yc_companies_with_jobs.json")
CACHE_DAYS = 7

def scrape_yc_companies_with_playwright():
    """Use Playwright to scrape YC company directory."""
    companies = []
    
    try:
        print("    🔍 Launching browser to scrape YC directory...")
        
        with sync_playwright() as p:
            # Set headless=False if you need to debug Cloudflare blocks
            browser = p.chromium.launch(headless=True)
            
            # Use a real user-agent to avoid immediate bot detection
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            page.goto("https://www.ycombinator.com/companies", wait_until="networkidle")
            print("    ✓ Page loaded, extracting company data...")
            page.wait_for_timeout(3000) 
            
            # Extract __NEXT_DATA__
            next_data = page.evaluate("""
                () => {
                    const scriptTag = document.getElementById('__NEXT_DATA__');
                    return scriptTag ? scriptTag.textContent : null;
                }
            """)
            
            if next_data:
                data = json.loads(next_data)
                props = data.get('props', {})
                page_props = props.get('pageProps', {})
                companies_data = page_props.get('companies', []) or page_props.get('initialCompanies', []) or []
                
                print(f"    📍 Found {len(companies_data)} companies in JSON data")
                
                for company in companies_data:
                    if isinstance(company, dict):
                        slug = company.get('slug', '')
                        name = company.get('name', '')
                        job_count = company.get('num_jobs', 0)
                        
                        if slug and name:
                            companies.append({
                                'slug': slug,
                                'name': name,
                                'job_count': job_count,
                            })
                print(f"    ✓ Extracted {len(companies)} companies")
            
            else:
                print("    ⚠️  Could not find __NEXT_DATA__, using DOM fallback...")
                
                # DOM Fallback: scrape visible company links
                company_links = page.query_selector_all('a[href^="/companies/"]')
                
                seen_slugs = set()
                for link in company_links:
                    href = link.get_attribute('href')
                    text = link.inner_text().strip()
                    
                    if href and href.startswith('/companies/'):
                        slug = href.replace('/companies/', '').strip('/')
                        
                        if slug and slug not in ['', 'top-companies', 'jobs', 'apply'] and slug not in seen_slugs:
                            seen_slugs.add(slug)
                            companies.append({
                                'slug': slug,
                                'name': text or slug.replace('-', ' ').title(),
                                'job_count': 1, # Defaulting to 1 to ensure it gets checked later
                            })
                
                print(f"    📍 Scraped {len(companies)} company links from DOM")
            
            browser.close()
    
    except Exception as e:
        print(f"  Playwright scraping failed: {e}")
    
    return companies

def scrape_company_jobs_with_playwright(slug, company_name):
    """Scrape jobs from a single company using Playwright."""
    jobs = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = f"https://www.ycombinator.com/companies/{slug}/jobs"
            response = page.goto(url, wait_until="domcontentloaded")
            
            if response.status == 404:
                browser.close()
                return []
            
            page.wait_for_timeout(2000)
            
            next_data = page.evaluate("""
                () => {
                    const scriptTag = document.getElementById('__NEXT_DATA__');
                    return scriptTag ? scriptTag.textContent : null;
                }
            """)
            
            # Strategy 1: JSON Data
            if next_data:
                data = json.loads(next_data)
                props = data.get('props', {})
                page_props = props.get('pageProps', {})
                jobs_data = page_props.get('jobs', []) or page_props.get('company', {}).get('jobs', []) or []
                page_company_name = page_props.get('company', {}).get('name', company_name)
                
                for job in jobs_data:
                    if isinstance(job, dict):
                        job_id = job.get('id', '')
                        job_url = job.get('url', '')
                        if not job_url and job_id:
                            job_url = f"https://www.ycombinator.com/companies/{slug}/jobs/{job_id}"
                        
                        location = job.get('location', 'Remote')
                        if isinstance(location, list):
                            location = ', '.join(str(loc) for loc in location if loc)
                        elif isinstance(location, dict):
                            location = location.get('name', 'Remote')
                            
                        jobs.append({
                            'title': job.get('title', ''),
                            'url': job_url,
                            'location': location or 'Remote',
                            'company': page_company_name,
                            'posted': job.get('created_at', job.get('postedAt', '')),
                        })
            
            # Strategy 2: DOM Fallback
            if not jobs:
                job_links = page.query_selector_all(f'a[href^="/companies/{slug}/jobs/"]')
                seen_urls = set()
                
                for link in job_links:
                    href = link.get_attribute('href')
                    
                    if href and href not in seen_urls and href != f"/companies/{slug}/jobs/":
                        seen_urls.add(href)
                        title = link.inner_text().strip()
                        
                        if title and title.lower() not in ['apply', 'view', 'jobs']:
                            jobs.append({
                                'title': title.split('\n')[0],
                                'url': f"https://www.ycombinator.com{href}",
                                'location': 'Unspecified/Remote', 
                                'company': company_name,
                                'posted': '',
                            })

            browser.close()
    
    except Exception as e:
        pass 
    
    return jobs

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
    jobs = []
    
    # Try cache first
    cached_companies = load_cache()
    
    if cached_companies:
        print(f"    ✓ Using cached {len(cached_companies)} YC companies")
        companies = cached_companies
    else:
        companies = scrape_yc_companies_with_playwright()
        
        if not companies:
            print("  YC: Failed to scrape companies")
            return []
        
        # Filter to only companies with jobs
        companies_with_jobs = [c for c in companies if c.get('job_count', 0) > 0]
        
        if not companies_with_jobs:
            # If no job counts available (due to fallback), take all companies
            companies_with_jobs = companies
        
        print(f"    📊 {len(companies_with_jobs)} companies have jobs (out of {len(companies)} total)")
        
        save_cache(companies_with_jobs)
        companies = companies_with_jobs
    
    # Fetch jobs from each company
    print(f"    🔍 Fetching jobs from {len(companies)} YC companies...")
    
    companies_fetched = 0
    test_limit = min(50, len(companies)) # Test with first 50 companies
    
    for i, company in enumerate(companies[:test_limit]):
        slug = company['slug']
        name = company['name']
        
        company_jobs = scrape_company_jobs_with_playwright(slug, name)
        
        if company_jobs:
            companies_fetched += 1
            jobs.extend([{
                "title": job['title'],
                "company": job['company'],
                "location": job['location'],
                "url": job['url'],
                "posted": job.get('posted', ''),
                "tags": [],
                "source": "YC",
            } for job in company_jobs])
        
        if (i + 1) % 10 == 0:
            print(f"      Progress: {i + 1}/{test_limit}, {companies_fetched} with jobs, {len(jobs)} total jobs")
        
        time.sleep(0.5)  # Slower to avoid detection
    
    print(f"    ✓ YC: {len(jobs)} jobs from {companies_fetched}/{test_limit} companies")
    return jobs