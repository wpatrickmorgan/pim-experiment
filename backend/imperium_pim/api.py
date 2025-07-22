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
    try:
        # Get counts from standard Frappe Item doctype
        total_products = frappe.db.count("Item")
        total_categories = frappe.db.count("Item Group")
        
        # Get low stock items (items with stock_qty < 10)
        low_stock_items = frappe.db.sql("""
            SELECT COUNT(*) as count 
            FROM `tabBin` 
            WHERE actual_qty < 10
        """)[0][0] if frappe.db.sql("""
            SELECT COUNT(*) as count 
            FROM `tabBin` 
            WHERE actual_qty < 10
        """) else 0
        
        # Get pending orders (Sales Orders with status Draft or To Deliver)
        pending_orders = frappe.db.count("Sales Order", {
            "status": ["in", ["Draft", "To Deliver"]]
        })
        
        return {
            "total_products": total_products,
            "total_categories": total_categories,
            "low_stock_items": low_stock_items,
            "pending_orders": pending_orders
        }
    except Exception as e:
        frappe.log_error(f"Error fetching dashboard stats: {str(e)}")
        return {
            "total_products": 0,
            "total_categories": 0,
            "low_stock_items": 0,
            "pending_orders": 0
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


@frappe.whitelist()
def get_products(limit=20, offset=0):
    """Get list of products for frontend"""
    try:
        limit = int(limit)
        offset = int(offset)
        
        # Get products from standard Item doctype
        products = frappe.db.sql("""
            SELECT 
                i.name,
                i.item_name,
                i.item_code,
                i.item_group,
                i.standard_rate,
                i.modified,
                COALESCE(b.actual_qty, 0) as stock_qty
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON i.name = b.item_code
            WHERE i.disabled = 0
            ORDER BY i.modified DESC
            LIMIT %s OFFSET %s
        """, (limit, offset), as_dict=True)
        
        return products
    except Exception as e:
        frappe.log_error(f"Error fetching products: {str(e)}")
        return []


@frappe.whitelist()
def get_product(name):
    """Get single product details"""
    try:
        product = frappe.db.sql("""
            SELECT 
                i.name,
                i.item_name,
                i.item_code,
                i.item_group,
                i.standard_rate,
                i.modified,
                COALESCE(b.actual_qty, 0) as stock_qty
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON i.name = b.item_code
            WHERE i.name = %s
        """, (name,), as_dict=True)
        
        return product[0] if product else None
    except Exception as e:
        frappe.log_error(f"Error fetching product: {str(e)}")
        return None
