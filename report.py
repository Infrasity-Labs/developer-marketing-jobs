"""Turn the day's categorized jobs into the README body plus chart statistics.

build_report() returns the markdown that goes between the JOBS markers and a
stats dict that readme_assets.write_all() draws into SVGs.
"""
import re
from collections import Counter
from urllib.parse import urlparse

from main import CATEGORIES, MAX_JOBS_PER_CATEGORY, categorize
from readme_assets import bar_key

SHOW = 8                      # rows visible per section before "Show more"
ASSETS = "./.github/assets"
ATS_COUNT, BOARD_COUNT = 5, 14

YC = {
    "label": "Y Combinator Startups",
    "description": "Open roles at Y Combinator-backed startups.",
}

# --------------------------------------------------------------------------- cleanup

_AGE = re.compile(r"(?i)^(about\s+)?\d+\s+(minute|hour|day|week|month|year)s?\s+ago$")

def clean_job(job):
    """Fix known scraper quirks without touching the source dict."""
    j = dict(job)
    title = (j.get("title") or "").strip()
    company = (j.get("company") or "").strip()
    # Superpath rows arrive as "Title·Company" with an emoji in the company field
    if "·" in title and (not re.search(r"[A-Za-z0-9]", company) or company.lower().startswith("unknown")):
        title, company = (p.strip() for p in title.rsplit("·", 1))
    loc = (j.get("location") or "").strip()
    # DevRelJobs sometimes puts "1 month ago" where the location should be
    if _AGE.match(loc) or loc.lower() in {"unknown", "n/a", "-", "—"}:
        loc = ""
    j["title"], j["company"], j["location"] = title, company, loc
    return j

# --------------------------------------------------------------------------- classification

_US_STATES = ("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM "
              "NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC").split()
_STATE_RE = re.compile(r"(?:,|\s)\s*(?:" + "|".join(_US_STATES) + r")\b(?!\w)")
_REGIONS = [
    ("North America", ("united states", "usa", "u.s.", "canada", "toronto", "vancouver", "new york", "nyc",
                       "san francisco", "seattle", "boston", "austin", "chicago", "los angeles", "california",
                       "texas", "washington", "virginia", "florida", "colorado", "north america", "americas",
                       "remote-us", "us-based", "bay area", "atlanta", "denver", "mississauga", "ontario", "montreal",
                       "montréal", "quebec", "ottawa", "calgary", "dallas", "philadelphia", "pennsylvania",
                       "louisiana", "new jersey", "connecticut", "palo alto", "culver city", "el segundo",
                       "us only", "us hybrid", "amer", "georgia", "ohio", "michigan", "illinois",
                       "massachusetts", "oregon", "utah", "arizona", "nevada", "carolina", "tennessee",
                       "maryland", "minnesota", "missouri", "indiana", "wisconsin", "oklahoma", "kansas",
                       "kentucky", "alabama", "houston", "miami", "portland", "san diego", "san jose",
                       "washington dc", "brooklyn", "raleigh", "charlotte", "nashville", "pittsburgh")),
    ("Europe & UK", ("united kingdom", "england", "london", "uk", "europe", "emea", "germany", "berlin", "munich",
                     "france", "paris", "spain", "madrid", "barcelona", "netherlands", "amsterdam", "ireland",
                     "dublin", "poland", "warsaw", "sweden", "stockholm", "denmark", "copenhagen", "norway",
                     "finland", "italy", "milan", "portugal", "lisbon", "switzerland", "zurich", "austria",
                     "vienna", "belgium", "czech", "prague", "romania", "slovakia", "serbia", "bulgaria",
                     "hungary", "greece", "barcelone", "duesseldorf", "düsseldorf", "frankfurt", "belgrade",
                     "macedonia", "hamburg", "cologne", "brussels", "lyon", "rotterdam", "utrecht", "manchester",
                     "edinburgh", "oxford", "krakow", "bucharest", "sofia", "tallinn", "riga", "vilnius",
                     "helsinki", "oslo", "gothenburg", "malmo", "geneva", "basel", "rome", "turin", "valencia",
                     "porto", "ukraine", "kyiv", "luxembourg", "malta", "cyprus", "tbilisi", "lithuania", "estonia", "latvia", "croatia", "scotland")),
    ("Asia-Pacific", ("india", "bangalore", "bengaluru", "mumbai", "gurugram", "gurgaon", "delhi", "hyderabad",
                      "pune", "chennai", "singapore", "japan", "tokyo", "australia", "sydney", "melbourne",
                      "china", "korea", "seoul", "hong kong", "apac", "pakistan", "lahore", "islamabad",
                      "karachi", "philippines", "malaysia", "indonesia", "vietnam", "thailand", "new zealand",
                      "taiwan", "bangladesh", "shanghai", "beijing", "shenzhen", "jakarta", "manila", "taguig",
                      "noida", "brisbane", "geebung", "perth", "auckland", "kolkata", "ahmedabad",
                      "kuala lumpur", "bangkok", "hanoi", "ho chi minh", "metro manila", "kochi")),
    ("Latin America", ("brazil", "sao paulo", "são paulo", "argentina", "buenos aires", "colombia", "chile",
                       "peru", "mexico", "méxico", "bogota", "bogotá", "medellin", "santiago", "latam", "latin america", "costa rica", "uruguay")),
    ("Middle East & Africa", ("israel", "tel aviv", "uae", "dubai", "abu dhabi", "saudi", "egypt", "nigeria",
                              "lagos", "south africa", "cape town", "kenya", "nairobi", "africa", "turkey",
                              "istanbul", "qatar", "mena")),
]

