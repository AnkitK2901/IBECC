#!/bin/bash

# === CONFIGURE ===
GCE_USER="ankit_anjul"
GCE_HOST="34.93.194.88"
# This is the path to the master deploy script ON THE SERVER
SERVER_SCRIPT_PATH="/home/ankit_anjul/IBECC/scripts/deploy.sh"
COMMIT_MESSAGE="Update"

echo "➡️  STEP 1: Committing and pushing local changes..."
# Add all changed files
git add .

# Commit with a generic message
git commit -m "$COMMIT_MESSAGE"

# Push to the main branch on GitHub
git push origin main || { echo "❌ Git push failed!"; exit 1; }

echo "✅ Local changes pushed successfully."
echo "----------------------------------------"
echo "🚀 STEP 2: Running deployment script on GCE..."

# Connect to the server and run the single deployment script
ssh $GCE_USER@$GCE_HOST "bash $SERVER_SCRIPT_PATH"

echo "✨ Deployment script finished."