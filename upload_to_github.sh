#!/bin/bash

# GitHub Upload Script for SMTP Tester
# Run this script after creating the repository on GitHub

echo "🚀 Uploading SMTP Tester to GitHub..."
echo "=================================================="

# Initialize git repository
echo "📋 Initializing Git repository..."
git init

# Add all files
echo "📁 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Gmail IMAP Credentials Checker

Features:
- Dual authentication (App Password + OAuth2)
- Google Colab optimization
- Bulk credential processing
- Real-time progress tracking
- Export functionality (CSV/summary)
- Enhanced debugging system
- Modular architecture (16 modules, <150 LoC each)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Add remote origin (replace YOUR_USERNAME with your GitHub username)
echo "🔗 Adding remote origin..."
echo "⚠️  REPLACE 'YOUR_USERNAME' with your actual GitHub username!"
git remote add origin https://github.com/YOUR_USERNAME/SMTP-Tester.git

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "=================================================="
echo "✅ Upload complete!"
echo "🔗 Repository URL: https://github.com/YOUR_USERNAME/SMTP-Tester"
echo "📓 Colab Notebook: https://github.com/YOUR_USERNAME/SMTP-Tester/blob/main/colab_deployment.ipynb"