#!/bin/bash
# Frontend build script for separate deployment

set -e

echo "🏗️  Building frontend for separate deployment..."

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
echo "Next steps:"
echo "1. Deploy the 'out' directory to your static hosting service"
echo "2. Ensure your backend API URL is correctly configured"
echo "3. Test the deployment with: npm run start"

