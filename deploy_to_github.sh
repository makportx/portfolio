#!/usr/bin/env bash
# Deploy static portfolio directly to GitHub Pages (gh-pages branch)
set -e

echo "=== 1. Building static portfolio ==="
python3 export_static.py

echo "=== 2. Preparing gh-pages branch deployment ==="
# Stash any uncommitted work if present
git stash push -m "deploy-temp-stash" || true

# Switch to orphan branch
git checkout --orphan gh-pages-deploy
git reset

# Add exported files
git --work-tree=dist add -A
TREE_ID=$(git --work-tree=dist write-tree)
COMMIT_ID=$(git commit-tree "$TREE_ID" -m "deploy: publish portfolio to GitHub Pages")

echo "=== 3. Pushing to origin gh-pages ==="
git push -f origin "$COMMIT_ID":refs/heads/gh-pages

echo "=== 4. Restoring main branch ==="
git checkout main
git branch -D gh-pages-deploy 2>/dev/null || true
git stash pop 2>/dev/null || true

echo "=== PUBLISHED SUCCESSFULLY! ==="
echo "Live URL: https://makportx.github.io/portfolio/"
