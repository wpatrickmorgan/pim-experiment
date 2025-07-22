#!/bin/bash
# Main backend deployment script

set -e

DEPLOYMENT_TARGET=${1:-"production"}
SITE_NAME=${2:-"pim.local"}

echo "🎯 Deploying backend for separate deployment..."

# Navigate to backend directory
cd backend

# Run the backend deployment script
./scripts/deploy.sh $DEPLOYMENT_TARGET $SITE_NAME

echo "✅ Backend deployment completed!"

