"""
API endpoints for Imperium PIM frontend integration
"""

import frappe
from frappe import _


@frappe.whitelist()
def ping():
    """Test API connectivity"""
    return {
        "message": "Pong! API is working correctly.",
        "user": frappe.session.user,
        "timestamp": frappe.utils.now()
    }


@frappe.whitelist()
def get_dashboard_stats():
    """Get dashboard statistics"""
    # TODO: Implement actual statistics from PIM data
    return {
        "total_items": 0,
        "total_vendors": 0,
        "total_attributes": 0,
        "pending_reviews": 0,
        "data_quality_score": 0,
        "catalog_completeness": 0
    }


@frappe.whitelist()
def get_vendor_list():
    """Get list of all vendors"""
    try:
        vendors = frappe.get_all(
            "PIM Vendor",
            fields=["name", "vendor_name", "contact_email", "status", "creation"],
            order_by="creation desc"
        )
        return vendors
    except Exception as e:
        frappe.log_error(f"Error fetching vendors: {str(e)}")
        return []


@frappe.whitelist()
def get_item_list():
    """Get list of all items"""
    try:
        items = frappe.get_all(
            "PIM Item",
            fields=["name", "item_name", "sku", "status", "creation"],
            order_by="creation desc"
        )
        return items
    except Exception as e:
        frappe.log_error(f"Error fetching items: {str(e)}")
        return []


@frappe.whitelist()
def get_attribute_list():
    """Get list of all attributes"""
    try:
        attributes = frappe.get_all(
            "PIM Attribute",
            fields=["name", "attribute_name", "attribute_type", "is_required", "creation"],
            order_by="creation desc"
        )
        return attributes
    except Exception as e:
        frappe.log_error(f"Error fetching attributes: {str(e)}")
        return []

