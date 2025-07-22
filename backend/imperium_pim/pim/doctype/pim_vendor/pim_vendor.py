# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PIMVendor(Document):
	pass


@frappe.whitelist()
def get_attribute_mapping_data(vendor, show_unmapped_only=0):
	"""Get vendor attributes, PIM attributes, and existing mappings for the attribute mapping table"""
	
	# Get all vendor attributes for this vendor, sorted alphabetically
	vendor_attributes = frappe.get_all(
		"PIM Vendor Attribute",
		filters={"pim_vendor": vendor},
		fields=["name", "vendor_attribute_name", "vendor_attribute_code"],
		order_by="vendor_attribute_name asc"
	)
	
	# Get all PIM attributes
	pim_attributes = frappe.get_all(
		"PIM Attribute",
		fields=["name", "attribute_name", "attribute_code"]
	)
	
	# Get existing mappings
	mappings_data = frappe.get_all(
		"PIM Vendor Attribute Mapping",
		filters={"pim_vendor": vendor},
		fields=["vendor_attribute", "pim_attribute"]
	)
	
	# Convert mappings to a dictionary for easy lookup
	mappings = {}
	for mapping in mappings_data:
		mappings[mapping.vendor_attribute] = mapping.pim_attribute
	
	# Filter vendor attributes if show_unmapped_only is checked
	if int(show_unmapped_only):
		vendor_attributes = [
			attr for attr in vendor_attributes 
			if attr.name not in mappings
		]
	
	return {
		"vendor_attributes": vendor_attributes,
		"pim_attributes": pim_attributes,
		"mappings": mappings
	}


@frappe.whitelist()
def update_attribute_mapping(vendor, vendor_attribute, pim_attribute):
	"""Create or update attribute mapping"""
	
	try:
		# Check if mapping already exists
		existing_mapping = frappe.db.get_value(
			"PIM Vendor Attribute Mapping",
			{"pim_vendor": vendor, "vendor_attribute": vendor_attribute},
			"name"
		)
		
		if pim_attribute:
			# Create or update mapping
			if existing_mapping:
				# Update existing mapping
				mapping_doc = frappe.get_doc("PIM Vendor Attribute Mapping", existing_mapping)
				mapping_doc.pim_attribute = pim_attribute
				mapping_doc.save()
				message = "Attribute mapping updated successfully"
			else:
				# Create new mapping
				mapping_doc = frappe.new_doc("PIM Vendor Attribute Mapping")
				mapping_doc.pim_vendor = vendor
				mapping_doc.vendor_attribute = vendor_attribute
				mapping_doc.pim_attribute = pim_attribute
				mapping_doc.insert()
				message = "Attribute mapping created successfully"
		else:
			# Remove mapping if pim_attribute is empty
			if existing_mapping:
				frappe.delete_doc("PIM Vendor Attribute Mapping", existing_mapping)
				message = "Attribute mapping removed successfully"
			else:
				message = "No mapping to remove"
		
		frappe.db.commit()
		
		return {
			"success": True,
			"message": message
		}
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error updating attribute mapping: {str(e)}")
		return {
			"success": False,
			"error": f"Error updating mapping: {str(e)}"
		}
