#!/usr/bin/env python3
"""
Build script for integrating React frontend with Frappe PIM app
"""

import os
import shutil
import subprocess
import sys
import json
import re
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Exit code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)


def get_repo_paths():
    """Get the paths to frontend and backend repositories"""
    script_dir = Path(__file__).parent.absolute()
    
    # Assume we're in the imperium-pim repo
    backend_path = script_dir
    
    # Look for frontend repo in parent directory
    frontend_path = backend_path.parent / "imperium-pim-front-end"
    
    if not frontend_path.exists():
        print(f"Frontend repository not found at: {frontend_path}")
        print("Please ensure the imperium-pim-front-end repository is cloned alongside imperium-pim")
        sys.exit(1)
    
    return frontend_path, backend_path


def build_frontend(frontend_path):
    """Build the React frontend"""
    print("Building React frontend...")
    
    # Install dependencies if node_modules doesn't exist
    if not (frontend_path / "node_modules").exists():
        print("Installing frontend dependencies...")
        run_command("npm install", cwd=frontend_path)
    
    # Build the frontend
    run_command("npm run build:client", cwd=frontend_path)
    
    build_dir = frontend_path / "dist" / "spa"
    if not build_dir.exists():
        print(f"Build directory not found: {build_dir}")
        sys.exit(1)
    
    return build_dir


def copy_assets(build_dir, backend_path):
    """Copy built assets to Frappe public folder"""
    print("Copying assets to Frappe public folder...")
    
    # Create target directory
    target_dir = backend_path / "imperium_pim" / "public" / "pim-ui"
    
    # Remove existing assets
    if target_dir.exists():
        shutil.rmtree(target_dir)
    
    # Copy build output
    shutil.copytree(build_dir, target_dir)
    print(f"Assets copied to: {target_dir}")
    
    return target_dir


def update_page_script(target_dir, backend_path):
    """Update the Page script with correct asset paths"""
    print("Updating Page script with asset paths...")
    
    # Find the built assets
    assets_dir = target_dir / "assets"
    if not assets_dir.exists():
        print("Assets directory not found in build output")
        return
    
    # Find CSS and JS files
    css_files = list(assets_dir.glob("*.css"))
    js_files = list(assets_dir.glob("*.js"))
    
    if not css_files or not js_files:
        print("Warning: CSS or JS files not found in assets")
        return
    
    # Get the main CSS and JS files (usually index.*)
    main_css = next((f for f in css_files if f.name.startswith("index")), css_files[0])
    main_js = next((f for f in js_files if f.name.startswith("index")), js_files[0])
    
    # Update the Page JSON file
    page_json_path = backend_path / "imperium_pim" / "imperium_pim" / "page" / "pim_dashboard" / "pim_dashboard.json"
    
    if not page_json_path.exists():
        print(f"Page JSON not found: {page_json_path}")
        return
    
    # Read the page JSON
    with open(page_json_path, 'r') as f:
        content = f.read()
    
    # Update asset paths in the script
    css_path = f"/assets/imperium_pim/pim-ui/assets/{main_css.name}"
    js_path = f"/assets/imperium_pim/pim-ui/assets/{main_js.name}"
    
    # Replace the asset links in the loadPimAssets function
    content = re.sub(
        r"cssLink\.href = '/assets/imperium_pim/pim-ui/assets/[^']*\.css';",
        f"cssLink.href = '{css_path}';",
        content
    )
    
    content = re.sub(
        r"jsScript\.src = '/assets/imperium_pim/pim-ui/assets/[^']*\.js';",
        f"jsScript.src = '{js_path}';",
        content
    )
    
    # Write back the updated page JSON
    with open(page_json_path, 'w') as f:
        f.write(content)
    
    print(f"Updated Page script with:")
    print(f"  CSS: {css_path}")
    print(f"  JS: {js_path}")


def main():
    """Main build process"""
    print("🚀 Starting PIM Frontend Build Process")
    print("=" * 50)
    
    # Get repository paths
    frontend_path, backend_path = get_repo_paths()
    print(f"Frontend path: {frontend_path}")
    print(f"Backend path: {backend_path}")
    
    # Build the frontend
    build_dir = build_frontend(frontend_path)
    
    # Copy assets to Frappe
    target_dir = copy_assets(build_dir, backend_path)
    
    # Update Page script with asset paths
    update_page_script(target_dir, backend_path)
    
    print("=" * 50)
    print("✅ Frontend build completed successfully!")
    print(f"📁 Assets available at: {target_dir}")
    print("🌐 Access the PIM Dashboard at: /app/pim-dashboard")
    print("💡 Run 'bench restart' to reload the Frappe app")


if __name__ == "__main__":
    main()
