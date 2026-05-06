import requests
import os

# Manually read .env file
env_file = '.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

login = os.getenv('DATAFORSEO_LOGIN')
password = os.getenv('DATAFORSEO_PASSWORD')

print(f'Login: {login}')
print(f'Password set: {password is not None}')

if not login or not password:
    print('ERROR: credentials not found')
    exit(1)

r = requests.post(
    'https://api.dataforseo.com/v3/serp/google/organic/live/advanced',
    auth=(login, password),
    json=[{
        'keyword': 'site:jobs.lever.co "developer advocate"',
        'location_code': 2840,
        'language_code': 'en',
        'depth': 100,
    }],
    timeout=30
)

print(f'Status: {r.status_code}')
data = r.json()
items = data.get('tasks', [{}])[0].get('result', [{}])[0].get('items', [])
print(f'Results: {len(items)}')

for item in items[:10]:
    print(f'  {item.get("url", "")}')