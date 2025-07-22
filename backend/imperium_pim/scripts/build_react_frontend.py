#!/usr/bin/env python3
"""
Script to build and deploy the React frontend for PIM Dashboard
"""

import os
import shutil
import subprocess
import frappe
from frappe import _

def build_and_deploy_react_frontend():
    """Build the React frontend and deploy it to the Frappe app"""
    
    print("Building and deploying React frontend for PIM Dashboard...")
    
    # Get paths
    app_path = frappe.get_app_path('imperium_pim')
    public_path = os.path.join(app_path, 'public')
    dashboard_path = os.path.join(public_path, 'pim-dashboard')
    
    # Frontend repo path (assuming it's cloned alongside the backend)
    frontend_repo_path = os.path.join(os.path.dirname(app_path), '..', 'imperium-pim-front-end')
    
    if not os.path.exists(frontend_repo_path):
        print(f"❌ Frontend repository not found at: {frontend_repo_path}")
        print("Please clone the imperium-pim-front-end repository first.")
        return False
    
    try:
        # Change to frontend directory
        os.chdir(frontend_repo_path)
        
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run(['npm', 'install'], check=True)
        
        # Build the React app
        print("🔨 Building React application...")
        subprocess.run(['npm', 'run', 'build'], check=True)
        
        # Create public directory if it doesn't exist
        os.makedirs(public_path, exist_ok=True)
        
        # Remove existing dashboard files
        if os.path.exists(dashboard_path):
            shutil.rmtree(dashboard_path)
        
        # Copy build files to Frappe app
        build_path = os.path.join(frontend_repo_path, 'dist')
        if os.path.exists(build_path):
            print("📁 Copying build files to Frappe app...")
            shutil.copytree(build_path, dashboard_path)
            print(f"✅ React frontend deployed to: {dashboard_path}")
            return True
        else:
            print("❌ Build directory not found. Build may have failed.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    build_and_deploy_react_frontend()
