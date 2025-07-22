#!/bin/bash
# Frontend deployment script for Vercel

set -e

# Configuration
DEPLOYMENT_TARGET=${1:-"vercel"}
BUILD_DIR="out"

echo "🚀 Deploying frontend to $DEPLOYMENT_TARGET..."

# Check if build exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Build directory not found. Running build first..."
    ./scripts/build.sh
fi

case $DEPLOYMENT_TARGET in
    "vercel")
        echo "🌐 Deploying to Vercel..."
        if command -v vercel &> /dev/null; then
            vercel --prod
            echo "✅ Deployed to Vercel!"
        else
            echo "⚠️  Vercel CLI not found. Install with: npm i -g vercel"
            echo "Or deploy via GitHub integration in Vercel dashboard"
        fi
        ;;
    
    "preview")
        echo "🧪 Deploying preview to Vercel..."
        if command -v vercel &> /dev/null; then
            vercel
            echo "✅ Preview deployed to Vercel!"
        else
            echo "⚠️  Vercel CLI not found. Install with: npm i -g vercel"
        fi
        ;;
    
    "local")
        echo "🏠 Starting local server..."
        cd $BUILD_DIR
        npx serve . -p 3000
        ;;
    
    *)
        echo "❌ Unknown deployment target: $DEPLOYMENT_TARGET"
        echo "Available targets: vercel, preview, local"
        echo "Usage: $0 <target>"
        exit 1
        ;;
esac

echo "🎉 Frontend deployment complete!"
