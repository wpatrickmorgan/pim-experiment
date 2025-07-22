#!/bin/bash
# Backend configuration script for Frappe site deployment

set -e

# Configuration
SITE_NAME=${1:-"your-site"}
FRONTEND_URL=${2:-"https://your-vercel-app.vercel.app"}

echo "🚀 Configuring backend for Frappe site deployment..."

# Check if we're in a Frappe bench environment
if [ ! -f "../sites/common_site_config.json" ] && [ ! -d "../sites" ]; then
    echo "⚠️  This script should be run from within a Frappe bench environment"
    echo "Please run this from: /path/to/frappe-bench/apps/imperium_pim/backend/scripts/"
fi

echo "🔧 Setting up CORS for Vercel frontend..."

# Create CORS setup command
cat > setup_cors.py << EOF
import frappe
import json
from frappe.utils import get_site_config

def setup_cors():
    site_config = get_site_config()
    
    # CORS settings for Vercel frontend
    cors_settings = {
        "allow_cors": "*",
        "cors_headers": [
            "Authorization",
            "Content-Type", 
            "X-Requested-With",
            "Accept",
            "Origin",
            "Cache-Control",
            "X-Frappe-CSRF-Token",
            "X-Frappe-CMD"
        ],
        "allow_cors_credentials": True,
        "cors_origins": ["$FRONTEND_URL", "http://localhost:3000"],
        "session_cookie_samesite": "None",
        "session_cookie_secure": True,
        "csrf_cookie_samesite": "None", 
        "csrf_cookie_secure": True
    }
    
    site_config.update(cors_settings)
    
    site_config_path = frappe.get_site_path("site_config.json")
    with open(site_config_path, 'w') as f:
        json.dump(site_config, f, indent=2)
    
    print(f"CORS configured for frontend: $FRONTEND_URL")

setup_cors()
EOF

# Run CORS setup if in bench environment
if command -v bench &> /dev/null; then
    echo "📝 Running CORS configuration..."
    bench --site $SITE_NAME execute setup_cors.py
    rm setup_cors.py
    
    echo "🔄 Running migrations..."
    bench --site $SITE_NAME migrate
    
    echo "🧹 Clearing cache..."
    bench --site $SITE_NAME clear-cache
    
    echo "✅ Backend configuration complete!"
    echo ""
    echo "Your Frappe site is now configured for Vercel frontend at: $FRONTEND_URL"
else
    echo "⚠️  Bench command not found. Please run manually:"
    echo "1. bench --site $SITE_NAME execute setup_cors.py"
    echo "2. bench --site $SITE_NAME migrate"
    echo "3. bench --site $SITE_NAME clear-cache"
fi

echo "🎉 Backend configuration complete!"
