import frappe
from frappe import _
import os
import glob
import json

def get_context(context):
    """Context for the PIM frontend page"""
    context.no_cache = 1
    context.show_sidebar = False
    
    # Add any context data needed for the frontend
    context.title = _("PIM Dashboard")
    context.description = _("Product Information Management System")
    
    # Get the React build assets dynamically
    context.react_assets = get_react_assets()
    
    return context

def get_react_assets():
    """Dynamically discover React build assets"""
    try:
        # Get the path to the public directory
        app_path = frappe.get_app_path("imperium_pim")
        public_path = os.path.join(app_path, "public", "_next", "static")
        
        assets = {
            "css": [],
            "js": {
                "webpack": [],
                "main": [],
                "main_app": [],
                "app_pages": [],
                "framework": []
            }
        }
        
        if not os.path.exists(public_path):
            frappe.log_error(f"Public path does not exist: {public_path}")
            return assets
            
        # Find CSS files
        css_pattern = os.path.join(public_path, "css", "*.css")
        for css_file in glob.glob(css_pattern):
            filename = os.path.basename(css_file)
            assets["css"].append(f"/assets/imperium_pim/_next/static/css/{filename}")
        
        # Find JavaScript chunks
        chunks_path = os.path.join(public_path, "chunks")
        if os.path.exists(chunks_path):
            # Webpack runtime
            webpack_pattern = os.path.join(chunks_path, "webpack-*.js")
            for js_file in glob.glob(webpack_pattern):
                filename = os.path.basename(js_file)
                assets["js"]["webpack"].append(f"/assets/imperium_pim/_next/static/chunks/{filename}")
            
            # Main chunks
            main_pattern = os.path.join(chunks_path, "main-*.js")
            for js_file in glob.glob(main_pattern):
                filename = os.path.basename(js_file)
                if "main-app-" in filename:
                    assets["js"]["main_app"].append(f"/assets/imperium_pim/_next/static/chunks/{filename}")
                else:
                    assets["js"]["main"].append(f"/assets/imperium_pim/_next/static/chunks/{filename}")
            
            # Framework chunks
            framework_pattern = os.path.join(chunks_path, "framework-*.js")
            for js_file in glob.glob(framework_pattern):
                filename = os.path.basename(js_file)
                assets["js"]["framework"].append(f"/assets/imperium_pim/_next/static/chunks/{filename}")
            
            # App pages
            app_chunks_path = os.path.join(chunks_path, "app")
            if os.path.exists(app_chunks_path):
                app_pattern = os.path.join(app_chunks_path, "*.js")
                for js_file in glob.glob(app_pattern):
                    filename = os.path.basename(js_file)
                    assets["js"]["app_pages"].append(f"/assets/imperium_pim/_next/static/chunks/app/{filename}")
        
        return assets
        
    except Exception as e:
        frappe.log_error(f"Error getting React assets: {str(e)}")
        return {
            "css": [],
            "js": {
                "webpack": [],
                "main": [],
                "main_app": [],
                "app_pages": [],
                "framework": []
            }
        }

@frappe.whitelist(allow_guest=True)
def get_assets_json():
    """API endpoint to get assets as JSON"""
    return get_react_assets()