def _has(word, text):
    return re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", text) is not None

_NOT_LOCATIONS = {"hybrid", "full-time", "full time", "part-time", "hq", "all", "onsite", "on-site", "on site",
                  "contract", "multiple locations", "various", "global"}

def region_of(job):
    raw = job.get("location") or ""
    loc = raw.lower()
    if not loc.strip() or loc.strip() in _NOT_LOCATIONS:
        return "Not stated"
    if "remote" in loc or "anywhere" in loc or "distributed" in loc or "work from home" in loc:
        return "Remote"
    for name, words in _REGIONS:
        if any(_has(w, loc) for w in words):
            return name
    if _STATE_RE.search(raw):
        return "North America"
    return "Other"

_ATS_HOSTS = ("greenhouse.io", "lever.co", "ashbyhq.com", "workable.com", "workatastartup.com",
              "recruitee.com", "personio.de", "personio.com")

def source_kind(job):
    """ATS feeds / Company careers sites / Job boards / Hand-curated."""
    url = job.get("url") or ""
    host = urlparse(url).netloc.lower()
    if job.get("source") in ("Manual", "LinkedIn") or "linkedin.com" in host:
        return "Hand-curated"
    if any(host.endswith(h) for h in _ATS_HOSTS):
        return "ATS feeds"
    if "gh_jid=" in url or "gh_src=" in url or job.get("source") in ("Greenhouse", "Lever", "Ashby", "Workable", "YC"):
        return "Company careers sites"
    return "Job boards"

# --------------------------------------------------------------------------- markdown

def slug(heading):
    text = re.sub(r"[^\w\- ]", "", heading.lower(), flags=re.UNICODE)
    return text.replace(" ", "-")

def picture(name, alt, width=None):
    w = f' width="{width}"' if width else ""
    return (f'<picture>\n'
            f'  <source media="(prefers-color-scheme: dark)" srcset="{ASSETS}/{name}-dark.svg">\n'
            f'  <img{w} alt="{alt}" src="{ASSETS}/{name}-light.svg">\n'
            f'</picture>')

def _cut(text, n):
    text = (text or "").replace("|", "/").replace("\n", " ").strip()
    return text if len(text) <= n else text[:n - 1].rstrip(" ,;/-–") + "…"

def table(jobs, new_urls):
    lines = ["| Role | Company | Location | |", "|:--|:--|:--|:-:|"]
    for j in jobs:
        tag = f' <img src="{ASSETS}/new.svg" height="16" alt="new">' if j["url"] in new_urls else ""
        loc = _cut(j["location"], 40) or "—"
        lines.append(f"| **{_cut(j['title'], 90)}**{tag} | {_cut(j['company'], 40) or '—'} | {loc} | [Apply ↗]({j['url']}) |")
    return "\n".join(lines)

def section(label, description, jobs, new_urls):
    n_new = sum(1 for j in jobs if j["url"] in new_urls)
    new_txt = f" · <b>{n_new}</b> new since the last run" if n_new else ""
    out = [f"## {label}", "",
           f"{description}<br>",
           f"<sub><b>{len(jobs)}</b> open{new_txt} · <a href=\"#browse-by-role\">back to top ↑</a></sub>", ""]
    if not jobs:
        out += ["_No open roles in the last 90 days. Check back tomorrow._", ""]
        return "\n".join(out)
    head, rest = jobs[:SHOW], jobs[SHOW:]
    out += [table(head, new_urls), ""]
    if rest:
        out += ["<details>", f"<summary><b>Show {len(rest)} more {label} roles</b></summary>", "",
                table(rest, new_urls), "", "</details>", ""]
    return "\n".join(out)

