import frappe

def has_app_permission(user=None):
    """Check if user has permission to access Imperium PIM app"""
    if not user:
        user = frappe.session.user
    
    # Allow if user has access to any PIM doctype
    return (
        frappe.has_permission("PIM Item", "read", user=user) or
        frappe.has_permission("PIM Vendor", "read", user=user) or
        frappe.has_permission("PIM Attribute", "read", user=user)
    )
