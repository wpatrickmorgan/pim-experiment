"""
Workspace configuration for Imperium PIM
"""

from frappe import _


def get_data():
    """
    Return workspace configuration for Imperium PIM
    """
    return [
        {
            "name": "Pim",
            "title": _("Imperium PIM"),
            "icon": "fa fa-cube",
            "color": "#3498db",
            "is_standard": 1,
            "category": "Modules",
            "charts": [],
            "shortcuts": [
                {
                    "type": "Page",
                    "name": "pim-dashboard",
                    "label": _("PIM Dashboard"),
                    "icon": "fa fa-dashboard",
                    "color": "#3498db"
                },
                {
                    "type": "DocType",
                    "name": "PIM Item",
                    "label": _("PIM Item"),
                    "icon": "fa fa-box",
                    "color": "#2ecc71"
                },
                {
                    "type": "DocType", 
                    "name": "PIM Vendor",
                    "label": _("PIM Vendor"),
                    "icon": "fa fa-building",
                    "color": "#e74c3c"
                },
                {
                    "type": "DocType",
                    "name": "PIM Attribute",
                    "label": _("PIM Attribute"),
                    "icon": "fa fa-tags",
                    "color": "#f39c12"
                },
                {
                    "type": "DocType",
                    "name": "PIM Attribute Value",
                    "label": _("PIM Attribute Value"),
                    "icon": "fa fa-tag",
                    "color": "#9b59b6"
                }
            ],
            "cards": [
                {
                    "name": "Dashboard",
                    "label": _("Dashboard"),
                    "items": [
                        {
                            "type": "Page",
                            "name": "pim-dashboard",
                            "label": _("PIM Dashboard"),
                            "description": _("Modern PIM dashboard interface")
                        }
                    ]
                },
                {
                    "name": "Items",
                    "label": _("Items"),
                    "items": [
                        {
                            "type": "DocType",
                            "name": "PIM Item",
                            "label": _("PIM Item"),
                            "description": _("Manage product items")
                        }
                    ]
                },
                {
                    "name": "Vendors",
                    "label": _("Vendors"),
                    "items": [
                        {
                            "type": "DocType",
                            "name": "PIM Vendor",
                            "label": _("PIM Vendor"),
                            "description": _("Manage vendors")
                        },
                        {
                            "type": "DocType",
                            "name": "PIM Vendor Attribute",
                            "label": _("PIM Vendor Attribute"),
                            "description": _("Manage vendor attributes")
                        },
                        {
                            "type": "DocType",
                            "name": "PIM Vendor Attribute Value",
                            "label": _("PIM Vendor Attribute Value"),
                            "description": _("Manage vendor attribute values")
                        },
                        {
                            "type": "DocType",
                            "name": "PIM Vendor Attribute Mapping",
                            "label": _("PIM Vendor Attribute Mapping"),
                            "description": _("Map vendor attributes")
                        },
                        {
                            "type": "DocType",
                            "name": "PIM Vendor Attribute Value Mapping",
                            "label": _("PIM Vendor Attribute Value Mapping"),
                            "description": _("Map vendor attribute values")
                        }
                    ]
                },
                {
                    "name": "Attributes",
                    "label": _("Attributes"),
                    "items": [
                        {
                            "type": "DocType",
                            "name": "PIM Attribute",
                            "label": _("PIM Attribute"),
                            "description": _("Manage product attributes")
                        },
                        {
                            "type": "DocType",
                            "name": "PIM Attribute Value",
                            "label": _("PIM Attribute Value"),
                            "description": _("Manage attribute values")
                        }
                    ]
                }
            ]
        }
    ]
