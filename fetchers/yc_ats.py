import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import re

CACHE_FILE = Path("yc_companies_with_jobs.json")
CACHE_DAYS = 7

def scrape_all_yc_companies():
    """Scrape YC company directory to get companies WITH job counts."""
    companies = []
    
    try:
        url = "https://www.ycombinator.com/companies"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        print("    🔍 Scraping YC company directory...")
        
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        
        print(f"    ✓ Got response ({len(r.content)} bytes)")
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Try to find __NEXT_DATA__
        next_data = soup.find('script', id='__NEXT_DATA__')
        
        if not next_data:
            print("    ⚠️  No __NEXT_DATA__ found, trying alternative methods...")
            
            # Alternative: Look for any script with company data
            all_scripts = soup.find_all('script')
            print(f"    Found {len(all_scripts)} script tags")
            
            for script in all_scripts:
                if script.string and 'companies' in script.string and 'slug' in script.string:
                    print("    📍 Found potential company data in script tag")
                    try:
                        # Try to extract JSON from various patterns
                        script_content = script.string
                        
                        # Pattern 1: window.__INITIAL_STATE__ = {...}
                        if 'window.__INITIAL_STATE__' in script_content:
                            json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script_content, re.DOTALL)
                            if json_match:
                                data = json.loads(json_match.group(1))
                                companies_data = data.get('companies', {}).get('companies', [])
                                
                                for company in companies_data:
                                    if isinstance(company, dict):
                                        slug = company.get('slug', '')
                                        name = company.get('name', '')
                                        
                                        if slug and name:
                                            companies.append({
                                                'slug': slug,
                                                'name': name,
                                                'job_count': 1,  # Assume has jobs
                                            })
                                
                                if companies:
                                    print(f"    📍 Extracted {len(companies)} companies from __INITIAL_STATE__")
                                    break
                    except Exception as e:
                        print(f"    ⚠️  Script parsing error: {e}")
                        continue
            
            # If still no companies, scrape links as fallback
            if not companies:
                print("    🔍 Falling back to link scraping...")
                links = soup.find_all('a', href=re.compile(r'^/companies/[^/]+/?$'))
                
                for link in links:
                    href = link['href']
                    match = re.match(r'^/companies/([a-zA-Z0-9-]+)/?$', href)
                    if match:
                        slug = match.group(1)
                        if slug not in ['', 'top-companies', 'jobs', 'apply', 'industries']:
                            # Try to get company name from link text
                            name = link.get_text(strip=True) or slug.replace('-', ' ').title()
                            companies.append({
                                'slug': slug,
                                'name': name,
                                'job_count': 1,
                            })
                
                # Remove duplicates
                seen = set()
                unique_companies = []
                for c in companies:
                    if c['slug'] not in seen:
                        seen.add(c['slug'])
                        unique_companies.append(c)
                
                companies = unique_companies
                print(f"    📍 Scraped {len(companies)} company links")
        
        else:
            # __NEXT_DATA__ found
            print("    ✓ Found __NEXT_DATA__ script tag")
            
            try:
                data = json.loads(next_data.string)
                
                props = data.get('props', {})
                page_props = props.get('pageProps', {})
                
                companies_data = (
                    page_props.get('companies', []) or
                    page_props.get('initialCompanies', []) or
                    page_props.get('allCompanies', []) or
                    []
                )
                
                print(f"    Found {len(companies_data)} companies in data")
                
                for company in companies_data:
                    if isinstance(company, dict):
                        slug = company.get('slug', '')
                        name = company.get('name', '')
                        job_count = company.get('num_jobs', company.get('jobCount', 1))
                        
                        if slug and name:
                            companies.append({
                                'slug': slug,
                                'name': name,
                                'job_count': job_count if job_count else 1,
                            })
                
                print(f"    📍 Extracted {len(companies)} companies from __NEXT_DATA__")
            
            except Exception as e:
                print(f"    ⚠️  JSON parsing error: {e}")
    
    except Exception as e:
        print(f"  YC directory scraping failed: {e}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
    
    return companies

def scrape_company_jobs(slug, company_name):
    """Scrape jobs from a YC company's jobs page."""
    jobs = []
    
    try:
        url = f"https://www.ycombinator.com/companies/{slug}/jobs"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 404:
            return []
        
        r.raise_for_status()
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        next_data = soup.find('script', id='__NEXT_DATA__')
        
        if next_data:
            try:
                data = json.loads(next_data.string)
                
                props = data.get('props', {})
                page_props = props.get('pageProps', {})
                
                jobs_data = (
                    page_props.get('jobs', []) or
                    page_props.get('company', {}).get('jobs', []) or
                    []
                )
                
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
                        
                        if not location:
                            location = 'Remote'
                        
                        jobs.append({
                            'title': job.get('title', ''),
                            'url': job_url,
                            'location': location,
                            'company': page_company_name,
                            'posted': job.get('created_at', job.get('postedAt', '')),
                        })
            
            except:
                pass
    
    except:
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
    
    cached_companies = load_cache()
    
    if cached_companies:
        print(f"    ✓ Using cached {len(cached_companies)} YC companies")
        companies = cached_companies
    else:
        companies = scrape_all_yc_companies()
        
        if not companies:
            print("  YC: No companies found")
            return []
        
        save_cache(companies)
    
    print(f"    🔍 Fetching jobs from {len(companies)} YC companies...")
    
    companies_fetched = 0
    
    for i, company in enumerate(companies[:100]):  # Limit to first 100 for testing
        slug = company['slug']
        name = company['name']
        
        company_jobs = scrape_company_jobs(slug, name)
        
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
        
        if (i + 1) % 20 == 0:
            print(f"      Progress: {i + 1}/100, {companies_fetched} fetched, {len(jobs)} jobs")
        
        time.sleep(0.1)
    
    print(f"    ✓ YC: {len(jobs)} jobs from {companies_fetched} companies")
    return jobs