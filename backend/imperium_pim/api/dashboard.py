import frappe
from frappe import _
from frappe.utils import today, add_months, add_days, getdate

@frappe.whitelist()
def get_dashboard_stats():
    """Get dashboard statistics for PIM system"""
    
    try:
        # Get total counts for each doctype
        total_items = frappe.db.count('PIM Item')
        total_vendors = frappe.db.count('PIM Vendor')
        total_attributes = frappe.db.count('PIM Attribute')
        total_attribute_values = frappe.db.count('PIM Attribute Value')
        
        # Get items by status
        active_items = frappe.db.count('PIM Item', {'status': 'Current'})
        draft_items = frappe.db.count('PIM Item', {'status': 'New'})
        discontinued_items = frappe.db.count('PIM Item', {'status': 'Discontinued'})
        
        # Get items added this month
        month_start = add_months(today(), -1)
        items_this_month = frappe.db.count('PIM Item', {
            'creation': ['>=', month_start]
        })
        
        # Get vendors added this month
        vendors_this_month = frappe.db.count('PIM Vendor', {
            'creation': ['>=', month_start]
        })
        
        # Get low stock items (items without recent activity)
        # Since we don't have stock fields, we'll use items that haven't been modified recently
        week_ago = add_days(today(), -7)  # 7 days ago
        low_activity_items = frappe.db.count('PIM Item', {
            'modified': ['<', week_ago]
        })
        
        # Get pending reviews (items with status 'New')
        pending_reviews = draft_items
        
        return {
            'total_products': total_items,
            'active_categories': total_attributes,  # Using attributes as categories
            'pending_reviews': pending_reviews,
            'low_stock_items': low_activity_items,
            'total_items': total_items,
            'total_vendors': total_vendors,
            'total_attributes': total_attributes,
            'total_attribute_values': total_attribute_values,
            'active_items': active_items,
            'draft_items': draft_items,
            'discontinued_items': discontinued_items,
            'items_this_month': items_this_month,
            'vendors_this_month': vendors_this_month
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting dashboard stats: {str(e)}")
        # Return default values if there's an error
        return {
            'total_products': 0,
            'active_categories': 0,
            'pending_reviews': 0,
            'low_stock_items': 0,
            'total_items': 0,
            'total_vendors': 0,
            'total_attributes': 0,
            'total_attribute_values': 0,
            'active_items': 0,
            'draft_items': 0,
            'discontinued_items': 0,
            'items_this_month': 0,
            'vendors_this_month': 0
        }

@frappe.whitelist()
def get_recent_items(limit=10):
    """Get recently created/modified PIM items"""
    
    try:
        items = frappe.get_list('PIM Item',
            fields=['name', 'sku', 'name1 as item_name', 'brand', 'status', 'creation', 'modified'],
            order_by='modified desc',
            limit=limit
        )
        
        # Format the data for frontend consumption
        formatted_items = []
        for item in items:
            formatted_items.append({
                'id': item.name,
                'name': item.item_name or item.sku,
                'sku': item.sku,
                'status': item.status or 'New',
                'brand': item.brand,
                'price': '$0.00',  # No price field in current structure
                'stock': 0,  # No stock field in current structure
                'lastModified': frappe.format_date(item.modified, 'medium'),
                'creation': item.creation,
                'modified': item.modified
            })
        
        return formatted_items
        
    except Exception as e:
        frappe.log_error(f"Error getting recent items: {str(e)}")
        return []

@frappe.whitelist()
def get_recent_vendors(limit=10):
    """Get recently created/modified PIM vendors"""
    
    try:
        vendors = frappe.get_list('PIM Vendor',
            fields=['name', 'vendor_name', 'vendor_code', 'vendor_active', 'creation', 'modified'],
            order_by='modified desc',
            limit=limit
        )
        
        # Format the data for frontend consumption
        formatted_vendors = []
        for vendor in vendors:
            formatted_vendors.append({
                'id': vendor.name,
                'name': vendor.vendor_name,
                'code': vendor.vendor_code,
                'active': vendor.vendor_active,
                'lastModified': frappe.format_date(vendor.modified, 'medium'),
                'creation': vendor.creation,
                'modified': vendor.modified
            })
        
        return formatted_vendors
        
    except Exception as e:
        frappe.log_error(f"Error getting recent vendors: {str(e)}")
        return []
