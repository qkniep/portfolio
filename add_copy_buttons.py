#!/usr/bin/env python3
import os
import re

paper_dir = "/Users/qkniep/projects/portfolio/paper"

for filename in os.listdir(paper_dir):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(paper_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already has copy button
    if "copy-btn" in content:
        print(f"Skipping {filename} - already has copy button")
        continue

    # Check if has BibTeX section
    if "<h2>BibTeX</h2>" not in content:
        print(f"Skipping {filename} - no BibTeX")
        continue

    # Add copy button before the pre element
    old_pattern = r'(<h2>BibTeX</h2>\s+<div class="abstract">)\s*(<pre)'
    new_pattern = r'\1\n            <button class="copy-btn" onclick="copyBibtex(this)">Copy</button>\n            <pre'

    new_content = re.sub(old_pattern, new_pattern, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated {filename}")

print("Done!")
