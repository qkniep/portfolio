#!/usr/bin/env python3
"""Fetch repositories from GitHub and generate portfolio data."""

import json
import re
import urllib.request

GITHUB_USER = "qkniep"
API_URL = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&sort=updated"

# Repos to highlight on the projects page (ordered by relevance)
FEATURED = [
    "alpenglow",
    "pqwg-rust",
    "js-regex",
    "multi-paxos-rs",
    "Simetra",
]

# Repos to skip (dotfiles, meta, etc.)
SKIP = {
    "qkniep",
    "dotfiles",
    "portfolio",
    "arewefinanceyet",
    "advent-of-code",
    "cryptopals",
    "xsv",
    "sprs",
    "rprs",
    "rayon",
    "agave",
    "sui",
    "erigon",
    "blockchain",
    "RPi_MusicServer",
    "eBIMS",
    "general-incremental-sliding-window-aggregation",
    "nw",
}

# Forks that are actually maintained/interesting — include despite fork=True
INCLUDE_FORKS = {"pqwg-rust"}

LANG_MAP = {
    "Rust": "rust",
    "Go": "go",
    "Python": "python",
    "C++": "cpp",
    "Haskell": "haskell",
    "TypeScript": "typescript",
    "Shell": "shell",
}

req = urllib.request.Request(API_URL, headers={"User-Agent": "portfolio-script"})
with urllib.request.urlopen(req) as resp:
    all_repos = json.loads(resp.read().decode())

repos = []
for r in all_repos:
    if r.get("fork") and r["name"] not in INCLUDE_FORKS:
        continue
    if r["name"] in SKIP:
        continue
    if r["name"].startswith("."):
        continue
    if r.get("archived"):
        continue

    desc = r.get("description") or ""
    if len(desc) > 120:
        desc = desc[:117] + "..."

    repos.append(
        {
            "name": r["name"],
            "stars": r["stargazers_count"],
            "language": r.get("language") or "",
            "description": desc,
            "url": r["html_url"],
            "featured": r["name"] in FEATURED,
            "lang_tag": LANG_MAP.get(
                r.get("language"), (r.get("language") or "").lower()
            ),
        }
    )

# Sort: featured first, then by stars descending
repos.sort(key=lambda x: (-int(x["featured"]), -x["stars"]))

with open("repos.json", "w") as f:
    json.dump(repos, f, indent=2)

print(f"Saved {len(repos)} repos to repos.json")
for r in repos:
    marker = " ★" if r["featured"] else "  "
    print(
        f"{marker} {r['name']:40s} ★{r['stars']:4d}  {r['language']:10s}  {r['description'][:70]}"
    )
