"""
CORS Configuration for Separate Frontend Deployment
This module provides utilities to configure CORS settings for Frappe
when the frontend is deployed separately from the backend.
"""

import frappe
import json
import os
from frappe.utils import get_site_config


def setup_cors_for_separate_deployment(frontend_urls=None):
    """
    Configure CORS settings for separate frontend deployment
    
    Args:
        frontend_urls (list): List of frontend URLs that should be allowed
    """
    if not frontend_urls:
        frontend_urls = [
            "http://localhost:3000",  # Development
            "https://your-frontend-domain.com",  # Production
        ]
    
    site_config = get_site_config()
    
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
    
    print(f"CORS configuration updated for frontend URLs: {frontend_urls}")
    return cors_settings


def get_cors_headers():
    """
    Get CORS headers for API responses
    """
    site_config = get_site_config()
    cors_origins = site_config.get("cors_origins", ["*"])
    
    headers = {
        "Access-Control-Allow-Origin": "*",  # Will be overridden by specific origin
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": ", ".join(site_config.get("cors_headers", [])),
        "Access-Control-Allow-Credentials": "true"
    }
    
    return headers


def add_cors_headers_to_response(response, origin=None):
    """
    Add CORS headers to a response object
    
    Args:
        response: Frappe response object
        origin: Origin of the request
    """
    headers = get_cors_headers()
    
    # Set specific origin if provided and allowed
    site_config = get_site_config()
    allowed_origins = site_config.get("cors_origins", ["*"])
    
    if origin and (origin in allowed_origins or "*" in allowed_origins):
        headers["Access-Control-Allow-Origin"] = origin
    
    for key, value in headers.items():
        response.headers[key] = value
    
    return response


# CLI command to setup CORS
def setup_cors_command():
    """
    Frappe command to setup CORS for separate deployment
    Usage: bench execute backend.cors_config.setup_cors_command
    """
    frontend_urls = os.getenv("FRONTEND_URLS", "").split(",")
    if not frontend_urls or frontend_urls == [""]:
        frontend_urls = [
            "http://localhost:3000",
            "https://your-frontend-domain.com"
        ]
    
    setup_cors_for_separate_deployment(frontend_urls)
    frappe.db.commit()
    print("CORS setup completed successfully!")


if __name__ == "__main__":
    setup_cors_command()

