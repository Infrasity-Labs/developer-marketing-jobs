import requests
import json
import time
import urllib.parse # Added for URL encoding

# 1. Your full Algolia URL
url = "https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.16.1)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=NzllNTY5MzJiZGM2OTY2ZTQwMDEzOTNhYWZiZGRjODlhYzVkNjBmOGRjNzJiMWM4ZTU0ZDlhYTZjOTJiMjlhMWFuYWx5dGljc1RhZ3M9eWNkYyZyZXN0cmljdEluZGljZXM9WUNDb21wYW55X3Byb2R1Y3Rpb24lMkNZQ0NvbXBhbnlfQnlfTGF1bmNoX0RhdGVfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVE"
headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://www.ycombinator.com",
    "Referer": "https://www.ycombinator.com/"
}

# IMPORTANT: Ensure these match EXACTLY what is in the YC dropdown.
# If "W24" doesn't work, try "Winter 2024" or whatever exact text the filter uses.
# New line

# Generate all YC batches from 2005 to 2024
# Create an empty list
batches = []

# The four possible seasons
seasons = ["Winter", "Spring", "Summer", "Fall"]

# Loop through every year from 2005 to 2026
for year in range(2005, 2027): 
    for season in seasons:
        batches.append(f"{season} {year}")

# Reverse the list so it starts at Fall 2026 and works backwards to 2005
batches.reverse()

# Optional: Add any weird one-off batches if you see them, like "IK12" (an old YC fellowship)
# batches.append("IK12")

all_company_names = []

print("Starting extraction...")

for batch in batches:
    print(f"\nFetching companies from batch: {batch}")
    page = 0
    has_more = True
    
    while has_more:
        # Create the raw filter string
        raw_filter = f'[["batch:{batch}"]]'
        
        # URL-encode the filter so Algolia can read it
        encoded_filter = urllib.parse.quote(raw_filter)
        
        # Construct the params string with the encoded filter
        params = f"query=&hitsPerPage=100&page={page}&facetFilters={encoded_filter}"
        
        payload = {
            "requests": [
                {
                    "indexName": "YCCompany_production",
                    "params": params
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Debugging: Print total hits found for this batch
            total_hits = data['results'][0].get('nbHits', 0)
            if page == 0:
                print(f" -> Algolia found {total_hits} total companies for {batch}")
            
            hits = data['results'][0].get('hits', [])
            
            if not hits:
                has_more = False
                break
                
            for company in hits:
                all_company_names.append(company.get('name'))
                
            page += 1
            time.sleep(1) 
            
        else:
            print(f"Error fetching page {page} for batch {batch}: {response.status_code}")
            print("Response:", response.text)
            has_more = False

print(f"\nSuccessfully extracted {len(all_company_names)} company names!")

with open("yc_companies_new.txt", "w", encoding="utf-8") as f:
    for name in all_company_names:
        f.write(name + "\n")
        
print("Saved to yc_companies_new.txt")