# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document


class PIMAttribute(Document):
	def validate(self):
		"""Validate the document before saving"""
		self.validate_attribute_code()
	
	def validate_attribute_code(self):
		"""
		Validate that attribute_code follows the required format:
		- Only lowercase letters (a-z)
		- Numbers (0-9) 
		- Underscores (_)
		- No spaces, hyphens, capital letters, or special characters
		"""
		if not self.attribute_code:
			return  # Required validation is handled by the field definition
		
		# Define the allowed pattern: lowercase letters, numbers, and underscores only
		pattern = r'^[a-z0-9_]+$'
		
		if not re.match(pattern, self.attribute_code):
			# Build a helpful error message
			invalid_chars = []
			for char in self.attribute_code:
				if not re.match(r'[a-z0-9_]', char):
					if char not in invalid_chars:
						invalid_chars.append(char)
			
			error_msg = f"Attribute Code '{self.attribute_code}' contains invalid characters. "
			error_msg += "Only lowercase letters (a-z), numbers (0-9), and underscores (_) are allowed."
			
			if invalid_chars:
				if len(invalid_chars) == 1:
					error_msg += f" Invalid character found: '{invalid_chars[0]}'"
				else:
					char_list = ', '.join([f"'{char}'" for char in invalid_chars])
					error_msg += f" Invalid characters found: {char_list}"
			
			frappe.throw(error_msg)
