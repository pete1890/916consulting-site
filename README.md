# 916consulting.com

Static site for 916 Consulting, LLC. No build system for the main page; edit
`index.html` directly.

## NJ AI Watch (`/nj-ai-watch/`)

Content lives in `nj-ai-watch/data/entries.json`. To publish an update:

1. Edit `entries.json` (add, edit, or remove entries)
2. `cd nj-ai-watch && python3 build.py`
3. Commit and push; GitHub Pages deploys automatically

The tracker is updated monthly at minimum. Check `review_by` dates during each
monthly pass and reverify anything overdue.
