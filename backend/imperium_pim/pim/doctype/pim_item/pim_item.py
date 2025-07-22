# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class PIMItem(Document):
	def before_save(self):
		"""Generate SKU if not already set and validate fields"""
		self.generate_sku()
		self.validate_upc()
	
	def generate_sku(self):
		"""Auto-generate SKU using format: {vendor_code}-{vendor_sku}"""
		if not self.sku and self.vendor_code and self.vendor_sku:
			self.sku = f"{self.vendor_code}-{self.vendor_sku}"
	
	def validate_upc(self):
		"""Validate that UPC is exactly 12 digits"""
		if self.upc:
			# Remove any whitespace
			upc_clean = str(self.upc).strip()
			
			# Check if it's exactly 12 digits
			if not re.match(r'^\d{12}$', upc_clean):
				frappe.throw(
					f"UPC must be exactly 12 digits. Got: '{self.upc}' ({len(upc_clean)} characters)",
					title="Invalid UPC Format"
				)
			
			# Update the field with cleaned value
			self.upc = upc_clean


@frappe.whitelist()
def get_items(filters=None, fields=None, limit=None, offset=None):
	"""
	REST API endpoint to retrieve PIM Items with filtering capabilities
	
	Args:
		filters (dict): Filter conditions for the query
		fields (list): List of fields to return (default: all fields)
		limit (int): Maximum number of records to return
		offset (int): Number of records to skip
	
	Returns:
		dict: Response containing items data and metadata
	"""
	try:
		# Parse filters if passed as string
		if isinstance(filters, str):
			import json
			filters = json.loads(filters)
		
		if not filters:
			filters = {}
		
		# Define allowed filter fields
		allowed_filters = [
			'sku', 'upc', 'name1', 'status', 'item_type', 
			'vendor_code', 'vendor_sku', 'brand'
		]
		
		# Clean filters to only include allowed fields
		clean_filters = {}
		for key, value in filters.items():
			if key in allowed_filters and value:
				clean_filters[key] = value
		
		# Define default fields to return (all fields)
		if not fields:
			fields = [
				'name', 'sku', 'name1', 'brand', 'status', 'item_type', 'dropship',
				'item_width_inches', 'item_depth_inches', 'item_height_inches',
				'carton_width_inches', 'carton_depth_inches', 'carton_height_inches',
				'item_weight_lbs', 'carton_weight_lbs', 'assembly_required',
				'upc', 'vendor_code', 'vendor_sku', 'creation', 'modified'
			]
		
		# Set default limit if not provided
		if not limit:
			limit = 100
		
		# Query the database
		items = frappe.get_all(
			"PIM Item",
			filters=clean_filters,
			fields=fields,
			limit=limit,
			start=offset or 0,
			order_by="modified desc"
		)
		
		# Get total count for pagination
		total_count = frappe.db.count("PIM Item", filters=clean_filters)
		
		return {
			"success": True,
			"data": items,
			"total_count": total_count,
			"returned_count": len(items),
			"filters_applied": clean_filters,
			"limit": limit,
			"offset": offset or 0
		}
		
	except Exception as e:
		frappe.log_error(f"Error in get_items API: {str(e)}")
		return {
			"success": False,
			"error": str(e),
			"message": "An error occurred while retrieving items"
		}


@frappe.whitelist()
def validate_sku_uniqueness(sku, current_name=None):
	"""
	Validate that SKU is unique across all PIM Items
	
	Args:
		sku (str): SKU to validate
		current_name (str): Current document name (for updates)
	
	Returns:
		dict: Validation result
	"""
	try:
		if not sku:
			return {"valid": True}
		
		filters = {"sku": sku}
		if current_name:
			filters["name"] = ["!=", current_name]
		
		existing = frappe.db.exists("PIM Item", filters)
		
		return {
			"valid": not bool(existing),
			"message": f"SKU '{sku}' already exists" if existing else "SKU is available"
		}
		
	except Exception as e:
		frappe.log_error(f"Error validating SKU uniqueness: {str(e)}")
		return {
			"valid": False,
			"error": str(e)
		}


@frappe.whitelist()
def get_vendor_info(vendor_code):
	"""
	Get vendor information for SKU generation
	
	Args:
		vendor_code (str): Vendor code to lookup
	
	Returns:
		dict: Vendor information
	"""
	try:
		if not vendor_code:
			return {"success": False, "message": "Vendor code is required"}
		
		vendor = frappe.get_doc("PIM Vendor", vendor_code)
		
		return {
			"success": True,
			"vendor_name": vendor.vendor_name,
			"vendor_code": vendor.vendor_code,
			"vendor_active": vendor.vendor_active
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"message": f"Vendor '{vendor_code}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error getting vendor info: {str(e)}")
		return {
			"success": False,
			"error": str(e)
		}

