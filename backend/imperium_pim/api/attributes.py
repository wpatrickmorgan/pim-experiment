import frappe
from frappe import _

@frappe.whitelist()
def get_attribute_list(limit=50, filters=None):
    """Get list of PIM attributes with filtering support"""
    
    try:
        # Build filters
        filter_dict = {}
        if filters:
            if isinstance(filters, str):
                import json
                filters = json.loads(filters)
            filter_dict.update(filters)
        
        attributes = frappe.get_list('PIM Attribute',
            fields=[
                'name', 
                'creation', 
                'modified'
            ],
            filters=filter_dict,
            order_by='modified desc',
            limit=limit
        )
        
        # Format the data for frontend consumption
        formatted_attributes = []
        for attr in attributes:
            # Get attribute values count
            values_count = frappe.db.count('PIM Attribute Value', {'parent': attr.name})
            
            formatted_attributes.append({
                'id': attr.name,
                'name': attr.name,
                'values_count': values_count,
                'lastModified': frappe.format_date(attr.modified, 'medium'),
                'creation': attr.creation,
                'modified': attr.modified
            })
        
        return formatted_attributes
        
    except Exception as e:
        frappe.log_error(f"Error getting attribute list: {str(e)}")
        return []

@frappe.whitelist()
def get_attribute_details(attribute_id):
    """Get detailed information for a specific PIM attribute"""
    
    try:
        attribute = frappe.get_doc('PIM Attribute', attribute_id)
        
        # Get attribute values
        values = frappe.get_list('PIM Attribute Value',
            fields=['name', 'creation', 'modified'],
            filters={'parent': attribute_id},
            order_by='creation asc'
        )
        
        return {
            'id': attribute.name,
            'name': attribute.name,
            'values': values,
            'values_count': len(values),
            'creation': attribute.creation,
            'modified': attribute.modified
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting attribute details for {attribute_id}: {str(e)}")
        return None

@frappe.whitelist()
def get_attribute_values(attribute_id=None, limit=100):
    """Get attribute values, optionally filtered by attribute"""
    
    try:
        filters = {}
        if attribute_id:
            filters['parent'] = attribute_id
            
        values = frappe.get_list('PIM Attribute Value',
            fields=[
                'name',
                'parent as attribute_name',
                'creation', 
                'modified'
            ],
            filters=filters,
            order_by='parent asc, creation asc',
            limit=limit
        )
        
        # Format the data for frontend consumption
        formatted_values = []
        for value in values:
            formatted_values.append({
                'id': value.name,
                'name': value.name,
                'attribute_name': value.attribute_name,
                'lastModified': frappe.format_date(value.modified, 'medium'),
                'creation': value.creation,
                'modified': value.modified
            })
        
        return formatted_values
        
    except Exception as e:
        frappe.log_error(f"Error getting attribute values: {str(e)}")
        return []

@frappe.whitelist()
def get_attributes_summary():
    """Get summary statistics for attributes"""
    
    try:
        total_attributes = frappe.db.count('PIM Attribute')
        total_values = frappe.db.count('PIM Attribute Value')
        
        # Get attributes with most values
        attributes_with_counts = frappe.db.sql("""
            SELECT 
                parent as attribute_name,
                COUNT(*) as value_count
            FROM `tabPIM Attribute Value`
            GROUP BY parent
            ORDER BY value_count DESC
            LIMIT 10
        """, as_dict=True)
        
        return {
            'total_attributes': total_attributes,
            'total_values': total_values,
            'top_attributes': attributes_with_counts,
            'average_values_per_attribute': round(total_values / total_attributes, 2) if total_attributes > 0 else 0
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting attributes summary: {str(e)}")
        return {
            'total_attributes': 0,
            'total_values': 0,
            'top_attributes': [],
            'average_values_per_attribute': 0
        }
