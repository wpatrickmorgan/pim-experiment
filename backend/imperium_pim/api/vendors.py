import frappe
from frappe import _

@frappe.whitelist()
def get_vendor_list(limit=50, filters=None):
    """Get list of PIM vendors with filtering support"""
    
    try:
        # Build filters
        filter_dict = {}
        if filters:
            if isinstance(filters, str):
                import json
                filters = json.loads(filters)
            filter_dict.update(filters)
        
        vendors = frappe.get_list('PIM Vendor',
            fields=[
                'name', 
                'vendor_name', 
                'vendor_code', 
                'vendor_active',
                'vendor_integration_enabled',
                'vendor_last_sync',
                'vendor_api_base_url',
                'creation', 
                'modified'
            ],
            filters=filter_dict,
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
                'integration_enabled': vendor.vendor_integration_enabled,
                'last_sync': vendor.vendor_last_sync,
                'api_url': vendor.vendor_api_base_url,
                'lastModified': frappe.format_date(vendor.modified, 'medium'),
                'creation': vendor.creation,
                'modified': vendor.modified
            })
        
        return formatted_vendors
        
    except Exception as e:
        frappe.log_error(f"Error getting vendor list: {str(e)}")
        return []

@frappe.whitelist()
def get_vendor_details(vendor_id):
    """Get detailed information for a specific PIM vendor"""
    
    try:
        vendor = frappe.get_doc('PIM Vendor', vendor_id)
        
        return {
            'id': vendor.name,
            'name': vendor.vendor_name,
            'code': vendor.vendor_code,
            'active': vendor.vendor_active,
            'integration': {
                'enabled': vendor.vendor_integration_enabled,
                'last_sync': vendor.vendor_last_sync,
                'api_base_url': vendor.vendor_api_base_url,
                'auth_type': vendor.vendor_api_auth_type,
                'endpoints': {
                    'items': vendor.vendor_items_endpoint,
                    'item_prices': vendor.vendor_item_prices_endpoint,
                    'item_categories': vendor.vendor_item_categories_endpoint,
                    'master_items': vendor.vendor_master_items_endpoint,
                    'packages': vendor.vendor_packages_endpoint,
                    'package_prices': vendor.vendor_package_prices_endpoint,
                    'package_categories': vendor.vendor_package_categories_endpoint,
                    'collections': vendor.vendor_collections_endpoint
                }
            },
            'creation': vendor.creation,
            'modified': vendor.modified
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting vendor details for {vendor_id}: {str(e)}")
        return None

@frappe.whitelist()
def get_active_vendors():
    """Get list of active vendors only"""
    
    try:
        return get_vendor_list(filters={'vendor_active': 1})
        
    except Exception as e:
        frappe.log_error(f"Error getting active vendors: {str(e)}")
        return []

@frappe.whitelist()
def get_vendors_with_integration():
    """Get list of vendors with integration enabled"""
    
    try:
        return get_vendor_list(filters={'vendor_integration_enabled': 1})
        
    except Exception as e:
        frappe.log_error(f"Error getting vendors with integration: {str(e)}")
        return []

@frappe.whitelist()
def get_vendor_items(vendor_code, limit=50):
    """Get items for a specific vendor"""
    
    try:
        items = frappe.get_list('PIM Item',
            fields=[
                'name', 
                'sku', 
                'name1 as item_name', 
                'brand', 
                'status', 
                'vendor_code',
                'vendor_sku',
                'creation', 
                'modified'
            ],
            filters={'vendor_code': vendor_code},
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
                'vendor_sku': item.vendor_sku,
                'status': item.status or 'New',
                'brand': item.brand,
                'lastModified': frappe.format_date(item.modified, 'medium'),
                'creation': item.creation,
                'modified': item.modified
            })
        
        return formatted_items
        
    except Exception as e:
        frappe.log_error(f"Error getting items for vendor {vendor_code}: {str(e)}")
        return []
