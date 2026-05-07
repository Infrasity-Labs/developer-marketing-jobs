# Expand Greenhouse Company List

## Purpose
Auto-discover and expand the list of companies using Greenhouse ATS that hire for developer marketing roles.
Currently we have a hardcoded list of ~96 companies cached every 7 days. This skill finds new ones automatically.

## When to use
- Monthly refresh to discover new companies
- When you notice a company is missing from job listings
- After a major tech hiring wave (new companies adopt Greenhouse)
- When `greenhouse_jobs.json` seems low on results

## How to use
```bash
# From repo root
claude skills/expand-greenhouse-companies.md
```

## What this skill does
1. Reads current company list from `fetchers/greenhouse.py`
2. Checks `discovered_greenhouse_companies.json` for already-discovered companies
3. Searches for new devtool/SaaS companies using Greenhouse ATS
4. Validates each new company actually has a Greenhouse board
5. Updates the company list in `fetchers/greenhouse.py`
6. Shows summary of new companies found

---

## Instructions for Claude

### Step 1: Read current state
Read these files and report:
- `fetchers/greenhouse.py` — current hardcoded company list (how many companies?)
- `discovered_greenhouse_companies.json` — cached discovered companies (how many?)
- `greenhouse_all_companies.json` — any other cached lists

Show me: