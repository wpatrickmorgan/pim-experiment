#!/usr/bin/env python3
"""
Verification script for Imperium PIM module restructure
"""

import os
import json
import sys

def check_file_exists(path, description):
    """Check if a file exists and report status"""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} (NOT FOUND)")
        return False

def check_json_field(file_path, field, expected_value, description):
    """Check if a JSON file contains the expected field value"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            actual_value = data.get(field)
            if actual_value == expected_value:
                print(f"✅ {description}: {field} = '{actual_value}'")
                return True
            else:
                print(f"❌ {description}: {field} = '{actual_value}' (expected '{expected_value}')")
                return False
    except Exception as e:
        print(f"❌ {description}: Error reading {file_path} - {e}")
        return False

def main():
    print("🔍 Verifying Imperium PIM Module Restructure")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check new module structure
    print("\n📁 Module Structure:")
    structure_checks = [
        ("imperium_pim/pim/__init__.py", "Pim module init"),
        ("imperium_pim/pim/doctype/__init__.py", "Pim doctype init"),
        ("imperium_pim/pim/module_def/pim.json", "Pim module definition"),
    ]
    
    for path, desc in structure_checks:
        if not check_file_exists(path, desc):
            all_checks_passed = False
    
    # Check modules.txt
    print("\n📝 modules.txt:")
    try:
        with open("imperium_pim/modules.txt", 'r') as f:
            content = f.read().strip()
            if content == "Pim":
                print(f"✅ modules.txt contains: '{content}'")
            else:
                print(f"❌ modules.txt contains: '{content}' (should be 'Pim')")
                all_checks_passed = False
    except Exception as e:
        print(f"❌ Error reading modules.txt: {e}")
        all_checks_passed = False
    
    # Check DocTypes moved to new location
    print("\n📦 DocTypes in new location:")
    expected_doctypes = [
        "pim_attribute",
        "pim_attribute_value", 
        "pim_item",
        "pim_vendor",
        "pim_vendor_attribute",
        "pim_vendor_attribute_mapping",
        "pim_vendor_attribute_value",
        "pim_vendor_attribute_value_mapping"
    ]
    
    for doctype in expected_doctypes:
        doctype_path = f"imperium_pim/pim/doctype/{doctype}"
        json_path = f"{doctype_path}/{doctype}.json"
        
        if not check_file_exists(doctype_path, f"DocType directory: {doctype}"):
            all_checks_passed = False
            continue
            
        if not check_file_exists(json_path, f"DocType JSON: {doctype}"):
            all_checks_passed = False
            continue
            
        # Check module reference in JSON
        if not check_json_field(json_path, "module", "Pim", f"DocType {doctype}"):
            all_checks_passed = False
    
    # Check module definition
    print("\n🏗️ Module Definition:")
    module_def_path = "imperium_pim/pim/module_def/pim.json"
    if os.path.exists(module_def_path):
        checks = [
            ("doctype", "Module Def", "Module definition doctype"),
            ("module_name", "Pim", "Module definition name"),
            ("app_name", "imperium_pim", "Module definition app")
        ]
        
        for field, expected, desc in checks:
            if not check_json_field(module_def_path, field, expected, desc):
                all_checks_passed = False
    
    # Check old structure is removed
    print("\n🗑️ Old structure cleanup:")
    old_paths = [
        "imperium_pim/doctype",
        "imperium_pim/module_def"
    ]
    
    for path in old_paths:
        if not os.path.exists(path):
            print(f"✅ Old path removed: {path}")
        else:
            print(f"❌ Old path still exists: {path}")
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("\nNext steps:")
        print("1. bench --site [site-name] migrate")
        print("2. bench --site [site-name] clear-cache") 
        print("3. bench restart")
        print("\nThe 'Pim' module should appear in Desk UI with all DocTypes!")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
