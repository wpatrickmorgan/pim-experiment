"""
Main API endpoints for Imperium PIM
This file provides a centralized location for all API endpoints
"""

import frappe
from frappe import _

# Import all API modules to ensure they're registered
from . import dashboard
from . import items
from . import vendors
from . import attributes
from . import ping

@frappe.whitelist(allow_guest=True)
def get_api_info():
    """Get information about available API endpoints"""
    return {
        'status': 'ok',
        'message': 'Imperium PIM API is running',
        'version': '1.0.0',
        'endpoints': {
            'ping': {
                'ping': 'imperium_pim.api.ping.ping',
                'health_check': 'imperium_pim.api.ping.health_check'
            },
            'dashboard': {
                'get_dashboard_stats': 'imperium_pim.api.dashboard.get_dashboard_stats',
                'get_recent_items': 'imperium_pim.api.dashboard.get_recent_items',
                'get_recent_vendors': 'imperium_pim.api.dashboard.get_recent_vendors'
            },
            'items': {
                'get_item_list': 'imperium_pim.api.items.get_item_list',
                'get_item_details': 'imperium_pim.api.items.get_item_details',
                'get_items_by_status': 'imperium_pim.api.items.get_items_by_status',
                'get_items_by_brand': 'imperium_pim.api.items.get_items_by_brand'
            },
            'vendors': {
                'get_vendor_list': 'imperium_pim.api.vendors.get_vendor_list',
                'get_vendor_details': 'imperium_pim.api.vendors.get_vendor_details'
            },
            'attributes': {
                'get_attribute_list': 'imperium_pim.api.attributes.get_attribute_list',
                'get_attribute_details': 'imperium_pim.api.attributes.get_attribute_details'
            }
        }
    }

# Alias methods for backward compatibility and easier access
@frappe.whitelist()
def get_stats():
    """Alias for get_dashboard_stats"""
    return dashboard.get_dashboard_stats()

@frappe.whitelist()
def get_items(limit=50, offset=0):
    """Alias for get_item_list with pagination"""
    return items.get_item_list(limit=limit)

@frappe.whitelist()
def get_products(limit=50, offset=0):
    """Alias for get_item_list (products = items)"""
    return items.get_item_list(limit=limit)

@frappe.whitelist()
def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        stats = dashboard.get_dashboard_stats()
        recent_items = dashboard.get_recent_items(limit=5)
        recent_vendors = dashboard.get_recent_vendors(limit=5)
        
        return {
            'stats': stats,
            'recent_items': recent_items,
            'recent_vendors': recent_vendors
        }
    except Exception as e:
        frappe.log_error(f"Error getting dashboard data: {str(e)}")
        return {
            'stats': {},
            'recent_items': [],
            'recent_vendors': []
        }
