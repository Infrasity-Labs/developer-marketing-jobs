import requests
import json
import urllib.parse

url = "https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.16.1)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=NzllNTY5MzJiZGM2OTY2ZTQwMDEzOTNhYWZiZGRjODlhYzVkNjBmOGRjNzJiMWM4ZTU0ZDlhYTZjOTJiMjlhMWFuYWx5dGljc1RhZ3M9eWNkYyZyZXN0cmljdEluZGljZXM9WUNDb21wYW55X3Byb2R1Y3Rpb24lMkNZQ0NvbXBhbnlfQnlfTGF1bmNoX0RhdGVfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVE"

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.ycombinator.com",
    "Referer": "https://www.ycombinator.com/"
}

raw_filter = '[["batch:Winter 2025"]]'
encoded_filter = urllib.parse.quote(raw_filter)
params = f"query=&hitsPerPage=3&page=0&facetFilters={encoded_filter}"

payload = {"requests": [{"indexName": "YCCompany_production", "params": params}]}
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# Print ALL fields of first company
print("First company fields:")
print(json.dumps(data['results'][0]['hits'][0], indent=2))