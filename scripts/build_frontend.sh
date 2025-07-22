#!/bin/bash

# Build Frontend Script
# Builds the Next.js frontend and deploys to nginx directory

set -e

echo "🔨 Building Next.js Frontend..."
echo "================================"

cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the application
echo "🏗️ Building application..."
npm run build

# Export static files if available
if npm run export 2>/dev/null; then
    echo "📤 Exporting static files..."
    
    # Create/update web directory
    sudo mkdir -p /var/www/client-a-frontend
    sudo rm -rf /var/www/client-a-frontend/*
    sudo cp -r out/* /var/www/client-a-frontend/
    sudo chown -R www-data:www-data /var/www/client-a-frontend
    
    echo "✅ Static files deployed to /var/www/client-a-frontend"
else
    echo "⚠️ Static export not available, copying build files..."
    
    # Create/update web directory with build files
    sudo mkdir -p /var/www/client-a-frontend
    sudo rm -rf /var/www/client-a-frontend/*
    
    # Copy public files
    if [ -d "public" ]; then
        sudo cp -r public/* /var/www/client-a-frontend/
    fi
    
    # Copy Next.js static files
    if [ -d ".next/static" ]; then
        sudo mkdir -p /var/www/client-a-frontend/_next
        sudo cp -r .next/static /var/www/client-a-frontend/_next/
    fi
    
    sudo chown -R www-data:www-data /var/www/client-a-frontend
    
    echo "✅ Build files deployed to /var/www/client-a-frontend"
fi

# Reload nginx to pick up any changes
echo "🔄 Reloading nginx..."
sudo nginx -s reload

echo ""
echo "🎉 Frontend build completed!"
echo "Visit: http://client-a.localtest.me"

cd ..

