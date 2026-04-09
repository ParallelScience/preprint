#!/usr/bin/env bash
# Publish the preprint: compile PDF, update docs/ metadata, and push to gh-pages.
#
# Usage:
#   ./publish.sh          # build + update docs/ + push to gh-pages branch
#   ./publish.sh --dry    # build + update docs/ but don't push
#
# Regular pushes to master never trigger a Pages rebuild.
# Only this script pushes to gh-pages, which triggers the rebuild
# and Parallel ArXiv re-scrape.

set -euo pipefail
cd "$(dirname "$0")"

DRY=false
[[ "${1:-}" == "--dry" ]] && DRY=true

# --- 1. Compile PDF ---
echo "Compiling PDF..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
bibtex main > /dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true

if [[ ! -f main.pdf ]]; then
    echo "Error: main.pdf not generated" >&2
    exit 1
fi

# --- 2. Update docs/ via Python ---
python3 update_docs.py

# --- 3. Push docs/ to gh-pages branch ---
if $DRY; then
    echo "Dry run — not pushing."
    exit 0
fi

# Create a temporary worktree to build the gh-pages commit
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Copy docs content
cp -r docs/* "$TMPDIR/"

# Push to gh-pages using a detached commit (no worktree needed)
cd "$TMPDIR"
git init -q
git checkout -q -b gh-pages
git add -A
DATE=$(TZ=Etc/GMT+12 date +%Y-%m-%d)
git commit -q -m "Publish preprint ($DATE)"
git remote add origin https://github.com/ParallelScience/preprint.git
git push -f origin gh-pages

echo "Published to gh-pages. GitHub Pages will rebuild and Parallel ArXiv will re-scrape."
