import frappe
from frappe import _
import os
import glob

def get_context(context):
    """Serve React frontend for PIM Dashboard"""
    
    # Check if user has permission to access PIM module
    if not frappe.has_permission("PIM Item", "read"):
        frappe.throw(_("You don't have permission to access PIM Dashboard"), frappe.PermissionError)
    
    context.no_cache = 1
    context.show_sidebar = False  # React app will handle its own layout
    
    # Set up configuration for React frontend
    context.pim_config = {
        'user': frappe.session.user,
        'csrfToken': frappe.sessions.get_csrf_token(),
        'apiBase': '/api/method/imperium_pim.api',
        'basePath': '/pim-dashboard'
    }
    
    # Check if React build files exist, otherwise show development message
    app_path = frappe.get_app_path('imperium_pim')
    react_build_path = os.path.join(app_path, 'public', 'pim-dashboard')
    
    if not os.path.exists(react_build_path) or not os.path.exists(os.path.join(react_build_path, 'index.html')):
        context.show_dev_message = True
        context.react_build_path = react_build_path
    else:
        context.show_dev_message = False
        
        # Find built JS and CSS files
        assets_path = os.path.join(react_build_path, 'assets')
        base_url = '/assets/imperium_pim/pim-dashboard'
        
        context.js_files = []
        context.css_files = []
        
        if os.path.exists(assets_path):
            # Find JS files
            js_files = glob.glob(os.path.join(assets_path, '*.js'))
            for js_file in js_files:
                filename = os.path.basename(js_file)
                context.js_files.append(f"{base_url}/assets/{filename}")
            
            # Find CSS files
            css_files = glob.glob(os.path.join(assets_path, '*.css'))
            for css_file in css_files:
                filename = os.path.basename(css_file)
                context.css_files.append(f"{base_url}/assets/{filename}")
    
    return context
