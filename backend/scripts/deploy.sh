#!/bin/bash
# Backend deployment script for separate deployment

set -e

# Configuration
DEPLOYMENT_TARGET=${1:-"production"}
SITE_NAME=${2:-"pim.local"}

echo "🚀 Deploying backend to $DEPLOYMENT_TARGET environment..."

case $DEPLOYMENT_TARGET in
    "production")
        echo "🌐 Deploying to production..."
        
        # Setup CORS for production
        echo "🔧 Configuring CORS..."
        if [ -n "$FRONTEND_URLS" ]; then
            python3 -c "
import sys
sys.path.append('.')
from imperium_pim.utils import setup_cors_for_site
setup_cors_for_site('$FRONTEND_URLS'.split(','))
"
        fi
        
        # Build and deploy with Docker
        if [ -f "Dockerfile" ]; then
            echo "🐳 Building and deploying with Docker..."
            docker build -t pim-backend:production .
            # Add your production Docker deployment commands here
            # docker push your-registry/pim-backend:production
            # kubectl apply -f k8s-manifests/
            echo "⚠️  Please configure production Docker deployment"
        else
            echo "⚠️  Please configure production deployment in this script"
        fi
        ;;
    
    "staging")
        echo "🧪 Deploying to staging..."
        # Add your staging deployment commands here
        echo "⚠️  Please configure staging deployment in this script"
        ;;
    
    "docker")
        echo "🐳 Starting with Docker Compose..."
        cd ..
        docker-compose -f docker-compose.separate.yml up -d backend
        echo "✅ Backend started with Docker!"
        echo "Backend available at: http://localhost:8000"
        ;;
    
    "local")
        echo "🏠 Starting local development server..."
        
        # Check if frappe-bench exists
        if [ ! -d "frappe-bench" ]; then
            echo "❌ frappe-bench not found. Please run setup first."
            exit 1
        fi
        
        cd frappe-bench
        
        # Setup CORS for local development
        echo "🔧 Setting up CORS for local development..."
        bench --site $SITE_NAME execute imperium_pim.utils.setup_cors_for_site --args "['http://localhost:3000']"
        
        # Start the server
        echo "🚀 Starting Frappe server..."
        bench start
        ;;
    
    *)
        echo "❌ Unknown deployment target: $DEPLOYMENT_TARGET"
        echo "Available targets: production, staging, docker, local"
        echo "Usage: $0 <target> [site_name]"
        exit 1
        ;;
esac

echo "🎉 Backend deployment complete!"

