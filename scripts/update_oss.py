#!/usr/bin/env python3
"""
Auto-updates the OSS contributions table in README.md.
Searches GitHub for merged PRs by USERNAME to external repos,
fetches live star counts, and regenerates the table.
"""
import os
import re
import json
import time
import urllib.request
import urllib.error
from collections import defaultdict

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "JiwaniZakir"
README_PATH = "README.md"
MIN_STARS = 1000  # only include repos with 1K+ stars

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "oss-update-script",
}

# Short descriptions to use instead of raw repo descriptions (keep concise)
DESCRIPTIONS = {
    "langchain-ai/langchain": "LLM application framework",
    "BerriAI/litellm": "Universal LLM proxy",
    "python-poetry/poetry": "Python dependency management",
    "microsoft/graphrag": "Microsoft graph RAG",
    "langchain-ai/langgraph": "Multi-agent orchestration",
    "topoteretes/cognee": "Knowledge graph memory",
    "confident-ai/deepeval": "LLM evaluation",
}


def gh_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} for {url}")
        return None


def format_stars(n):
    if n >= 1000:
        return f"{round(n / 1000)}K"
    return str(n)


def fetch_merged_prs():
    """Return dict: repo_full -> sorted list of PR numbers."""
    prs_by_repo = defaultdict(list)
    page = 1
    while True:
        url = (
            f"https://api.github.com/search/issues"
            f"?q=is:pr+author:{USERNAME}+-user:{USERNAME}+is:merged"
            f"&per_page=100&page={page}&sort=created&order=desc"
        )
        data = gh_get(url)
        if not data:
            break
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            repo_full = item["repository_url"].split("repos/")[1]
            prs_by_repo[repo_full].append(item["number"])
        print(f"  Page {page}: {len(items)} PRs found")
        if len(items) < 100:
            break
        page += 1
        time.sleep(0.5)  # respect search rate limit
    return {k: sorted(v) for k, v in prs_by_repo.items()}


def fetch_repo_meta(repo_full):
    data = gh_get(f"https://api.github.com/repos/{repo_full}")
    if not data:
        return None
    return {
        "stars": data.get("stargazers_count", 0),
        "description": data.get("description") or "",
    }


def build_table(repos):
    """repos: list of (repo_full, stars, description, [pr_nums])"""
    rows = [
        "*Bug fixes and features across major AI/ML projects*",
        "",
        "| Project | Stars | PRs |",
        "|---------|:-----:|-----|",
    ]
    for repo_full, stars, description, pr_nums in repos:
        name = repo_full.split("/")[1]
        desc = DESCRIPTIONS.get(repo_full) or (description[:60] if description else "")
        pr_links = " · ".join(
            f"[#{n}](https://github.com/{repo_full}/pull/{n})" for n in pr_nums
        )
        rows.append(
            f"| [**{name}**](https://github.com/{repo_full}) · {desc} "
            f"| ⭐ {format_stars(stars)} | {pr_links} |"
        )
    return "\n".join(rows)


def update_readme(table):
    with open(README_PATH, "r") as f:
        content = f.read()

    new_content = re.sub(
        r"<!--START_SECTION:oss-->.*?<!--END_SECTION:oss-->",
        f"<!--START_SECTION:oss-->\n{table}\n<!--END_SECTION:oss-->",
        content,
        flags=re.DOTALL,
    )

    if new_content == content:
        print("No changes to README.")
        return False

    with open(README_PATH, "w") as f:
        f.write(new_content)
    return True


def main():
    print("Fetching merged PRs...")
    prs_by_repo = fetch_merged_prs()
    print(f"Found PRs in {len(prs_by_repo)} external repos")

    print("Fetching repo star counts...")
    repos = []
    for repo_full, pr_nums in prs_by_repo.items():
        meta = fetch_repo_meta(repo_full)
        if meta and meta["stars"] >= MIN_STARS:
            repos.append((repo_full, meta["stars"], meta["description"], pr_nums))
            print(f"  {repo_full}: {meta['stars']} stars, {len(pr_nums)} PRs")
        time.sleep(0.1)

    repos.sort(key=lambda x: x[1], reverse=True)
    print(f"\n{len(repos)} repos with {MIN_STARS}+ stars")

    table = build_table(repos)
    changed = update_readme(table)
    print("README updated." if changed else "README unchanged.")


if __name__ == "__main__":
    main()
