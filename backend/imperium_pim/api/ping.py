import frappe
from frappe.utils import now

@frappe.whitelist(allow_guest=True)
def ping():
    """Simple ping endpoint to test API connectivity"""
    return {
        'status': 'ok',
        'message': 'Imperium PIM API is running',
        'timestamp': now(),
        'version': '1.0.0'
    }

@frappe.whitelist()
def health_check():
    """Detailed health check endpoint"""
    try:
        # Test database connectivity
        frappe.db.sql("SELECT 1")
        
        # Get basic system info
        site_config = frappe.get_site_config()
        
        return {
            'status': 'healthy',
            'message': 'All systems operational',
            'timestamp': now(),
            'database': 'connected',
            'site': frappe.local.site,
            'version': frappe.__version__,
            'app_version': '1.0.0'
        }
    except Exception as e:
        frappe.log_error(f"Health check failed: {str(e)}")
        return {
            'status': 'unhealthy',
            'message': f'System error: {str(e)}',
            'timestamp': now(),
            'database': 'error',
            'site': frappe.local.site if hasattr(frappe.local, 'site') else 'unknown'
        }
