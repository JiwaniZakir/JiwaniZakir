#!/usr/bin/env python3
"""
Generate language stats from GitHub API and update README with progress bars.
Runs via GitHub Actions on a schedule.
"""
import os
import re
import requests
from collections import defaultdict

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
USERNAME = os.environ.get("GITHUB_USERNAME", "JiwaniZakir")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
BAR_WIDTH = 25
TOP_N = 7

SKIP_LANGS = {"HTML", "CSS", "Makefile", "Dockerfile", "Shell"}


def get_repos():
    repos, page = [], 1
    while True:
        r = requests.get(
            f"https://api.github.com/users/{USERNAME}/repos",
            headers=HEADERS,
            params={"per_page": 100, "page": page, "type": "owner"},
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [r for r in repos if not r.get("fork")]


def get_language_totals(repos):
    totals = defaultdict(int)
    for repo in repos:
        r = requests.get(repo["languages_url"], headers=HEADERS)
        if r.status_code == 200:
            for lang, nbytes in r.json().items():
                if lang not in SKIP_LANGS:
                    totals[lang] += nbytes
    return totals


def progress_bar(pct, width=BAR_WIDTH):
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def build_stats_block(totals):
    total = sum(totals.values())
    if not total:
        return "No language data available."

    top = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:TOP_N]
    lines = []
    for lang, nbytes in top:
        pct = nbytes / total * 100
        bar = progress_bar(pct)
        lines.append(f"{lang:<24} {bar}   {pct:5.2f} %")
    return "\n".join(lines)


def update_readme(block):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!--START_SECTION:languages-->"
    end = "<!--END_SECTION:languages-->"

    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end), re.DOTALL
    )
    replacement = f"{start}\n```text\n{block}\n```\n{end}"

    if start not in content:
        print("ERROR: markers not found in README.md")
        return

    new_content = pattern.sub(replacement, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated.")


if __name__ == "__main__":
    print(f"Fetching repos for {USERNAME}...")
    repos = get_repos()
    print(f"  {len(repos)} repos found")
    totals = get_language_totals(repos)
    print(f"  {len(totals)} languages aggregated")
    block = build_stats_block(totals)
    print(block)
    update_readme(block)
