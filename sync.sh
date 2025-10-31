#!/bin/bash

set -e

echo "Starting sync..."

git add WALL.md
git commit -m "wall update"
git push

echo "Waiting for GitHub Actions workflow to complete..."
sleep 10
run_id=$(gh run list --branch main --limit 1 --json databaseId -q '.[0].databaseId')
gh run watch $run_id
sleep 5

echo "Pulling latest changes..."
git pull

echo "Sync completed."
