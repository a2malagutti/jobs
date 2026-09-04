#!/usr/bin/env bash

set -e

# Verify git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Error: Not inside a Git repository."
  exit 1
fi

# Detect current branch
BRANCH=$(git branch --show-current)

if [ -z "$BRANCH" ]; then
  echo "Error: Unable to detect current branch (detached HEAD?)."
  exit 1
fi

# Set commit message (use first argument or prompt user)
COMMIT_MSG="$1"
if [ -z "$COMMIT_MSG" ]; then
  read -r -p "Enter commit message: " COMMIT_MSG
fi

if [ -z "$COMMIT_MSG" ]; then
  echo "Error: Commit message cannot be empty."
  exit 1
fi

echo "==> Staging all changes..."
git add -A

# Check if there are changes staged
if git diff --cached --quiet; then
  echo "No changes to commit. Working tree is clean."
  exit 0
fi

echo "==> Committing changes..."
git commit -m "$COMMIT_MSG"

echo "==> Pulling latest remote changes (rebase)..."
git pull --rebase origin "$BRANCH"

echo "==> Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo "Repository updated successfully."