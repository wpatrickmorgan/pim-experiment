import frappe
from frappe import _

def get_context(context):
    """Context for the PIM frontend page"""
    context.no_cache = 1
    context.show_sidebar = False
    
    # Add any context data needed for the frontend
    context.title = _("PIM Dashboard")
    context.description = _("Product Information Management System")
    
    return context

