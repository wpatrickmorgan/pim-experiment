"""
Permission functions for Imperium PIM app
"""

import frappe


def has_app_permission():
    """
    Check if the current user has permission to access the PIM app.
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    # For now, allow all logged-in users to access the PIM app
    # You can customize this logic based on your requirements
    
    if frappe.session.user == "Guest":
        return False
    
    # Check if user has any of the required roles
    # You can customize these roles based on your needs
    required_roles = ["System Manager", "PIM User", "PIM Manager"]
    user_roles = frappe.get_roles(frappe.session.user)
    
    # Allow System Manager always
    if "System Manager" in user_roles:
        return True
    
    # Check for PIM-specific roles
    for role in required_roles:
        if role in user_roles:
            return True
    
    # For development/testing, allow all authenticated users
    # Remove this in production and implement proper role-based access
    return True


def has_pim_read_permission():
    """
    Check if user has read permission for PIM data
    """
    return has_app_permission()


def has_pim_write_permission():
    """
    Check if user has write permission for PIM data
    """
    if not has_app_permission():
        return False
    
    # Additional write permission checks
    user_roles = frappe.get_roles(frappe.session.user)
    write_roles = ["System Manager", "PIM Manager", "PIM User"]
    
    for role in write_roles:
        if role in user_roles:
            return True
    
    return False


def has_pim_admin_permission():
    """
    Check if user has admin permission for PIM
    """
    user_roles = frappe.get_roles(frappe.session.user)
    admin_roles = ["System Manager", "PIM Manager"]
    
    for role in admin_roles:
        if role in user_roles:
            return True
    
    return False
