#!/bin/bash
# Main frontend deployment script

set -e

DEPLOYMENT_TARGET=${1:-"production"}

echo "🎯 Deploying frontend for separate deployment..."

# Navigate to frontend directory
cd frontend

# Run the frontend deployment script
./scripts/deploy.sh $DEPLOYMENT_TARGET

echo "✅ Frontend deployment completed!"

