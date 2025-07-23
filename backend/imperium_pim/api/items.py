import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_item_list(limit=50, filters=None):
    """Get list of PIM items with filtering support"""
    
    try:
        # Build filters
        filter_dict = {}
        if filters:
            if isinstance(filters, str):
                import json
                filters = json.loads(filters)
            filter_dict.update(filters)
        
        items = frappe.get_list('PIM Item',
            fields=[
                'name', 
                'sku', 
                'name1 as item_name', 
                'brand', 
                'status', 
                'item_type',
                'creation', 
                'modified',
                'item_weight_lbs',
                'item_width_inches',
                'item_height_inches',
                'item_depth_inches',
                'upc',
                'vendor_code',
                'vendor_sku'
            ],
            filters=filter_dict,
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
                'type': item.item_type,
                'weight': item.item_weight_lbs,
                'dimensions': {
                    'width': item.item_width_inches,
                    'height': item.item_height_inches,
                    'depth': item.item_depth_inches
                },
                'upc': item.upc,
                'vendor_code': item.vendor_code,
                'vendor_sku': item.vendor_sku,
                'price': '$0.00',  # No price field in current structure
                'stock': 0,  # No stock field in current structure
                'lastModified': frappe.format_date(item.modified, 'medium'),
                'creation': item.creation,
                'modified': item.modified
            })
        
        return formatted_items
        
    except Exception as e:
        frappe.log_error(f"Error getting item list: {str(e)}")
        return []

@frappe.whitelist(allow_guest=True)
def get_item_details(item_id):
    """Get detailed information for a specific PIM item"""
    
    try:
        item = frappe.get_doc('PIM Item', item_id)
        
        return {
            'id': item.name,
            'sku': item.sku,
            'name': item.name1,
            'brand': item.brand,
            'status': item.status,
            'type': item.item_type,
            'dropship': item.dropship,
            'assembly_required': item.assembly_required,
            'dimensions': {
                'item': {
                    'width': item.item_width_inches,
                    'height': item.item_height_inches,
                    'depth': item.item_depth_inches,
                    'weight': item.item_weight_lbs
                },
                'carton': {
                    'width': item.carton_width_inches,
                    'height': item.carton_height_inches,
                    'depth': item.carton_depth_inches,
                    'weight': item.carton_weight_lbs
                }
            },
            'vendor_info': {
                'upc': item.upc,
                'vendor_code': item.vendor_code,
                'vendor_sku': item.vendor_sku
            },
            'creation': item.creation,
            'modified': item.modified
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting item details for {item_id}: {str(e)}")
        return None

@frappe.whitelist(allow_guest=True)
def get_items_by_status(status=None):
    """Get items filtered by status"""
    
    try:
        filters = {}
        if status:
            filters['status'] = status
            
        return get_item_list(filters=filters)
        
    except Exception as e:
        frappe.log_error(f"Error getting items by status {status}: {str(e)}")
        return []

@frappe.whitelist(allow_guest=True)
def get_items_by_brand(brand=None):
    """Get items filtered by brand"""
    
    try:
        filters = {}
        if brand:
            filters['brand'] = brand
            
        return get_item_list(filters=filters)
        
    except Exception as e:
        frappe.log_error(f"Error getting items by brand {brand}: {str(e)}")
        return []
