#!/bin/bash
# Backend build script for separate deployment

set -e

echo "🏗️  Building backend for separate deployment..."

# Check if we're in the backend directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the backend directory."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "🐍 Python version: $python_version"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Validate imperium_pim app structure
echo "🔍 Validating app structure..."
if [ -f "verify_pim_structure.py" ]; then
    python3 verify_pim_structure.py
else
    echo "⚠️  Structure validation script not found, skipping..."
fi

# Build Docker image if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "🐳 Building Docker image..."
    docker build -t pim-backend:latest .
    echo "✅ Docker image built successfully!"
else
    echo "⚠️  No Dockerfile found, skipping Docker build"
fi

# Check if frappe-bench exists for local development
if [ -d "frappe-bench" ]; then
    echo "🔧 Setting up Frappe bench..."
    cd frappe-bench
    
    # Install imperium_pim app if not already installed
    if [ ! -d "apps/imperium_pim" ]; then
        echo "📱 Installing imperium_pim app..."
        bench get-app imperium_pim ../
    fi
    
    # Run migrations
    echo "🔄 Running migrations..."
    bench --site all migrate
    
    # Clear cache
    echo "🧹 Clearing cache..."
    bench --site all clear-cache
    
    cd ..
fi

echo "✅ Backend build completed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure your database connection"
echo "2. Set up CORS for your frontend domain"
echo "3. Deploy using Docker or traditional hosting"

