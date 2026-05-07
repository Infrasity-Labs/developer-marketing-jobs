import { motion } from 'framer-motion';
import { Terminal, Cpu, Network, Database, Lock, Users, Clock, GitMerge, Settings, Activity } from 'lucide-react';

const DIAGRAMS = [
  {
    id: 1,
    icon: <Activity className="text-cyan-400" size={24} />,
    title: "1. HIGH-LEVEL OVERVIEW",
    shortTitle: "Overview",
    color: "from-cyan-500/20 to-blue-500/5",
    content: `
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│         GitHub Actions Workflow (Daily 6 AM UTC)                │
│                  + Manual Skills (on-demand)                    │
│                                                                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        ┌──────────────┐              ┌──────────────┐
        │ AUTOMATED    │              │  MANUAL      │
        │ DAILY CRON   │              │  CLAUDE      │
        │              │              │  SKILLS      │
        └──────┬───────┘              └──────┬───────┘
               │                             │
               ▼                             ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ 7 Parallel Jobs     │      │ User runs:          │
    │ Run Simultaneously  │      │ claude skills/...md │
    └──────────┬──────────┘      └──────────┬──────────┘
               │                             │
               ▼                             ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ Build README        │      │ Updates main.py /   │
    │ + Auto-commit       │      │ greenhouse.py       │
    └─────────────────────┘      └─────────────────────┘`
  },
  {
    id: 2,
    icon: <Network className="text-indigo-400" size={24} />,
    title: "2. COMPLETE DATA FLOW",
    shortTitle: "Data Flow",
    color: "from-indigo-500/20 to-purple-500/5",
    content: `
EXTERNAL SOURCES        DISCOVERY LAYER       FETCHERS        PROCESSING        OUTPUT
                                                                               
┌──────────────┐                          ┌──────────┐      ┌──────────┐      ┌─────────┐
│  RemoteOK    │─────── Direct API ──────▶│remoteok  │─────▶│          │      │         │
│  Public API  │                          │   .py    │      │          │      │         │
└──────────────┘                          └──────────┘      │          │      │         │
                                                            │          │      │         │
┌──────────────┐                          ┌──────────┐      │          │      │         │
│  Remotive    │─────── Direct API ──────▶│remotive  │─────▶│          │      │         │
│  Public API  │                          │   .py    │      │          │      │         │
└──────────────┘                          └──────────┘      │          │      │         │
                                                            │          │      │         │
┌──────────────┐                          ┌──────────┐      │          │      │         │
│  Adzuna API  │─────── Paid Keys ───────▶│ adzuna   │─────▶│          │      │         │
│  (4 regions) │                          │   .py    │      │          │      │         │
└──────────────┘                          └──────────┘      │          │      │         │
                                                            │ Combine  │      │         │
┌──────────────┐                          ┌──────────┐      │   All    │      │         │
│  Arbeitnow   │─────── Direct API ──────▶│arbeitnow │─────▶│  Jobs    │      │         │
│  EU Public   │                          │   .py    │      │          │      │         │
└──────────────┘                          └──────────┘      │          │      │         │
                                                            │ Categorize      │         │
┌──────────────┐                          ┌──────────┐      │ by Keyword      │         │
│  Greenhouse  │       96 hardcoded ─────▶│greenhouse│─────▶│          │─────▶│ README  │
│  Boards API  │       companies          │   .py    │      │ Filter   │      │  .md    │
└──────────────┘                          └──────────┘      │ Last     │      │         │
       ▲                                                    │ 90 days  │      │         │
       │                                                    │          │      │         │
┌──────┴───────┐    ┌──────────────┐     ┌──────────┐       │ Dedupe   │      │         │
│Common Crawl  │───▶│ Auto-Extract │────▶│greenhouse│──────▶│ company  │      │         │
│   Index      │    │ 842 slugs    │     │_cc.py    │       │ + title  │      │         │
└──────────────┘    └──────────────┘     └──────────┘       │          │      │         │
                                                            │ Sort by  │      │         │
┌──────────────┐                          ┌──────────┐      │ Date     │      │         │
│  Ashby API   │─────── Direct API ──────▶│ ashby    │─────▶│          │      │         │
│  Public      │                          │   .py    │      │ Separate │      │         │
└──────────────┘                          └──────────┘      │ YC into  │      │         │
                                                            │ own      │      │         │
┌──────────────┐    ┌──────────────┐     ┌──────────┐       │ section  │      │         │
│  YC Algolia  │───▶│Get 5,600+    │────▶│ yc_ats   │─────▶│          │      │         │
│  API         │    │ company slugs│     │   .py    │       │ Build    │      │         │
└──────────────┘    └──────────────┘     │+Playwright       │ markdown │      │         │
                                         │ (2 parallel      │ tables   │      │         │
                                         │  browsers)       │          │      │         │
                                         └──────────┘       │ Update   │      │         │
                                                            │ between  │      │         │
┌──────────────┐    ┌──────────────┐     ┌──────────┐       │ markers  │      │         │
│  DataForSEO  │───▶│ Find Lever   │────▶│ lever.py │──┐    │          │      │         │
│  SERP API    │    │ companies    │     └──────────┘  │    │          │      │         │
└──────────────┘    │ (paid)       │                   │    │          │      │         │
                    └──────────────┘                   │    │          │      │         │
                            +                          │    │          │      │         │
                    ┌──────────────┐                   ▼    │          │      │         │
                    │ Common Crawl │                ┌─────────┐        │      │         │
                    │ as fallback  │                │ Lever   │        │      │         │
                    └──────────────┘                │ Public  │───────▶│      │         │
                                                    │ API     │        │      │         │
                                                    └─────────┘        │      │         │
                                                                       │      │         │
┌──────────────┐    ┌──────────────┐     ┌──────────┐                  │      │         │
│  DataForSEO  │───▶│ Find Workable│────▶│workable  │──┐               │      │         │
│  SERP API    │    │ companies    │     │   .py    │  │               │      │         │
└──────────────┘    │ (paid)       │     └──────────┘  │               │      │         │
                    └──────────────┘                   │               │      │         │
                                                       ▼               │      │         │
                                                  ┌─────────┐          │      │         │
                                                  │Workable │          │      │         │
                                                  │Public   │─────────▶│      │         │
                                                  │API      │          │      │         │
                                                  └─────────┘          └──────┴─────────┘
                                                                             
                                          ~30,000 jobs/day        ~500 jobs in README`
  },
  {
    id: 3,
    icon: <Database className="text-emerald-400" size={24} />,
    title: "3. CACHING LAYER",
    shortTitle: "Cache Layer",
    color: "from-emerald-500/20 to-teal-500/5",
    content: `
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              💾 LOCAL JSON CACHE FILES                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

   Cache File                                TTL        Used By
   ────────────────────────────────────────────────────────────────
   yc_all_companies.json                   7 days     yc_ats.py
   discovered_lever_companies.json         30 days    lever.py
   discovered_workable_companies.json      30 days    workable.py
   discovered_greenhouse_companies.json    30 days    greenhouse_cc.py
   expanded_keywords_cache.json            30 days    keyword_expander
   dataforseo_discovered.json              30 days    DataForSEO discovery

   Flow:
   ┌──────────────┐
   │ Fetcher runs │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐   Hit      ┌──────────────┐
   │ Check cache  │───────────▶│ Use cached   │
   │ < TTL?       │            │ companies    │
   └──────┬───────┘            └──────────────┘
          │ Miss
          ▼
   ┌──────────────┐
   │ Re-discover  │
   │ + save cache │
   └──────────────┘`
  },
  {
    id: 4,
    icon: <Cpu className="text-purple-400" size={24} />,
    title: "4. CLAUDE CODE SKILLS",
    shortTitle: "Claude Skills",
    color: "from-purple-500/20 to-fuchsia-500/5",
    content: `
USER ACTION                CLAUDE PROCESSES               OUTPUT
                                                              
┌──────────────┐                                          
│ User runs:   │                                          
│ claude       │                                          
│ skills/      │                                          
│ expand-      │                                          
│ keywords.md  │                                          
└──────┬───────┘                                          
       │                                                  
       ▼                                                  
┌─────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│ Reads main.py   │───▶│ For each category:   │───▶│ Updates main.py  │
│ CATEGORIES list │    │ • Generate 30+       │    │ with expanded    │
│                 │    │   variations         │    │ keywords         │
│ 8 categories    │    │ • Add seniority      │    │                  │
│ ~10 keywords    │    │ • Add abbreviations  │    │ 8 categories     │
│ each            │    │ • Add synonyms       │    │ ~40+ keywords    │
└─────────────────┘    └──────────────────────┘    │ each             │
                                                   └──────────────────┘

┌──────────────┐                                          
│ User runs:   │                                          
│ claude       │                                          
│ skills/      │                                          
│ expand-      │                                          
│ greenhouse-  │                                          
│ companies.md │                                          
└──────┬───────┘                                          
       │                                                  
       ▼                                                  
┌─────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│ Reads current   │───▶│ • Suggests 200+      │───▶│ Updates          │
│ greenhouse.py   │    │   devtool companies  │    │ greenhouse.py    │
│                 │    │ • Validates each     │    │                  │
│ 96 companies    │    │   via Greenhouse API │    │ 96 → 200+        │
│                 │    │ • Filters non-tech   │    │ companies        │
└─────────────────┘    └──────────────────────┘    └──────────────────┘`
  },
  {
    id: 5,
    icon: <Settings className="text-rose-400" size={24} />,
    title: "5. SKILL ARCHITECTURE INTERNALS",
    shortTitle: "Skill Internals",
    color: "from-rose-500/20 to-orange-500/5",
    content: `
┌─────────────────────────────────────────────────────────────┐
│   skills/expand-keywords.md  (Claude Code skill)            │
│   skills/expand-greenhouse-companies.md                     │
│                                                             │
│   ↓ User runs in terminal                                   │
│   claude skills/expand-keywords.md                          │
│                                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Claude Code CLI     │
                │ (OAuth via Pro/Max  │
                │  subscription)      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Reads your repo     │
                │ files directly      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Edits files in      │
                │ place (main.py)     │
                └─────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│   skills/keyword_expander.py  (Python module)               │
│                                                             │
│   ↓ Imported by main.py                                     │
│   from skills.keyword_expander import get_expanded_categories│
│                                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ subprocess.run()    │
                │ ['claude', '-p',    │
                │  prompt]            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Runs in temp dir    │
                │ + clean env vars    │
                │ (prevents Claude    │
                │ reading project)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Returns JSON or     │
                │ numbered list       │
                │ (parses both)       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Caches result for   │
                │ 30 days in          │
                │ expanded_keywords_  │
                │ cache.json          │
                └─────────────────────┘`
  },
  {
    id: 6,
    icon: <GitMerge className="text-amber-400" size={24} />,
    title: "6. CATEGORIZATION LOGIC",
    shortTitle: "Categorization",
    color: "from-amber-500/20 to-yellow-500/5",
    content: `
                         ┌─────────────────┐
                         │  Raw Job Data   │
                         │  (~30,000 jobs) │
                         └────────┬────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────────┐
                  │  Get categories list:             │
                  │  • CATEGORIES from main.py        │
                  │  • OR expanded version from cache │
                  └───────────────┬───────────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │  For each job:                │
                  │  Check title + tags against   │
                  │  category keywords            │
                  └───────────────┬───────────────┘
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
       ▼                          ▼                          ▼
┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│  Matches a   │           │  No match    │           │  Source = YC │
│  category?   │           │              │           │              │
└──────┬───────┘           └──────┬───────┘           └──────┬───────┘
       │                          │                          │
       │ YES                      │                          │
       ▼                          ▼                          ▼
┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│ Add to bucket│           │   Discard    │           │ Goes into    │
│              │           │              │           │ separate YC  │
│ • DevRel     │           │              │           │ section in   │
│ • Tech Write │           │              │           │ README       │
│ • Dev Mkt    │           │              │           │              │
│ • Product Mkt│           │              │           │ Categorized  │
│ • Growth     │           │              │           │ same way     │
│ • VP Mkt     │           │              │           │              │
│ • Community  │           │              │           │              │
│ • PLG        │           │              │           │              │
└──────┬───────┘           └──────────────┘           └──────┬───────┘
       │                                                     │
       ▼                                                     ▼
┌──────────────┐                                     ┌──────────────┐
│   Filter:    │                                     │   Filter:    │
│ Last 90 days │                                     │   Last 90    │
│              │                                     │   days       │
│  Dedupe by   │                                     │  Dedupe      │
│ company+title│                                     │              │
│              │                                     │  Sort newest │
│  Sort newest │                                     │  first       │
│  first       │                                     │              │
└──────┬───────┘                                     └──────┬───────┘
       │                                                     │
       ▼                                                     ▼
┌──────────────┐                                     ┌──────────────┐
│  Main README │                                     │  YC Section  │
│   Sections   │                                     │   in README  │
│  (8 buckets) │                                     │  (8 buckets) │
└──────────────┘                                     └──────────────┘`
  },
  {
    id: 7,
    icon: <Clock className="text-lime-400" size={24} />,
    title: "7. TIMING DIAGRAM",
    shortTitle: "Timing Flow",
    color: "from-lime-500/20 to-green-500/5",
    content: `
TIME →    0 min    5 min    10 min    20 min    30 min    45 min    60 min
          │        │        │         │         │         │         │
START ────┼────────┼────────┼─────────┼─────────┼─────────┼─────────┼─────▶
          │        │        │         │         │         │         │
PARALLEL: │        │        │         │         │         │         │
          │        │        │         │         │         │         │
APIs(4)   ████░░░░░░░░░░░░░░░░░░░░░░░│         │         │         │  ✅ (5 min)
          │        │        │         │         │         │         │
Greenhouse████████████░░░░░░░░░░░░░░░│         │         │         │  ✅ (10 min)
          │        │        │         │         │         │         │
GH Crawl  ████████████████████████░░░│         │         │         │  ✅ (25 min)
          │        │        │         │         │         │         │
Ashby     ████████░░░░░░░░░░░░░░░░░░│         │         │         │  ✅ (8 min)
          │        │        │         │         │         │         │
YC        ████████████████████████████████████████████████░░░░░░░░│  ✅ (50 min)
          │        │        │         │         │         │         │
Lever     ███████████████████████████░░░░░░░░░░░░░░░░░░░│         │  ✅ (28 min)
          │        │        │         │         │         │         │
Workable  ███████████████████████████░░░░░░░░░░░░░░░░░░░│         │  ✅ (28 min)
          │        │        │         │         │         │         │
SEQUENTIAL│        │        │         │         │         │         │
          │        │        │         │         │         │         │
Build     │        │        │         │         │         │  ████░░│  ✅ (3 min)
README    │        │        │         │         │         │         │
          │        │        │         │         │         │         │
Commit    │        │        │         │         │         │        █│  ✅ (1 min)
          │        │        │         │         │         │         │
TOTAL: ~55 minutes (parallel) — was 90+ min sequentially`
  },
  {
    id: 8,
    icon: <Terminal className="text-blue-400" size={24} />,
    title: "8. SYSTEM ARCHITECTURE",
    shortTitle: "Architecture",
    color: "from-blue-500/20 to-indigo-500/5",
    content: `
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         🌐 INTERNET                                 │
│                                                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │RemoteOK │ │ Adzuna  │ │  Ashby  │ │   YC    │ │  Lever  │        │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │Remotive │ │Arbeitnow│ │Greenhouse│ │CommCrawl│ │Workable │       │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│  ┌─────────┐ ┌─────────┐                                            │
│  │Algolia  │ │DataForSEO│                                           │
│  │(YC API) │ │(Discovery)                                           │
│  └─────────┘ └─────────┘                                            │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ APIs / Web Scraping
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│              🤖 GITHUB ACTIONS (Cloud Compute)                      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │   Python 3.11 Runtime                                        │   │
│  │   ├─ 7 Parallel Fetcher Jobs                                 │   │
│  │   ├─ Playwright (browser automation, 2 parallel for YC)      │   │
│  │   ├─ DataForSEO discovery layer                              │   │
│  │   ├─ Common Crawl discovery layer                            │   │
│  │   ├─ Build README script                                     │   │
│  │   └─ Auto-commit with git rebase                             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │   Cached Data (actions/cache@v4)                             │   │
│  │   ├─ YC company slugs (7 days)                               │   │
│  │   ├─ Lever companies (30 days)                               │   │
│  │   ├─ Workable companies (30 days)                            │   │
│  │   └─ Greenhouse discovered (30 days)                         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ Auto-commit (git pull --rebase)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│           📦 GITHUB REPOSITORY (developer-marketing-jobs)           │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │   📄 README.md (auto-updated daily)                      │      │
│   │   📄 main.py / fetchers/ / skills/                       │      │
│   │   📄 CONTRIBUTING.md / LICENSE / CoC                     │      │
│   │   📁 .github/workflows + ISSUE_TEMPLATE                  │      │
│   └──────────────────────────────────────────────────────────┘      │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │                              ▲
                              │                              │
                              │ Browse / Star / Fork         │ Manual run:
                              ▼                              │ claude skills/...md
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                  👥 USERS                                           │
│                                                                     │
│  ┌──────────────────┐              ┌──────────────────┐             │
│  │  Job Seekers     │              │  Contributors    │             │
│  │                  │              │                  │             │
│  │  Browse README   │              │  Run skills      │             │
│  │  Apply to jobs   │              │  Add fetchers    │             │
│  │                  │              │  Submit PRs      │             │
│  └──────────────────┘              └──────────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘`
  },
  {
    id: 9,
    icon: <Lock className="text-red-400" size={24} />,
    title: "9. SECURITY & SECRETS FLOW",
    shortTitle: "Security",
    color: "from-red-500/20 to-orange-500/5",
    content: `
┌──────────────────┐
│ GitHub Repo      │
│ Settings         │
│ → Secrets        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  Stored Secrets:                     │
│  • ADZUNA_APP_ID                     │
│  • ADZUNA_APP_KEY                    │
│  • DATAFORSEO_LOGIN                  │
│  • DATAFORSEO_PASSWORD               │
│  • ANTHROPIC_API_KEY (optional)      │
└────────┬─────────────────────────────┘
         │
         │ Injected as env vars
         ▼
┌──────────────────────────────────────┐
│  GitHub Actions Workflow             │
│  ├─ Adzuna fetcher uses keys         │
│  ├─ Lever uses DataForSEO            │
│  └─ Workable uses DataForSEO         │
└──────────────────────────────────────┘

   For local dev: same vars in .env file
   .env is in .gitignore (never committed)`
  },
  {
    id: 10,
    icon: <Users className="text-pink-400" size={24} />,
    title: "10. CONTRIBUTOR FLOW",
    shortTitle: "Contributors",
    color: "from-pink-500/20 to-rose-500/5",
    content: `
NEW USER WANTS TO USE SKILLS LOCALLY:

   ┌─────────────────────┐
   │ git clone repo      │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │ pip install -r      │
   │ requirements.txt    │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │ npm install -g      │
   │ @anthropic-ai/      │
   │ claude-code         │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │ claude login        │
   │ (OAuth via Pro/Max) │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │ Run skills:         │
   │ • expand-keywords   │
   │ • expand-greenhouse │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │ Files updated       │
   │ Commit & push PR    │
   └─────────────────────┘`
  }
];

