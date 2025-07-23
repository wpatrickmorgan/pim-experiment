#!/usr/bin/env python3
"""
CORS Configuration Script for Imperium PIM

This script configures CORS settings for the Frappe backend to allow
communication with the frontend deployed on Vercel.

Usage:
    python setup_cors.py [frontend_url]

If no frontend_url is provided, it will configure for common development
and production URLs.
"""

import json
import os
import sys
from pathlib import Path

def setup_cors_config(frontend_url=None):
    """
    Setup CORS configuration for Frappe site
    
    Args:
        frontend_url (str): The frontend URL to allow (optional)
    """
    
    # Default frontend URLs if none provided
    if not frontend_url:
        frontend_urls = [
            "http://localhost:3000",  # Local development
            "https://pim-experiment.vercel.app",  # Vercel deployment
            "https://pim-experiment-git-*.vercel.app",  # Vercel preview deployments
        ]
    else:
        frontend_urls = [frontend_url]
    
    # CORS configuration
    cors_config = {
        "allow_cors": "*",
        "cors_origins": frontend_urls,
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
        "session_cookie_samesite": "None",
        "session_cookie_secure": True,
        "csrf_cookie_samesite": "None",
        "csrf_cookie_secure": True
    }
    
    print("🔧 Setting up CORS configuration...")
    print(f"📍 Allowed origins: {frontend_urls}")
    
    # Try to find site_config.json in common locations
    possible_paths = [
        "site_config.json",
        "../site_config.json", 
        "../../site_config.json",
        "/home/frappe/frappe-bench/sites/site1.local/site_config.json",
        "/home/frappe/frappe-bench/sites/localhost/site_config.json"
    ]
    
    site_config_path = None
    existing_config = {}
    
    # Try to find existing site_config.json
    for path in possible_paths:
        if os.path.exists(path):
            site_config_path = path
            try:
                with open(path, 'r') as f:
                    existing_config = json.load(f)
                print(f"✅ Found existing site_config.json at: {path}")
                break
            except Exception as e:
                print(f"⚠️  Could not read {path}: {e}")
                continue
    
    # If no site_config.json found, create one
    if not site_config_path:
        site_config_path = "site_config.json"
        print(f"📝 Creating new site_config.json at: {site_config_path}")
    
    # Merge with existing configuration
    existing_config.update(cors_config)
    
    # Write the configuration
    try:
        with open(site_config_path, 'w') as f:
            json.dump(existing_config, f, indent=2)
        
        print(f"✅ CORS configuration written to: {site_config_path}")
        print("\n📋 Configuration details:")
        for key, value in cors_config.items():
            print(f"   {key}: {value}")
        
        print("\n🚀 Next steps:")
        print("1. Restart your Frappe server:")
        print("   bench restart")
        print("\n2. Or if using systemd:")
        print("   sudo systemctl restart frappe-web")
        print("   sudo systemctl restart frappe-worker")
        print("\n3. Test the connection from your frontend")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        return False

def main():
    """Main function"""
    frontend_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🌐 Imperium PIM CORS Configuration Setup")
    print("=" * 50)
    
    success = setup_cors_config(frontend_url)
    
    if success:
        print("\n✅ CORS configuration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ CORS configuration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
