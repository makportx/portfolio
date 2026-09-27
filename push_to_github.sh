#!/bin/bash
# Push portfolio to GitHub

cd "$(dirname "$0")"

echo "Checking remote connection..."
if git push -u origin main; then
    echo " Successfully pushed to https://github.com/makportx/portfolio"
else
    echo "Push failed. Trying with force..."
    git push -u origin main --force
fi
