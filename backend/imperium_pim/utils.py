"""
Utility functions for Imperium PIM

INSTALLATION INSTRUCTIONS:
=========================

After installing or updating this app, run the following commands to ensure
the module appears correctly in the Desk UI:

1. Run migration:
   bench --site [site-name] migrate

2. Clear cache:
   bench --site [site-name] clear-cache

3. Restart bench:
   bench restart

4. Optional - manually sync desktop icons:
   bench --site [site-name] console
   >>> from imperium_pim.utils import sync_desktop_icons
   >>> sync_desktop_icons()

The "Imperium PIM" module should now appear in the left-hand Desk UI menu
with all 8 custom Doctypes organized in categories.

TROUBLESHOOTING:
===============

If the module still doesn't appear:
1. Check that all Doctypes have module = "Imperium PIM"
2. Verify hooks.py includes app_include_desktop line
3. Ensure desktop.py exists and returns correct module data
4. Run: bench --site [site-name] rebuild-global-search
5. Try logging out and back in to refresh the UI
"""

import frappe
import json


def sync_desktop_icons():
    """
    Sync desktop icons for Imperium PIM module
    This ensures the module appears correctly in the Desk UI
    """
    try:
        from frappe.desk.doctype.desktop_icon.desktop_icon import sync_desktop_icons
        sync_desktop_icons()
        frappe.msgprint("Desktop icons synced successfully for Imperium PIM")
    except Exception as e:
        frappe.log_error(f"Error syncing desktop icons: {str(e)}")
        frappe.throw(f"Failed to sync desktop icons: {str(e)}")


def setup_module():
    """
    Setup function to ensure proper module configuration
    This can be called after installation or migration
    """
    # Sync desktop icons
    sync_desktop_icons()
    
    # Clear cache to ensure changes take effect
    frappe.clear_cache()
    
    frappe.msgprint("Imperium PIM module setup completed successfully")


def handle_cors_preflight():
    """
    Handle CORS preflight requests for separate frontend deployment
    This function is called before each request via hooks.py
    """
    if frappe.request.method == "OPTIONS":
        # Get site configuration
        site_config = frappe.get_site_config()
        
        # Get origin from request
        origin = frappe.get_request_header("Origin")
        
        # Check if origin is allowed
        allowed_origins = site_config.get("cors_origins", ["*"])
        
        if origin and (origin in allowed_origins or "*" in allowed_origins):
            # Set CORS headers for preflight
            frappe.response.headers.update({
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": ", ".join(site_config.get("cors_headers", [
                    "Authorization", "Content-Type", "X-Requested-With", 
                    "Accept", "Origin", "Cache-Control", "X-Frappe-CSRF-Token"
                ])),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400"
            })
            
            # Return empty response for preflight
            frappe.response.http_status_code = 204
            return


def add_cors_headers():
    """
    Add CORS headers to all responses for separate frontend deployment
    This function is called after each request via hooks.py
    """
    # Get site configuration
    site_config = frappe.get_site_config()
    
    # Get origin from request
    origin = frappe.get_request_header("Origin")
    
    # Check if CORS is enabled
    if site_config.get("allow_cors"):
        allowed_origins = site_config.get("cors_origins", ["*"])
        
        # Set CORS headers
        cors_headers = {
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": ", ".join(site_config.get("cors_headers", [
                "Authorization", "Content-Type", "X-Requested-With", 
                "Accept", "Origin", "Cache-Control", "X-Frappe-CSRF-Token"
            ])),
            "Access-Control-Allow-Credentials": "true"
        }
        
        # Set specific origin if allowed
        if origin and (origin in allowed_origins or "*" in allowed_origins):
            cors_headers["Access-Control-Allow-Origin"] = origin
        elif "*" in allowed_origins:
            cors_headers["Access-Control-Allow-Origin"] = "*"
        
        # Update response headers
        frappe.response.headers.update(cors_headers)


def setup_cors_for_site(frontend_urls=None):
    """
    Setup CORS configuration for the current site
    
    Args:
        frontend_urls (list): List of frontend URLs to allow
    """
    if not frontend_urls:
        frontend_urls = [
            "http://localhost:3000",  # Development
            "https://your-frontend-domain.com",  # Production
        ]
    
    site_config = frappe.get_site_config()
    
    # Update CORS settings
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
        "cors_origins": frontend_urls,
        "session_cookie_samesite": "None",
        "session_cookie_secure": True,
        "csrf_cookie_samesite": "None", 
        "csrf_cookie_secure": True
    }
    
    # Update site config
    site_config.update(cors_settings)
    
    # Write back to site_config.json
    site_config_path = frappe.get_site_path("site_config.json")
    with open(site_config_path, 'w') as f:
        json.dump(site_config, f, indent=2)
    
    frappe.msgprint(f"CORS configuration updated for frontend URLs: {frontend_urls}")
    return cors_settings
