# Keyword Expander for Developer Marketing Job Board

## Purpose
Expand the job category keywords in `main.py` to improve job matching coverage.
Currently each category has ~10 hardcoded keywords. This skill expands them to 40+ using Claude's knowledge of real job titles.

## When to use
Run this skill when:
- You've added a new category to `main.py` and want keywords expanded
- Jobs you expect to see aren't showing up in the README
- You want to improve categorization coverage
- It's been 30+ days since last keyword expansion

## How to use
```bash
# From your repo root
claude skills/expand-keywords.md
```

## What this skill does
1. Reads current CATEGORIES from `main.py`
2. For each category, generates 30+ additional job title keywords
3. Merges new keywords with existing ones (no duplicates)
4. Updates `main.py` with the expanded keyword lists
5. Shows a summary of what was added

## Instructions for Claude

### Step 1: Read current categories
Read `main.py` and extract the CATEGORIES list. Show me the current state:
- How many categories exist
- How many keywords each category currently has
- Total keyword count

### Step 2: Expand keywords for each category
For each category in CATEGORIES, generate 30+ additional keywords that:
- Are real job titles used by actual companies
- Belong specifically to that category
- Include seniority variations (Senior, Staff, Lead, Head of, Director, VP, Principal)
- Include abbreviations and synonyms
- Are 1-5 words, lowercase

**Categories to expand:**

#### 🎤 Developer Advocate / DevRel
Add keywords like: devrel engineer, developer relations manager, api evangelist, technical evangelist, developer experience engineer, dx engineer, head of developer relations, vp of developer relations, developer community manager, open source advocate, developer educator, developer programs manager, developer success engineer, technical community manager, platform evangelist, field engineer devrel, developer outreach manager, staff developer advocate, principal developer advocate

#### ✍️ Technical Writing & Documentation
Add keywords like: technical writer, docs engineer, documentation engineer, information architect, content engineer, api documentation writer, documentation lead, staff technical writer, principal technical writer, head of documentation, docs lead, developer documentation manager, technical content writer, documentation specialist, knowledge base manager, docs platform engineer, technical editor, documentation architect

#### 📣 Developer Marketing
Add keywords like: developer content manager, technical content strategist, developer growth marketer, developer brand manager, content marketing manager, technical content lead, developer education manager, developer programs manager, developer marketing lead, head of developer marketing, vp developer marketing, developer marketing specialist, technical marketing manager, developer content creator, api marketing manager

#### 📦 Product Marketing
Add keywords like: product marketing manager, senior product marketing manager, staff product marketing manager, principal pmm, head of product marketing, vp product marketing, director product marketing, technical product marketing manager, solutions marketing manager, product marketing lead, competitive intelligence manager, go-to-market manager, gtm lead, product launch manager, market intelligence manager, solutions marketing lead

#### 📈 Head of Growth
Add keywords like: growth marketing manager, senior growth manager, head of growth marketing, vp growth, director of growth, growth lead, lifecycle marketing manager, performance marketing manager, senior lifecycle marketing manager, acquisition marketing manager, retention marketing manager, growth hacker, growth operations manager, growth product manager, user acquisition manager, senior performance marketing manager

#### 👔 VP Marketing
Add keywords like: chief marketing officer, cmo, vp marketing, vice president marketing, svp marketing, evp marketing, head of marketing, director of marketing, marketing director, senior director marketing, marketing lead, global head of marketing, regional marketing director, fractional cmo, interim cmo, marketing executive

#### 👥 Community
Add keywords like: community manager, senior community manager, head of community, director of community, community lead, community operations manager, community programs manager, developer community manager, online community manager, community growth manager, community engagement manager, community advocate, forum manager, discord community manager, slack community manager, community builder, community strategist

#### 🎯 Product Led Growth
Add keywords like: plg manager, product led growth manager, head of plg, product growth manager, self serve growth manager, product adoption manager, activation manager, onboarding manager, product growth lead, plg engineer, growth product manager, product-led sales manager, expansion revenue manager, user onboarding specialist, product engagement manager

### Step 3: Update main.py
After generating keywords for all categories, update the CATEGORIES list in `main.py`:

1. For each category, ADD the new keywords to the existing `keywords` list
2. Remove duplicates
3. Keep all original keywords
4. Sort alphabetically within each category for readability

The format should remain exactly the same:
```python
{
    "label": "🎤 Developer Advocate / DevRel",
    "keywords": [
        "developer advocate",
        "developer relations", 
        # ... all expanded keywords here
    ],
},
```

### Step 4: Show summary
After updating, show:
- Before/after keyword count for each category
- Total keywords before vs after
- Sample of new keywords added per category

### Step 5: Test the expansion
Run this command to verify the changes work:
```bash
python -c "from main import CATEGORIES; total = sum(len(c['keywords']) for c in CATEGORIES); print(f'Total keywords: {total}')"
```

## Expected output example