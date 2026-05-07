from main import CATEGORIES
from skills.keyword_expander import get_expanded_categories

expanded = get_expanded_categories(CATEGORIES)
print()

for cat in expanded:
    orig = cat.get('original_keywords', [])
    new = [k for k in cat['keywords'] if k not in orig]
    label = cat['label']
    total = len(cat['keywords'])
    print(f"{label}")
    print(f"  {len(orig)} -> {total} keywords (+{len(new)} new)")
    print(f"  Sample new: {new[:3]}")
    print()

# Summary
total_orig = sum(len(c.get('original_keywords', [])) for c in expanded)
total_new = sum(len(c['keywords']) for c in expanded)
print(f"TOTAL: {total_orig} -> {total_new} keywords across all categories")