#!/usr/bin/env python3
"""
Verification script for Imperium PIM Desk UI setup
Run this to verify all requirements are met for proper Desk UI integration
"""

import os
import json
import sys


def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False


def check_hooks_py():
    """Check hooks.py for required configurations"""
    hooks_path = "imperium_pim/hooks.py"
    if not os.path.exists(hooks_path):
        print(f"❌ hooks.py not found at {hooks_path}")
        return False
    
    with open(hooks_path, 'r') as f:
        content = f.read()
    
    checks = [
        ('app_include_desktop', 'app_include_desktop = "imperium_pim/config/desktop.py"'),
        ('desktop_icons', 'desktop_icons = ['),
        ('workspaces', 'workspaces = ['),
        ('after_install', 'after_install = "imperium_pim.utils.setup_module"'),
        ('after_migrate', 'after_migrate = "imperium_pim.utils.sync_desktop_icons"')
    ]
    
    print("\n📋 Checking hooks.py configuration:")
    all_good = True
    for check_name, check_string in checks:
        if check_string in content:
            print(f"✅ {check_name} configuration found")
        else:
            print(f"❌ {check_name} configuration missing")
            all_good = False
    
    return all_good


def check_desktop_py():
    """Check desktop.py configuration"""
    desktop_path = "imperium_pim/config/desktop.py"
    if not os.path.exists(desktop_path):
        print(f"❌ desktop.py not found at {desktop_path}")
        return False
    
    with open(desktop_path, 'r') as f:
        content = f.read()
    
    required_elements = [
        'def get_data():',
        '"module_name": "Imperium PIM"',
        '"category": "Modules"',
        '"type": "module"'
    ]
    
    print("\n🖥️  Checking desktop.py configuration:")
    all_good = True
    for element in required_elements:
        if element in content:
            print(f"✅ Found: {element}")
        else:
            print(f"❌ Missing: {element}")
            all_good = False
    
    return all_good


def check_doctypes():
    """Check all Doctypes have correct module assignment"""
    doctype_dir = "imperium_pim/doctype"
    if not os.path.exists(doctype_dir):
        print(f"❌ Doctype directory not found: {doctype_dir}")
        return False
    
    print("\n📄 Checking Doctype configurations:")
    all_good = True
    doctype_count = 0
    
    for item in os.listdir(doctype_dir):
        item_path = os.path.join(doctype_dir, item)
        if os.path.isdir(item_path):
            json_file = os.path.join(item_path, f"{item}.json")
            if os.path.exists(json_file):
                doctype_count += 1
                try:
                    with open(json_file, 'r') as f:
                        doctype_data = json.load(f)
                    
                    module = doctype_data.get('module')
                    custom = doctype_data.get('custom', 0)
                    istable = doctype_data.get('istable', 0)
                    issingle = doctype_data.get('issingle', 0)
                    
                    if module == "Imperium PIM":
                        print(f"✅ {item}: module = 'Imperium PIM'")
                    else:
                        print(f"❌ {item}: module = '{module}' (should be 'Imperium PIM')")
                        all_good = False
                    
                    if custom == 0 and istable == 0 and issingle == 0:
                        print(f"✅ {item}: correct flags (custom=0, istable=0, issingle=0)")
                    else:
                        print(f"⚠️  {item}: flags (custom={custom}, istable={istable}, issingle={issingle})")
                        
                except json.JSONDecodeError:
                    print(f"❌ {item}: Invalid JSON in {json_file}")
                    all_good = False
    
    print(f"\n📊 Total Doctypes found: {doctype_count}")
    return all_good


def check_modules_txt():
    """Check modules.txt contains the correct module"""
    modules_path = "imperium_pim/modules.txt"
    if not os.path.exists(modules_path):
        print(f"❌ modules.txt not found at {modules_path}")
        return False
    
    with open(modules_path, 'r') as f:
        content = f.read().strip()
    
    print(f"\n📝 Checking modules.txt:")
    if content == "Imperium PIM":
        print(f"✅ modules.txt contains: '{content}'")
        return True
    else:
        print(f"❌ modules.txt contains: '{content}' (should be 'Imperium PIM')")
        return False


def main():
    """Run all verification checks"""
    print("🔍 Verifying Imperium PIM Desk UI Setup")
    print("=" * 50)
    
    # Change to the correct directory if needed
    if os.path.exists("imperium_pim"):
        os.chdir(".")
    elif os.path.exists("../imperium_pim"):
        os.chdir("..")
    else:
        print("❌ Cannot find imperium_pim directory")
        sys.exit(1)
    
    checks = [
        ("Essential Files", lambda: all([
            check_file_exists("imperium_pim/hooks.py", "hooks.py"),
            check_file_exists("imperium_pim/config/desktop.py", "desktop.py"),
            check_file_exists("imperium_pim/config/workspace.py", "workspace.py"),
            check_file_exists("imperium_pim/utils.py", "utils.py"),
            check_file_exists("imperium_pim/modules.txt", "modules.txt"),
            check_file_exists("imperium_pim/module_def/imperium_pim/imperium_pim.json", "module_def")
        ])),
        ("hooks.py Configuration", check_hooks_py),
        ("desktop.py Configuration", check_desktop_py),
        ("modules.txt Content", check_modules_txt),
        ("Doctype Configurations", check_doctypes)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("\n" + "="*50)
        print("📋 INSTALLATION INSTRUCTIONS")
        print("="*50)
        print("\n1. Install the app:")
        print("   bench --site [site-name] install-app imperium_pim")
        print("\n2. Run migration:")
        print("   bench --site [site-name] migrate")
        print("\n3. Clear cache:")
        print("   bench --site [site-name] clear-cache")
        print("\n4. Restart bench:")
        print("   bench restart")
        print("\n✅ The 'Imperium PIM' module should now appear in the Desk UI!")
        print("✅ All 8 DocTypes should be accessible from the module.")
        print("\n🔧 If the module doesn't appear, run:")
        print("   bench --site [site-name] console")
        print("   >>> from imperium_pim.utils import setup_module")
        print("   >>> setup_module()")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
