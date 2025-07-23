import frappe
from frappe import _

def get_context(context):
    """Simple PIM Dashboard status page"""
    
    # Check if user has permission to access PIM module
    if not frappe.has_permission("PIM Item", "read"):
        frappe.throw(_("You don't have permission to access PIM Dashboard"), frappe.PermissionError)
    
    context.no_cache = 1
    context.show_sidebar = False
    
    return context
