# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document


class PIMVendorAttribute(Document):
	def before_insert(self):
		"""Auto-generate vendor_attribute_code if it's blank"""
		if not self.vendor_attribute_code:
			self.vendor_attribute_code = self.generate_vendor_attribute_code()
	
	def before_save(self):
		"""Auto-generate vendor_attribute_code if it's blank"""
		if not self.vendor_attribute_code:
			self.vendor_attribute_code = self.generate_vendor_attribute_code()
	
	def generate_vendor_attribute_code(self):
		"""
		Generate vendor_attribute_code using format: {vendor_code}-{slugified_vendor_attribute_name}
		
		Slugification rules:
		- Convert to lowercase
		- Replace spaces, underscores, and dashes with a single dash (-)
		- Remove all non-alphanumeric characters (except dashes)
		- Collapse multiple dashes into one
		"""
		if not self.pim_vendor or not self.vendor_attribute_name:
			frappe.throw("Both Vendor and Attribute Name are required to generate the attribute code")
		
		# Get vendor_code from the linked PIM Vendor document
		vendor_doc = frappe.get_doc("PIM Vendor", self.pim_vendor)
		vendor_code = vendor_doc.vendor_code
		
		if not vendor_code:
			frappe.throw(f"Vendor Code is missing for vendor: {self.pim_vendor}")
		
		# Slugify the vendor_attribute_name
		slugified_name = self.slugify_attribute_name(self.vendor_attribute_name)
		
		# Generate the final code
		return f"{vendor_code}-{slugified_name}"
	
	def slugify_attribute_name(self, name):
		"""
		Slugify the attribute name according to the specified rules:
		- Convert to lowercase
		- Replace spaces, underscores, and dashes with a single dash (-)
		- Remove all non-alphanumeric characters (except dashes)
		- Collapse multiple dashes into one
		"""
		if not name:
			return ""
		
		# Convert to lowercase
		slug = name.lower()
		
		# Replace spaces, underscores, and existing dashes with a single dash
		slug = re.sub(r'[\s_-]+', '-', slug)
		
		# Remove all non-alphanumeric characters except dashes
		slug = re.sub(r'[^a-z0-9-]', '', slug)
		
		# Collapse multiple dashes into one
		slug = re.sub(r'-+', '-', slug)
		
		# Remove leading and trailing dashes
		slug = slug.strip('-')
		
		return slug
