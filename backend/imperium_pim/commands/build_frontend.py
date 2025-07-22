import frappe
import os
import subprocess
import shutil
from frappe import _

def execute():
    """Build the React frontend for PIM Dashboard"""
    
    app_path = frappe.get_app_path('imperium_pim')
    frontend_path = os.path.join(app_path, 'frontend')
    build_output_path = os.path.join(app_path, 'public', 'pim-dashboard')
    
    if not os.path.exists(frontend_path):
        frappe.throw(_("Frontend source code not found at {0}").format(frontend_path))
    
    try:
        # Change to frontend directory
        os.chdir(frontend_path)
        
        # Check if node_modules exists, if not install dependencies
        if not os.path.exists('node_modules'):
            print("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Build the frontend
        print("Building React frontend...")
        subprocess.run(['npm', 'run', 'build'], check=True)
        
        # Verify build output exists
        if not os.path.exists(build_output_path):
            frappe.throw(_("Build failed - output directory not found"))
        
        print(f"✅ Frontend built successfully!")
        print(f"📁 Build output: {build_output_path}")
        
        # List built files for verification
        if os.path.exists(os.path.join(build_output_path, 'assets')):
            assets = os.listdir(os.path.join(build_output_path, 'assets'))
            print(f"📦 Built assets: {', '.join(assets)}")
        
        return {
            'success': True,
            'message': 'Frontend built successfully',
            'build_path': build_output_path
        }
        
    except subprocess.CalledProcessError as e:
        frappe.throw(_("Build failed with error: {0}").format(str(e)))
    except Exception as e:
        frappe.throw(_("Unexpected error during build: {0}").format(str(e)))

def cleanup():
    """Clean up build artifacts"""
    app_path = frappe.get_app_path('imperium_pim')
    build_output_path = os.path.join(app_path, 'public', 'pim-dashboard')
    
    if os.path.exists(build_output_path):
        shutil.rmtree(build_output_path)
        print("🧹 Cleaned up build artifacts")
    
    return {'success': True, 'message': 'Build artifacts cleaned up'}

