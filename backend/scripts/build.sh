#!/bin/bash
# Backend preparation script for standard Frappe site deployment

set -e

echo "🏗️  Preparing backend for Frappe site deployment..."

# Check if we're in the backend directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the backend directory."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "🐍 Python version: $python_version"

# Validate imperium_pim app structure
echo "🔍 Validating app structure..."
if [ -f "verify_pim_structure.py" ]; then
    python3 verify_pim_structure.py
else
    echo "⚠️  Structure validation script not found, skipping..."
fi

# Validate required files for Frappe app
echo "🔍 Checking required Frappe app files..."
required_files=("setup.py" "imperium_pim/hooks.py" "imperium_pim/__init__.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "❌ $file missing - required for Frappe app"
        exit 1
    fi
done

echo "✅ Backend preparation completed successfully!"
echo ""
echo "Next steps for Frappe site deployment:"
echo "1. Copy this app to your Frappe bench: bench get-app imperium_pim /path/to/this/directory"
echo "2. Install on your site: bench --site your-site install-app imperium_pim"
echo "3. Configure CORS for your Vercel frontend domain"
echo "4. Run: bench --site your-site migrate"
