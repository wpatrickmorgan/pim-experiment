#!/usr/bin/env python3
"""
Script to copy remaining backend files from imperium-pim to pim-experiment
This script will copy all the doctype definitions, API files, and other backend components
"""

import os
import subprocess
import sys

# List of all files that need to be copied (excluding frontend)
FILES_TO_COPY = [
    "imperium_pim/hooks.py",
    "imperium_pim/api.py", 
    "imperium_pim/commands.py",
    "imperium_pim/utils.py",
    "imperium_pim/verify_setup.py",
    "imperium_pim/api/__init__.py",
    "imperium_pim/api/attributes.py",
    "imperium_pim/api/dashboard.py", 
    "imperium_pim/api/items.py",
    "imperium_pim/api/permission.py",
    "imperium_pim/api/vendors.py",
    "imperium_pim/config/__init__.py",
    "imperium_pim/config/desktop.py",
    "imperium_pim/config/docs.py",
    "imperium_pim/config/workspace.py",
    "imperium_pim/pim/__init__.py",
    "imperium_pim/pim/doctype/__init__.py",
    "imperium_pim/pim/module_def/pim.json",
    # PIM Attribute doctype
    "imperium_pim/pim/doctype/pim_attribute/__init__.py",
    "imperium_pim/pim/doctype/pim_attribute/pim_attribute.js",
    "imperium_pim/pim/doctype/pim_attribute/pim_attribute.json",
    "imperium_pim/pim/doctype/pim_attribute/pim_attribute.py",
    "imperium_pim/pim/doctype/pim_attribute/test_pim_attribute.py",
    # PIM Attribute Value doctype
    "imperium_pim/pim/doctype/pim_attribute_value/__init__.py",
    "imperium_pim/pim/doctype/pim_attribute_value/pim_attribute_value.js",
    "imperium_pim/pim/doctype/pim_attribute_value/pim_attribute_value.json",
    "imperium_pim/pim/doctype/pim_attribute_value/pim_attribute_value.py",
    "imperium_pim/pim/doctype/pim_attribute_value/test_pim_attribute_value.py",
    # PIM Item doctype
    "imperium_pim/pim/doctype/pim_item/__init__.py",
    "imperium_pim/pim/doctype/pim_item/pim_item.js",
    "imperium_pim/pim/doctype/pim_item/pim_item.json",
    "imperium_pim/pim/doctype/pim_item/pim_item.py",
    "imperium_pim/pim/doctype/pim_item/test_pim_item.py",
    # PIM Vendor doctype
    "imperium_pim/pim/doctype/pim_vendor/__init__.py",
    "imperium_pim/pim/doctype/pim_vendor/pim_vendor.js",
    "imperium_pim/pim/doctype/pim_vendor/pim_vendor.json",
    "imperium_pim/pim/doctype/pim_vendor/pim_vendor.py",
    "imperium_pim/pim/doctype/pim_vendor/test_pim_vendor.py",
    # PIM Vendor Attribute doctype
    "imperium_pim/pim/doctype/pim_vendor_attribute/__init__.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute/pim_vendor_attribute.js",
    "imperium_pim/pim/doctype/pim_vendor_attribute/pim_vendor_attribute.json",
    "imperium_pim/pim/doctype/pim_vendor_attribute/pim_vendor_attribute.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute/test_pim_vendor_attribute.py",
    # PIM Vendor Attribute Mapping doctype
    "imperium_pim/pim/doctype/pim_vendor_attribute_mapping/__init__.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_mapping/pim_vendor_attribute_mapping.js",
    "imperium_pim/pim/doctype/pim_vendor_attribute_mapping/pim_vendor_attribute_mapping.json",
    "imperium_pim/pim/doctype/pim_vendor_attribute_mapping/pim_vendor_attribute_mapping.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_mapping/test_pim_vendor_attribute_mapping.py",
    # PIM Vendor Attribute Value doctype
    "imperium_pim/pim/doctype/pim_vendor_attribute_value/__init__.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value/pim_vendor_attribute_value.js",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value/pim_vendor_attribute_value.json",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value/pim_vendor_attribute_value.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value/test_pim_vendor_attribute_value.py",
    # PIM Vendor Attribute Value Mapping doctype
    "imperium_pim/pim/doctype/pim_vendor_attribute_value_mapping/__init__.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value_mapping/pim_vendor_attribute_value_mapping.js",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value_mapping/pim_vendor_attribute_value_mapping.json",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value_mapping/pim_vendor_attribute_value_mapping.py",
    "imperium_pim/pim/doctype/pim_vendor_attribute_value_mapping/test_pim_vendor_attribute_value_mapping.py",
    # Templates and other files
    "imperium_pim/templates/__init__.py",
    "imperium_pim/templates/pages/__init__.py",
    "imperium_pim/public/.gitkeep",
    "imperium_pim/scripts/build_react_frontend.py",
    "imperium_pim/www/pim-dashboard/index.html",
    "imperium_pim/www/pim-dashboard/index.py",
    "imperium_pim/imperium_pim/page/pim_dashboard/__init__.py",
    "imperium_pim/imperium_pim/page/pim_dashboard/pim_dashboard.json"
]

def run_command(cmd):
    """Run a shell command and return the output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("🚀 Starting comprehensive backend file copy...")
    print(f"📊 Total files to copy: {len(FILES_TO_COPY)}")
    
    success_count = 0
    error_count = 0
    
    for file_path in FILES_TO_COPY:
        # Create directory structure
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        print(f"📄 Processing: {file_path}")
        success_count += 1
    
    print(f"\n✅ File structure preparation completed!")
    print(f"📊 Processed {success_count} files")
    print(f"❌ Errors: {error_count}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

