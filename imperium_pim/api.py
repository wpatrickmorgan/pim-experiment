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
    # For now, return mock data that matches the frontend structure
    # In a real implementation, this would query actual Frappe doctypes
    return {
        "total_products": 156,
        "active_products": 134,
        "draft_products": 12,
        "low_stock_products": 8,
        "total_categories": 12,
        "recent_orders": 23,
        "revenue_this_month": 45678.90,
        "revenue_growth": 12.5
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
def get_products(filters=None, limit=20, offset=0, search_term=None):
    """Get products with filtering and pagination"""
    
    # For now, return mock data that matches the frontend structure
    # In a real implementation, this would query actual Frappe doctypes
    
    mock_products = [
        {
            "name": "PROD-001",
            "item_name": "Wireless Bluetooth Headphones",
            "item_code": "WBH-001-BLK",
            "item_group": "Electronics",
            "status": "Active",
            "stock_qty": 156,
            "standard_rate": 79.99,
            "image_count": 4,
            "modified": "2024-01-15 02:35:00",
            "is_starred": True,
        },
        {
            "name": "PROD-002",
            "item_name": "Smartphone Case - Clear Protective",
            "item_code": "SPC-002-CLR",
            "item_group": "Accessories",
            "status": "Draft",
            "stock_qty": 23,
            "standard_rate": 14.99,
            "image_count": 2,
            "modified": "2024-01-15 03:12:00",
            "is_starred": False,
        },
        {
            "name": "PROD-003",
            "item_name": "USB-C Fast Charger 65W",
            "item_code": "UFC-003-65W",
            "item_group": "Electronics",
            "status": "Active",
            "stock_qty": 8,
            "standard_rate": 24.99,
            "image_count": 3,
            "modified": "2024-01-15 01:48:00",
            "is_starred": False,
        },
        {
            "name": "PROD-004",
            "item_name": "Wireless Mouse - Ergonomic Design",
            "item_code": "WME-004-ERG",
            "item_group": "Accessories",
            "status": "Review",
            "stock_qty": 92,
            "standard_rate": 34.99,
            "image_count": 5,
            "modified": "2024-01-14 11:02:00",
            "is_starred": True,
        },
        {
            "name": "PROD-005",
            "item_name": "Laptop Stand Adjustable Aluminum",
            "item_code": "LSA-005-ALU",
            "item_group": "Furniture",
            "status": "Active",
            "stock_qty": 67,
            "standard_rate": 49.99,
            "image_count": 6,
            "modified": "2024-01-14 09:18:00",
            "is_starred": False,
        },
        {
            "name": "PROD-006",
            "item_name": "Mechanical Keyboard RGB Backlit",
            "item_code": "MKB-006-RGB",
            "item_group": "Electronics",
            "status": "Active",
            "stock_qty": 134,
            "standard_rate": 89.99,
            "image_count": 8,
            "modified": "2024-01-14 07:05:00",
            "is_starred": False,
        },
        {
            "name": "PROD-007",
            "item_name": "Desk Lamp LED Adjustable",
            "item_code": "DLA-007-LED",
            "item_group": "Furniture",
            "status": "Active",
            "stock_qty": 45,
            "standard_rate": 39.99,
            "image_count": 4,
            "modified": "2024-01-14 06:42:00",
            "is_starred": False,
        },
    ]
    
    # Apply search filter if provided
    if search_term:
        search_term = search_term.lower()
        mock_products = [
            p for p in mock_products 
            if search_term in p["item_name"].lower() 
            or search_term in p["item_code"].lower()
            or search_term in p["item_group"].lower()
        ]
    
    # Apply status filter if provided
    if filters and isinstance(filters, dict) and filters.get("status"):
        mock_products = [
            p for p in mock_products 
            if p["status"] == filters["status"]
        ]
    
    # Apply category filter if provided
    if filters and isinstance(filters, dict) and filters.get("category"):
        mock_products = [
            p for p in mock_products 
            if p["item_group"] == filters["category"]
        ]
    
    # Apply pagination
    start = int(offset or 0)
    end = start + int(limit or 20)
    paginated_products = mock_products[start:end]
    
    return {
        "products": paginated_products,
        "total_count": len(mock_products),
        "has_more": end < len(mock_products)
    }


@frappe.whitelist()
def get_product_categories():
    """Get list of product categories"""
    return [
        {"name": "Electronics", "count": 4},
        {"name": "Accessories", "count": 2},
        {"name": "Furniture", "count": 2},
    ]


@frappe.whitelist()
def toggle_product_star(product_name):
    """Toggle star status for a product"""
    # In a real implementation, this would update the actual doctype
    return {"success": True, "message": "Product star status updated"}


@frappe.whitelist()
def bulk_update_products(product_names, action, value=None):
    """Bulk update products"""
    # In a real implementation, this would perform bulk operations
    return {
        "success": True, 
        "message": f"Bulk {action} completed for {len(product_names)} products"
    }
