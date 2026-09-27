#!/usr/bin/env bash
# Deploy static portfolio directly to GitHub Pages (gh-pages branch)
set -e

echo "=== 1. Building static portfolio ==="
python3 export_static.py

echo "=== 2. Creating atomic gh-pages commit ==="
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_FILE="$ROOT_DIR/.git/gh_pages_index"

rm -f "$INDEX_FILE"
GIT_INDEX_FILE="$INDEX_FILE" GIT_WORK_TREE="$ROOT_DIR/dist" git add -A
TREE_ID=$(GIT_INDEX_FILE="$INDEX_FILE" git write-tree)
COMMIT_ID=$(git commit-tree "$TREE_ID" -m "deploy: publish portfolio to GitHub Pages $(date -u '+%Y-%m-%d %H:%M:%S UTC')")
rm -f "$INDEX_FILE"

echo "Created commit $COMMIT_ID"
echo "=== 3. Pushing to origin gh-pages branch ==="
git push -f origin "$COMMIT_ID":refs/heads/gh-pages

echo "=== PUBLISHED SUCCESSFULLY! ==="
echo "Live URL: https://makportx.github.io/portfolio/"
