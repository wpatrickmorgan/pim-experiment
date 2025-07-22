"""
Desktop configuration for Imperium PIM module
"""

from frappe import _


def get_data():
    """
    Return desktop configuration for Imperium PIM module
    """
    return [
        {
            "module_name": "Pim",
            "category": "Modules",
            "label": _("Imperium PIM"),
            "color": "#3498db",  # Blue color
            "icon": "fa fa-cube",  # Font Awesome cube icon for PIM
            "type": "module",
            "description": _("Product Information Management System"),
        }
    ]
