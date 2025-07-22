# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document


class PIMVendorAttributeValue(Document):
	def autoname(self):
		"""Generate both the document name and vendor_attribute_value_code"""
		if not self.vendor_attribute_value_code and self.pim_vendor_attribute and self.vendor_attribute_value_name:
			self.vendor_attribute_value_code = self.generate_attribute_value_code()
		
		# Use the generated code as the document name
		if self.vendor_attribute_value_code:
			self.name = self.vendor_attribute_value_code
		else:
			frappe.throw("Cannot generate document name. Please ensure Parent Attribute and Attribute Value Name are provided.")
	
	def before_save(self):
		"""Ensure attribute_value_code is populated (backup in case autoname didn't run)"""
		if not self.vendor_attribute_value_code and self.pim_vendor_attribute and self.vendor_attribute_value_name:
			self.vendor_attribute_value_code = self.generate_attribute_value_code()
	
	def validate(self):
		"""Validate that vendor_attribute_value_code is populated"""
		if not self.vendor_attribute_value_code:
			frappe.throw("Attribute Value Code is required and could not be auto-generated. Please ensure Parent Attribute and Attribute Value Name are provided.")
	
	def generate_attribute_value_code(self):
		"""Generate attribute_value_code using format: {vendor_attribute_code}-{slugified_value_name}"""
		# Get vendor_attribute_code from the linked parent attribute
		parent_attribute = frappe.get_doc("PIM Vendor Attribute", self.pim_vendor_attribute)
		vendor_attribute_code = parent_attribute.vendor_attribute_code
		
		# Slugify the attribute_value_name
		slugified_name = self.slugify_value_name(self.vendor_attribute_value_name)
		
		# Return the formatted code
		return f"{vendor_attribute_code}-{slugified_name}"
	
	def slugify_value_name(self, value_name):
		"""
		Slugify the value name:
		- Lowercase
		- Replace spaces/dashes/underscores with '-'
		- Remove all non-alphanumeric characters except dashes
		"""
		if not value_name:
			return ""
		
		# Convert to lowercase
		slugified = value_name.lower()
		
		# Replace spaces, dashes, and underscores with single dash
		slugified = re.sub(r'[\s\-_]+', '-', slugified)
		
		# Remove all non-alphanumeric characters except dashes
		slugified = re.sub(r'[^a-z0-9\-]', '', slugified)
		
		# Remove leading/trailing dashes and collapse multiple dashes
		slugified = re.sub(r'^-+|-+$', '', slugified)
		slugified = re.sub(r'-+', '-', slugified)
		
		return slugified
