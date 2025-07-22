# Copyright (c) 2025, Imperium Systems & Consulting and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPIMAttribute(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Clean up any existing test data
		frappe.db.delete("PIM Attribute", {"attribute_code": ["like", "test_%"]})
		frappe.db.commit()
	
	def tearDown(self):
		"""Clean up after tests"""
		# Clean up test data
		frappe.db.delete("PIM Attribute", {"attribute_code": ["like", "test_%"]})
		frappe.db.commit()
	
	def test_valid_attribute_codes(self):
		"""Test that valid attribute codes are accepted"""
		valid_codes = [
			"test_valid_code",
			"test123",
			"test_code_123",
			"lowercase_only",
			"numbers123",
			"with_underscores_",
			"a",  # single character
			"test_very_long_attribute_code_with_many_underscores_and_numbers_123456789"
		]
		
		for i, code in enumerate(valid_codes):
			with self.subTest(code=code):
				doc = frappe.get_doc({
					"doctype": "PIM Attribute",
					"attribute_code": code,
					"attribute_name": f"Test Attribute {i}",
					"attribute_type": "ShortText"
				})
				
				# This should not raise any exception
				doc.validate()
				doc.insert()
				
				# Verify the document was created successfully
				self.assertEqual(doc.attribute_code, code)
				
				# Clean up
				doc.delete()
	
	def test_invalid_attribute_codes(self):
		"""Test that invalid attribute codes are rejected"""
		invalid_codes = [
			("Test_Code", "uppercase letters"),
			("test-code", "hyphens"),
			("test code", "spaces"),
			("test@code", "special characters"),
			("test.code", "periods"),
			("test#code", "hash symbols"),
			("test$code", "dollar signs"),
			("test%code", "percent signs"),
			("test&code", "ampersands"),
			("test*code", "asterisks"),
			("test+code", "plus signs"),
			("test=code", "equals signs"),
			("test!code", "exclamation marks"),
			("test?code", "question marks"),
			("test/code", "forward slashes"),
			("test\\code", "backslashes"),
			("test|code", "pipes"),
			("test<code", "less than signs"),
			("test>code", "greater than signs"),
			("test[code]", "brackets"),
			("test{code}", "braces"),
			("test(code)", "parentheses"),
			("test\"code", "quotes"),
			("test'code", "apostrophes"),
			("test`code", "backticks"),
			("test~code", "tildes"),
			("test^code", "carets"),
			("test:code", "colons"),
			("test;code", "semicolons"),
			("test,code", "commas"),
		]
		
		for code, description in invalid_codes:
			with self.subTest(code=code, description=description):
				doc = frappe.get_doc({
					"doctype": "PIM Attribute",
					"attribute_code": code,
					"attribute_name": f"Test Attribute for {description}",
					"attribute_type": "ShortText"
				})
				
				# This should raise a ValidationError
				with self.assertRaises(frappe.ValidationError) as context:
					doc.validate()
				
				# Verify the error message contains helpful information
				error_message = str(context.exception)
				self.assertIn("contains invalid characters", error_message)
				self.assertIn("Only lowercase letters (a-z), numbers (0-9), and underscores (_) are allowed", error_message)
	
	def test_empty_attribute_code(self):
		"""Test that empty attribute_code is handled gracefully"""
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		
		# Empty attribute_code should not raise validation error in our custom validation
		# (required validation is handled by the field definition)
		doc.validate_attribute_code()  # Should not raise exception
	
	def test_none_attribute_code(self):
		"""Test that None attribute_code is handled gracefully"""
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": None,
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		
		# None attribute_code should not raise validation error in our custom validation
		doc.validate_attribute_code()  # Should not raise exception
	
	def test_error_message_single_invalid_character(self):
		"""Test error message format for single invalid character"""
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "test-code",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		
		with self.assertRaises(frappe.ValidationError) as context:
			doc.validate()
		
		error_message = str(context.exception)
		self.assertIn("Invalid character found: '-'", error_message)
	
	def test_error_message_multiple_invalid_characters(self):
		"""Test error message format for multiple invalid characters"""
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "Test-Code@123",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		
		with self.assertRaises(frappe.ValidationError) as context:
			doc.validate()
		
		error_message = str(context.exception)
		self.assertIn("Invalid characters found:", error_message)
		# Should contain all invalid characters
		self.assertIn("'T'", error_message)  # uppercase
		self.assertIn("'-'", error_message)  # hyphen
		self.assertIn("'C'", error_message)  # uppercase
		self.assertIn("'@'", error_message)  # special character
	
	def test_edge_cases(self):
		"""Test edge cases"""
		# Test with only underscores
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "___",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		doc.validate()  # Should not raise exception
		
		# Test with only numbers
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "123456",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		doc.validate()  # Should not raise exception
		
		# Test with mixed valid characters
		doc = frappe.get_doc({
			"doctype": "PIM Attribute",
			"attribute_code": "a1b2c3_test_456",
			"attribute_name": "Test Attribute",
			"attribute_type": "ShortText"
		})
		doc.validate()  # Should not raise exception
