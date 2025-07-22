#!/bin/bash
# Frontend build script for Vercel deployment

set -e

echo "🏗️  Building frontend for Vercel deployment..."

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm ci

# Run type checking
echo "🔍 Running type check..."
npm run type-check

# Run linting
echo "🧹 Running linter..."
npm run lint

# Build the application
echo "🔨 Building application..."
npm run build

# Verify build output
if [ -d "out" ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Static files generated in 'out' directory"
    echo "📊 Build size:"
    du -sh out/
else
    echo "❌ Build failed - no output directory found"
    exit 1
fi

echo "🎉 Frontend build complete!"
echo ""
echo "Next steps for Vercel deployment:"
echo "1. Connect your GitHub repo to Vercel"
echo "2. Set environment variables in Vercel dashboard"
echo "3. Deploy automatically on push to main branch"
