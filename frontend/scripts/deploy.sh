#!/bin/bash
# Frontend deployment script for separate deployment

set -e

# Configuration
DEPLOYMENT_TARGET=${1:-"production"}
BUILD_DIR="out"

echo "🚀 Deploying frontend to $DEPLOYMENT_TARGET environment..."

# Check if build exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Build directory not found. Running build first..."
    ./scripts/build.sh
fi

case $DEPLOYMENT_TARGET in
    "production")
        echo "🌐 Deploying to production..."
        # Add your production deployment commands here
        # Examples:
        # aws s3 sync out/ s3://your-bucket-name --delete
        # rsync -avz --delete out/ user@server:/var/www/html/
        # docker build -t frontend:latest .
        echo "⚠️  Please configure production deployment in this script"
        ;;
    
    "staging")
        echo "🧪 Deploying to staging..."
        # Add your staging deployment commands here
        echo "⚠️  Please configure staging deployment in this script"
        ;;
    
    "docker")
        echo "🐳 Building Docker image..."
        docker build -t pim-frontend:latest .
        echo "✅ Docker image built successfully!"
        echo "Run with: docker run -p 3000:3000 pim-frontend:latest"
        ;;
    
    "local")
        echo "🏠 Starting local server..."
        cd $BUILD_DIR
        npx serve . -p 3000
        ;;
    
    *)
        echo "❌ Unknown deployment target: $DEPLOYMENT_TARGET"
        echo "Available targets: production, staging, docker, local"
        exit 1
        ;;
esac

echo "🎉 Frontend deployment complete!"

