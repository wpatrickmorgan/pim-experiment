#!/usr/bin/env python3
"""
Script to update CORS configuration for Frappe site
Run this on your server to fix CORS issues with Vercel frontend
"""

import json
import os
import sys

def update_site_cors_config(site_name, frontend_url="https://pim-experiment.vercel.app"):
    """
    Update the site_config.json file with proper CORS settings
    """
    
    # Path to site config
    site_config_path = f"/home/frappe/frappe-bench/sites/{site_name}/site_config.json"
    
    # Check if file exists
    if not os.path.exists(site_config_path):
        print(f"❌ Site config file not found: {site_config_path}")
        print("Please check your site name and frappe-bench path")
        return False
    
    try:
        # Read existing config
        with open(site_config_path, 'r') as f:
            config = json.load(f)
        
        print(f"📖 Current config: {json.dumps(config, indent=2)}")
        
        # Update CORS settings
        cors_settings = {
            "allow_cors": "*",
            "cors_origins": [
                frontend_url,
                "https://pim-experiment-git-main.vercel.app",
                "http://localhost:3000"
            ],
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
        
        # Merge with existing config
        config.update(cors_settings)
        
        # Write back to file
        with open(site_config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ CORS configuration updated successfully!")
        print(f"📝 Updated config: {json.dumps(config, indent=2)}")
        print(f"🔄 Please restart your Frappe server: bench restart")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating CORS config: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_cors.py <site_name> [frontend_url]")
        print("Example: python3 update_cors.py site1.local https://pim-experiment.vercel.app")
        sys.exit(1)
    
    site_name = sys.argv[1]
    frontend_url = sys.argv[2] if len(sys.argv) > 2 else "https://pim-experiment.vercel.app"
    
    print(f"🔧 Updating CORS configuration for site: {site_name}")
    print(f"🌐 Frontend URL: {frontend_url}")
    
    success = update_site_cors_config(site_name, frontend_url)
    
    if success:
        print("\n🎉 CORS configuration updated successfully!")
        print("Next steps:")
        print("1. Run: bench restart")
        print("2. Test your frontend API calls")
        print("3. Check browser console for any remaining CORS errors")
    else:
        print("\n❌ Failed to update CORS configuration")
        print("Please check the error messages above and try again")

if __name__ == "__main__":
    main()
