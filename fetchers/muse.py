params = {
    "category": "Technology",
    "location": "Remote",
    "page": 0,
}
r = requests.get(url, params=params, timeout=15)
# Add pagination
for page in range(1, 10):  # You can adjust the max page number as needed
    params['page'] = page
    try:
        r = requests.get(url, params=params, timeout=15)
        # Process the response
    except requests.RequestException as e:
        print(f'Error on page {page}: {e}')
