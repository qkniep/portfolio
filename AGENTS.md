# AGENTS.md

## Repo overview

Static portfolio website for Quentin Kniep (CS researcher). Contains:
- `index.html`, `research.html`, `engineering.html` — main pages
- `research/` — 14 paper detail HTML files
- `engineering/` — 5 project detail HTML files
- `css/style.css` — retro-futuristic industrial theme
- `js/` — grain.js, dots.js (visual effects)
- Favicon: `favicon.svg` with `[QK]` logo

## Commands

No build system. Edit HTML directly.

## Conventions

- External links: `target="_blank" rel="noopener noreferrer"`
- Footer text: `Built with conviction (and <a href="https://opencode.ai/">OpenCode</a>)`
- Paper detail HTML structure: `<div class="detail-layout">` with `<div class="detail-main">` and `<div class="detail-sidebar">`
- Name format: "Quentin Kniep" (no title, no middle name)
- Author highlighting in lists: `<span class="self">Quentin Kniep</span>`
- Paper sidebar elements: Venue (tag), Year, Authors, Citations, Links

## Common tasks

- Update abstract: Edit the `<div class="abstract"><p>...</p></div>` in detail-main
- Fix sidebar link: Edit `<a href="...">` in detail-sidebar
- Add slides link: Add new `<a href="...">Slides &#8599;</a>` in Links block

## Style reference

Colors (from css/style.css):
- `--accent: #c8a44e` (amber/gold)
- `--bg-primary: #0d0d0d` (near black)
- Fonts: Space Mono, JetBrains Mono
