#!/bin/bash

# NEVERDIE HQ - Global Launchpad
# This script handles the final push to GitHub.

echo "🚀 NEVERDIE HQ - Starting Global Launch Protocol..."

# 1. Initialize Git if not already done
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: NEVERDIE HQ - Super Premium Version"
fi

# 2. Check for GitHub username
read -p "Enter your GitHub username: " GH_USER

# 3. Create Repo logic (requires manual or gh CLI)
echo "--------------------------------------------------"
echo "STEP: Please ensure you have created a repository named 'rainmanneverdie' on GitHub."
echo "URL: https://github.com/new"
echo "--------------------------------------------------"
read -p "Press Enter once the repository is created..."

# 4. Add Remote and Push
git remote add origin https://github.com/$GH_USER/rainmanneverdie.git
git branch -M main
git push -u origin main

echo "✅ DEPLOYMENT COMPLETE!"
echo "Your site will be live at: https://$GH_USER.github.io/rainmanneverdie/"
echo "Note: It may take 1-2 minutes for the first build to complete."
