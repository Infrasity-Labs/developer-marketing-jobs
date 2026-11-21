# Contributing to Developer Marketing Jobs

Thank you for helping make this the best developer marketing job board on the internet! 🎉

This repo is maintained by [Infrasity](https://infrasity.com) and updated daily via GitHub Actions.

---

## Ways to Contribute

### 1. Submit a Job Opening
Know of a DevRel, Technical Writing, Developer Marketing, or Community role that's not listed?

[Open a Job Submission issue →](../../issues/new?template=job_submission.yml)

### 2. Add a Company
Know a devtool company we're missing from our sources?

[Open a Company Request issue →](../../issues/new?template=company_request.yml)

### 3. Fix a Bug
Found broken links, wrong categorization, or duplicate listings?

[Open a Bug Report →](../../issues/new?template=bug_report.yml)

### 4. Add a New Source
Know a job board or ATS we're not pulling from?

[Open a Company / Source Request →](../../issues/new?template=company_request.yml)

### 5. Improve the Code
Want to improve fetchers, fix bugs, or add new features? See the dev setup below.

---

## Development Setup

### Prerequisites
- Python 3.11+
- Git

### Local Setup

```bash
# Clone the repo
git clone https://github.com/Infrasity-Labs/developer-marketing-jobs.git
cd developer-marketing-jobs

# Install dependencies
pip install -r requirements.txt

# Install Playwright (for YC fetcher)
playwright install chromium

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running Locally

```bash
# Run all fetchers and update README
python main.py

# Run a single fetcher to test
python -c "from fetchers import greenhouse; jobs = greenhouse.fetch(); print(len(jobs))"
```

### Project Structure

```text
.
├── main.py                 # Role categories, keyword matching, dedupe, README rendering
├── build_readme.py         # CI entry point: loads fetcher artifacts, rebuilds README sections
├── fetchers/               # One module per source (ATS platform or job board), each exposes fetch()
├── skills/                 # Optional Claude-powered keyword expansion
├── manual_jobs.json        # Hand-curated roles no fetcher picks up yet
├── *_companies.json        # Company/board lists and discovery caches for each ATS
├── test/                   # Ad-hoc scripts for probing sources and filters
├── GithubPages/front/      # React + Vite front end deployed to GitHub Pages
└── .github/workflows/      # update-jobs.yml (nightly build), deploy-pages.yml
```

### How the README is generated

Everything between `<!-- JOBS:START -->` and `<!-- JOBS:END -->` is rewritten by the nightly workflow, as are the `STATS` and `TOC` blocks near the top. Edit the rest of `README.md` freely, but never hand-edit those blocks.

### Adding a Source

1. Create `fetchers/<name>.py` with a `fetch()` that returns a list of dicts with `title`, `company`, `location`, `url`, `posted`, and `source`.
2. Add `<name>` to the matrix in `.github/workflows/update-jobs.yml` (or add its own job and list it in `build-readme`'s `needs`).
3. Update the source table in `README.md` and the badge counts if you added a new ATS platform.

### Adding a Role Category or Keyword

Edit `CATEGORIES` in `main.py`. A job is placed in the first category whose keyword matches its title or tags.

---

## Pull Requests

- Keep PRs focused and describe what changed and why. The [PR template](.github/PULL_REQUEST_TEMPLATE.md) will guide you.
- Never commit secrets. API keys belong in `.env` (git-ignored) locally and in repository secrets in CI.
- Be kind. See the [Code of Conduct](CODE_OF_CONDUCT.md).
