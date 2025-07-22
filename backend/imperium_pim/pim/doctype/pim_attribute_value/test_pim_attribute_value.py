# Copyright (c) 2025, Imperium Systems & Consulting and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from imperium_pim.pim.doctype.pim_attribute_value.pim_attribute_value import PIMAttributeValue


class TestPIMAttributeValue(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Create a test PIM Attribute if it doesn't exist
		if not frappe.db.exists("PIM Attribute", "test-color"):
			test_attribute = frappe.get_doc({
				"doctype": "PIM Attribute",
				"attribute_code": "test-color",
				"attribute_name": "Test Color",
				"attribute_type": "Select",
				"is_required": 0
			})
			test_attribute.insert()
	
	def test_slugify_attribute_value_name(self):
		"""Test the slugify_attribute_value_name method"""
		pim_attr_value = PIMAttributeValue()
		
		# Test basic slugification
		self.assertEqual(pim_attr_value.slugify_attribute_value_name("Red Color"), "red-color")
		
		# Test with special characters
		self.assertEqual(pim_attr_value.slugify_attribute_value_name("Blue & Green!"), "blue-green")
		
		# Test with underscores and dashes
		self.assertEqual(pim_attr_value.slugify_attribute_value_name("Dark_Blue-Green"), "dark-blue-green")
		
		# Test with multiple spaces
		self.assertEqual(pim_attr_value.slugify_attribute_value_name("Light   Yellow"), "light-yellow")
		
		# Test with leading/trailing spaces and special chars
		self.assertEqual(pim_attr_value.slugify_attribute_value_name("  Purple!  "), "purple")
		
		# Test empty string
		self.assertEqual(pim_attr_value.slugify_attribute_value_name(""), "")
		
		# Test None
		self.assertEqual(pim_attr_value.slugify_attribute_value_name(None), "")
	
	def test_generate_attribute_value_code(self):
		"""Test the generate_attribute_value_code method"""
		# Create a test PIM Attribute Value document
		pim_attr_value = frappe.get_doc({
			"doctype": "PIM Attribute Value",
			"pim_attribute": "test-color",
			"attribute_value_name": "Bright Red"
		})
		
		# Test code generation
		generated_code = pim_attr_value.generate_attribute_value_code()
		self.assertEqual(generated_code, "test-color-bright-red")
	
	def test_auto_generation_on_insert(self):
		"""Test that attribute_value_code is auto-generated on insert when blank"""
		# Create a new PIM Attribute Value without attribute_value_code
		pim_attr_value = frappe.get_doc({
			"doctype": "PIM Attribute Value",
			"pim_attribute": "test-color",
			"attribute_value_name": "Forest Green"
		})
		
		# Simulate before_insert
		pim_attr_value.before_insert()
		
		# Check that attribute_value_code was generated
		self.assertEqual(pim_attr_value.attribute_value_code, "test-color-forest-green")
	
	def test_auto_generation_on_save(self):
		"""Test that attribute_value_code is auto-generated on save when blank"""
		# Create a new PIM Attribute Value without attribute_value_code
		pim_attr_value = frappe.get_doc({
			"doctype": "PIM Attribute Value",
			"pim_attribute": "test-color",
			"attribute_value_name": "Ocean Blue"
		})
		
		# Simulate before_save
		pim_attr_value.before_save()
		
		# Check that attribute_value_code was generated
		self.assertEqual(pim_attr_value.attribute_value_code, "test-color-ocean-blue")
	
	def test_no_overwrite_existing_code(self):
		"""Test that existing attribute_value_code is not overwritten"""
		# Create a PIM Attribute Value with existing code
		pim_attr_value = frappe.get_doc({
			"doctype": "PIM Attribute Value",
			"pim_attribute": "test-color",
			"attribute_value_name": "Ocean Blue",
			"attribute_value_code": "existing-code"
		})
		
		# Simulate before_save
		pim_attr_value.before_save()
		
		# Check that existing code was not overwritten
		self.assertEqual(pim_attr_value.attribute_value_code, "existing-code")
	
	def tearDown(self):
		"""Clean up test data"""
		# Delete test PIM Attribute if it exists
		if frappe.db.exists("PIM Attribute", "test-color"):
			frappe.delete_doc("PIM Attribute", "test-color", force=True)
