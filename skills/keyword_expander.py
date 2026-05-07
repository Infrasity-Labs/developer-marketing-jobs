# skills/keyword_expander.py
import json
import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("expanded_keywords_cache.json")
CACHE_DAYS = 30


def run_claude(prompt):
    """
    Run Claude Code CLI in a clean isolated environment.
    Prevents Claude from reading project context.
    """
    import shutil

    claude_cmd = (
        shutil.which("claude.cmd")
        or shutil.which("claude")
        or r"C:\nvm4w\nodejs\claude.cmd"
    )

    # Clean environment - prevents Claude reading project context
    clean_env = {
        'PATH': os.environ.get('PATH', ''),
        'HOME': os.environ.get('HOME', ''),
        'USERPROFILE': os.environ.get('USERPROFILE', ''),
        'APPDATA': os.environ.get('APPDATA', ''),
        'LOCALAPPDATA': os.environ.get('LOCALAPPDATA', ''),
        'TEMP': os.environ.get('TEMP', ''),
        'TMP': os.environ.get('TMP', ''),
        'SystemRoot': os.environ.get('SystemRoot', ''),
        'SystemDrive': os.environ.get('SystemDrive', ''),
        'COMPUTERNAME': os.environ.get('COMPUTERNAME', ''),
        'USERNAME': os.environ.get('USERNAME', ''),
    }

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [claude_cmd, "-p", prompt],
                capture_output=True,
                text=True,
                timeout=120,
                encoding='utf-8',
                shell=True,
                cwd=tmpdir,
                env=clean_env
            )

            if result.returncode != 0:
                print(f"      Claude error: {result.stderr[:200]}")
                return None

            return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print("      Claude timed out after 2 minutes")
        return None
    except Exception as e:
        print(f"      Claude error: {e}")
        return None


def expand_keywords_for_category(category_label, existing_keywords):
    """Use Claude to expand keywords for a single category."""

    prompt = (
        f"List 25 job title keywords for '{category_label}' roles.\n"
        f"Exclude: {json.dumps(existing_keywords)}\n"
        "Format: JSON array only. Example:\n"
        '["senior devrel engineer", "head of developer relations", "api evangelist"]\n'
        "Rules: lowercase, 1-5 words, real job titles only.\n"
        "Reply with the JSON array only, no numbering, no explanation."
    )

    response = run_claude(prompt)

    if not response:
        return existing_keywords

    text = response.strip()
    keywords = []

    try:
        # Try JSON first
        if '[' in text:
            json_text = text[text.index('['):text.rindex(']') + 1]
            parsed = json.loads(json_text)
            keywords = [k.lower().strip() for k in parsed if isinstance(k, str) and k.strip()]

        # If JSON failed or empty, parse as numbered/bulleted list
        if not keywords:
            import re
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Remove "1. " "1) " "- " "* " prefixes
                line = re.sub(r'^[\d]+[\.\)]\s*', '', line)
                line = re.sub(r'^[-\*•]\s*', '', line)
                line = line.strip().lower()
                # Skip lines that are sentences (headers like "Here are 25...")
                if line and len(line.split()) <= 6 and not line.endswith(':'):
                    keywords.append(line)

        if keywords:
            print(f"      ✓ Got {len(keywords)} new keywords")
            return list(set(existing_keywords + keywords))

        return existing_keywords

    except Exception as e:
        print(f"      Parse error: {e}")
        print(f"      Raw: {text[:200]}")
        return existing_keywords
    
    except Exception as e:
        print(f"      Parse error: {e}")
        print(f"      Raw: {response[:200]}")
        return existing_keywords
        
def expand_all_categories(categories):
    """Expand keywords for all categories."""
    expanded_categories = []

    for i, cat in enumerate(categories):
        label = cat["label"]
        original_keywords = cat["keywords"]

        print(f"    [{i+1}/{len(categories)}] {label}")

        new_keywords = expand_keywords_for_category(label, original_keywords)

        # Merge original + new, deduplicate
        all_keywords = list(set(original_keywords + new_keywords))
        new_count = len(all_keywords) - len(original_keywords)

        print(f"      {len(original_keywords)} → {len(all_keywords)} keywords (+{new_count} new)")

        expanded_categories.append({
            "label": label,
            "keywords": all_keywords,
            "original_keywords": original_keywords,
        })

    return expanded_categories


def load_cache():
    """Load expanded keywords from cache."""
    if not CACHE_FILE.exists():
        return None
    try:
        data = json.loads(CACHE_FILE.read_text())
        cache_date = datetime.fromisoformat(data["updated_at"])
        if datetime.now() - cache_date > timedelta(days=CACHE_DAYS):
            print("    Cache expired, regenerating...")
            return None
        return data["categories"]
    except:
        return None


def save_cache(categories):
    """Save expanded keywords to cache."""
    CACHE_FILE.write_text(json.dumps({
        "updated_at": datetime.now().isoformat(),
        "categories": categories,
    }, indent=2))
    print(f"    💾 Cached to {CACHE_FILE}")


def is_claude_available():
    """Check if Claude Code CLI is installed."""
    import shutil

    claude_cmd = (
        shutil.which("claude.cmd")
        or shutil.which("claude")
        or r"C:\nvm4w\nodejs\claude.cmd"
    )

    clean_env = {
        'PATH': os.environ.get('PATH', ''),
        'USERPROFILE': os.environ.get('USERPROFILE', ''),
        'APPDATA': os.environ.get('APPDATA', ''),
        'LOCALAPPDATA': os.environ.get('LOCALAPPDATA', ''),
        'SystemRoot': os.environ.get('SystemRoot', ''),
    }

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [claude_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=15,
                shell=True,
                cwd=tmpdir,
                env=clean_env
            )
            return result.returncode == 0
    except:
        return False


def get_expanded_categories(categories):
    """
    Main function — returns categories with expanded keywords.
    Uses cache if available, otherwise calls Claude Code CLI.
    """
    if not is_claude_available():
        print("    ⚠️ Claude Code CLI not available — using original keywords")
        return categories

    # Try cache first
    cached = load_cache()
    if cached:
        cached_labels = {c["label"] for c in cached}
        current_labels = {c["label"] for c in categories}
        if cached_labels == current_labels:
            print(f"    ✓ Using cached expanded keywords")
            return cached
        print("    Categories changed, regenerating...")

    # Expand with Claude
    print("    🤖 Expanding keywords with Claude Code CLI...")
    expanded = expand_all_categories(categories)
    save_cache(expanded)

    return expanded