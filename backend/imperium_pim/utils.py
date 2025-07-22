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
