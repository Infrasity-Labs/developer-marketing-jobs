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

[Open a Feature Request →](../../issues/new?template=feature_request.yml)

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