export default function Architecture() {
  
  // Smooth scroll function for the index buttons
  const scrollToDiagram = (id) => {
    const element = document.getElementById(`diagram-${id}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  // Animation variants for the index grid
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.05, delayChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15, scale: 0.95 },
    visible: { opacity: 1, y: 0, scale: 1, transition: { type: 'spring', stiffness: 100 } }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 py-24 relative overflow-hidden">
      
      {/* Background Ambient Glows */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-cyan-600/10 rounded-full blur-[150px] pointer-events-none"></div>

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="font-quicksand text-5xl font-bold text-white mb-6 tracking-tight">
            System <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Blueprints</span>
          </h1>
          <p className="font-inter text-slate-400 max-w-2xl mx-auto text-lg">
            A comprehensive breakdown of the automated pipelines, parsing algorithms, and cloud infrastructure powering the job board.
          </p>
        </motion.div>

        {/* 🚀 THE NEW INTERACTIVE INDEX UI 🚀 */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mb-32"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent to-slate-800"></div>
            <span className="font-quicksand font-bold text-slate-400 uppercase tracking-widest text-sm">Quick Navigation</span>
            <div className="h-[1px] flex-1 bg-gradient-to-l from-transparent to-slate-800"></div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {DIAGRAMS.map((diagram) => (
              <motion.button
                key={`nav-${diagram.id}`}
                variants={itemVariants}
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => scrollToDiagram(diagram.id)}
                className={`flex flex-col items-center justify-center gap-3 p-4 bg-slate-900/50 border border-slate-800 rounded-xl transition-all hover:bg-slate-800 hover:shadow-lg hover:border-slate-600 group relative overflow-hidden`}
              >
                {/* Subtle hover gradient background based on the diagram's theme color */}
                <div className={`absolute inset-0 bg-gradient-to-br ${diagram.color} opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none`}></div>
                
                <div className="relative z-10 p-2 bg-slate-950 rounded-lg group-hover:scale-110 transition-transform duration-300 ring-1 ring-slate-800">
                  {diagram.icon}
                </div>
                <span className="relative z-10 font-inter text-xs font-bold text-slate-300 group-hover:text-white transition-colors">
                  {diagram.id}. {diagram.shortTitle}
                </span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Blueprint Cards */}
        <div className="space-y-32">
          {DIAGRAMS.map((diagram) => (
            <motion.div
              id={`diagram-${diagram.id}`}
              key={diagram.id}
              initial={{ opacity: 0, y: 50, scale: 0.98 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, ease: "easeOut" }}
              className="relative group scroll-mt-32" 
            >
              {/* Decorative Window Bar */}
              <div className="absolute -top-4 left-0 right-0 h-10 bg-slate-900/80 rounded-t-2xl border-x border-t border-slate-800 flex items-center px-4 gap-2 z-20 backdrop-blur-md">
                <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                <div className="ml-4 flex items-center gap-2 font-mono text-xs text-slate-500 font-bold tracking-wider">
                  {diagram.icon}
                  {diagram.title}
                </div>
              </div>

              {/* Terminal Body */}
              <div className={`relative bg-gradient-to-br ${diagram.color} rounded-2xl border border-slate-800/50 p-1 shadow-2xl backdrop-blur-sm overflow-hidden`}>
                
                {/* Subtle animated overlay grid */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none opacity-20"></div>

                <div className="bg-slate-950/90 rounded-xl p-8 pt-12 overflow-x-auto custom-scrollbar relative z-10">
                  <pre className="font-mono text-sm leading-relaxed text-slate-300 whitespace-pre">
                    <code>{diagram.content}</code>
                  </pre>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

      </div>

      <style dangerouslySetInnerHTML={{__html: `
        html {
          scroll-behavior: smooth;
        }
        .custom-scrollbar::-webkit-scrollbar {
          height: 8px;
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(15, 23, 42, 0.5);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(71, 85, 105, 0.8);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(99, 102, 241, 0.8);
        }
      `}} />
    </div>
  );
}