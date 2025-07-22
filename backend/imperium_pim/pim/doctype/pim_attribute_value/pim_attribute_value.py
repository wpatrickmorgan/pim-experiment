# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document


class PIMAttributeValue(Document):
	def before_insert(self):
		"""Auto-generate attribute_value_code if it's blank"""
		if not self.attribute_value_code and self.pim_attribute and self.attribute_value_name:
			self.attribute_value_code = self.generate_attribute_value_code()
	
	def before_save(self):
		"""Auto-generate attribute_value_code if it's blank"""
		if not self.attribute_value_code and self.pim_attribute and self.attribute_value_name:
			self.attribute_value_code = self.generate_attribute_value_code()
	
	def generate_attribute_value_code(self):
		"""Generate attribute_value_code using format: {pim_attribute_code}-{slugified_attribute_value_name}"""
		# Get the attribute_code from the linked PIM Attribute
		pim_attribute_doc = frappe.get_doc("PIM Attribute", self.pim_attribute)
		pim_attribute_code = pim_attribute_doc.attribute_code
		
		# Slugify the attribute_value_name
		slugified_name = self.slugify_attribute_value_name(self.attribute_value_name)
		
		# Combine to create the final code
		return f"{pim_attribute_code}-{slugified_name}"
	
	def slugify_attribute_value_name(self, name):
		"""
		Slugify attribute_value_name:
		- Lowercase
		- Replace spaces/dashes/underscores with '-'
		- Remove special characters
		"""
		if not name:
			return ""
		
		# Convert to lowercase
		slug = name.lower()
		
		# Replace spaces, dashes, and underscores with hyphens
		slug = re.sub(r'[\s\-_]+', '-', slug)
		
		# Remove special characters (keep only alphanumeric and hyphens)
		slug = re.sub(r'[^a-z0-9\-]', '', slug)
		
		# Remove leading/trailing hyphens and collapse multiple hyphens
		slug = re.sub(r'-+', '-', slug).strip('-')
		
		return slug