SOURCES_TABLE = """<details>
<summary><b>Where the jobs come from</b></summary>

| Type | Sources |
|:--|:--|
| **ATS platforms (5)** | [Greenhouse](https://www.greenhouse.com) · [Lever](https://www.lever.co) · [Ashby](https://www.ashbyhq.com) · [Workable](https://www.workable.com) · [Y Combinator](https://www.ycombinator.com/jobs) |
| **Job boards (14)** | RemoteOK · Remotive · Adzuna · Arbeitnow · Jobicy · Himalayas · We Work Remotely · The Muse · DevRelJobs · DevRelJob · TheMinCave · DevToolJobs · ExitFive · Superpath |
| **Hand-curated** | Roles from LinkedIn and elsewhere, added in [`manual_jobs.json`](./manual_jobs.json) |

Links go to the company's own posting wherever one exists, not a reposted copy.

</details>"""

# --------------------------------------------------------------------------- report

def build_report(jobs, yc_jobs, when, previous_urls=None):
    """Return (markdown, total, stats). `jobs`/`yc_jobs` are already filtered and deduped."""
    previous_urls = previous_urls or set()
    jobs = [clean_job(j) for j in jobs]
    yc_jobs = [clean_job(j) for j in yc_jobs]

    buckets = {cat["label"]: [] for cat in CATEGORIES}
    for j in jobs:
        label = categorize(j, CATEGORIES)
        if label:
            buckets[label].append(j)
    for label in buckets:
        buckets[label] = buckets[label][:MAX_JOBS_PER_CATEGORY]

    yc_all = [j for j in yc_jobs if categorize(j, CATEGORIES)][:MAX_JOBS_PER_CATEGORY]

    groups = [(cat["label"], cat.get("description", ""), buckets[cat["label"]]) for cat in CATEGORIES]
    groups.append((YC["label"], YC["description"], yc_all))

    everything = [j for _, _, js in groups for j in js]
    new_urls = {j["url"] for j in everything if previous_urls and j["url"] not in previous_urls}
    # newest first inside each section; sort is stable so the nightly order is kept otherwise
    groups = [(l, d, sorted(js, key=lambda j: j["url"] not in new_urls)) for l, d, js in groups]

    total = len(everything)
    added = sum(1 for j in everything if j["url"] in new_urls)

    cats = [{"label": l, "count": len(js), "new": sum(1 for j in js if j["url"] in new_urls)} for l, _, js in groups]

    names = Counter()
    for j in everything:
        name = re.sub(r"\s+", " ", j["company"]).strip()
        if name and re.search(r"[A-Za-z0-9]", name):
            names[name.lower()] += 1
    display = {}
    for j in everything:
        display.setdefault(j["company"].strip().lower(), j["company"].strip())
    top = [(display.get(n, n.title()), c) for n, c in names.most_common(10)]

    reg = Counter(region_of(j) for j in everything)
    order = ["North America", "Remote", "Europe & UK", "Asia-Pacific", "Latin America", "Middle East & Africa", "Other", "Not stated"]
    regions = sorted(((r, reg[r]) for r in order if reg[r]), key=lambda t: -t[1])

    mix = Counter(source_kind(j) for j in everything)
    mix_order = ["ATS feeds", "Job boards", "Company careers sites", "Hand-curated"]
    source_mix = sorted(((k, mix[k]) for k in mix_order if mix[k]), key=lambda t: -t[1])

    stats = {
        "total": total, "added": added, "when": when,
        "companies": len(names), "remote_pct": round(100 * reg["Remote"] / total) if total else 0,
        "top_companies": top, "regions": regions, "source_mix": source_mix, "cats": cats,
        "ats": ATS_COUNT, "boards": BOARD_COUNT,
    }

    # ---- markdown
    rows = ["| Role family | Open | New | |", "|:--|--:|--:|:--|"]
    for (label, _, _), cat in zip(groups, cats):
        new_cell = f"+{cat['new']}" if cat["new"] else "—"
        rows.append(f"| [{label}](#{slug(label)}) | **{cat['count']}** | {new_cell} | "
                    f"{picture('bars/' + bar_key(label), str(cat['count']) + ' roles')} |".replace("\n", " "))
    parts = [
        "## Browse by role", "", "\n".join(rows), "",
        "<sub>Bars share one scale. The darker part of each bar is roles added in the last run.</sub>", "",
        "## Market snapshot", "",
        '<p align="center">',
        picture("top-companies", "Top 10 companies by open roles", "49%"),
        picture("regions", "Open roles by region", "49%"),
        "</p>", "",
        '<p align="center">', picture("source-mix", "Where listings come from", "100%"), "</p>", "",
        SOURCES_TABLE, "",
    ]
    for label, desc, js in groups:
        parts += [section(label, desc, js, new_urls), ""]
    return "\n".join(parts), total, stats
