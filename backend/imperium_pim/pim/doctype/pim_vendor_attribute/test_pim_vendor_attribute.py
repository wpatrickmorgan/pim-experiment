# Copyright (c) 2025, Imperium Systems & Consulting and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from imperium_pim.pim.doctype.pim_vendor_attribute.pim_vendor_attribute import PIMVendorAttribute


class TestPIMVendorAttribute(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Create a test vendor if it doesn't exist
		if not frappe.db.exists("PIM Vendor", "ASH"):
			vendor = frappe.get_doc({
				"doctype": "PIM Vendor",
				"vendor_name": "Ashley Furniture",
				"vendor_code": "ASH",
				"vendor_active": 1
			})
			vendor.insert()
	
	def test_slugify_attribute_name(self):
		"""Test the slugification logic"""
		attr = PIMVendorAttribute()
		
		# Test basic slugification
		self.assertEqual(attr.slugify_attribute_name("Table Shape"), "table-shape")
		
		# Test with underscores and dashes
		self.assertEqual(attr.slugify_attribute_name("Table_Shape-Size"), "table-shape-size")
		
		# Test with special characters
		self.assertEqual(attr.slugify_attribute_name("Table & Chair (Set)"), "table-chair-set")
		
		# Test with multiple spaces and dashes
		self.assertEqual(attr.slugify_attribute_name("Table   ---   Shape"), "table-shape")
		
		# Test with leading/trailing spaces and dashes
		self.assertEqual(attr.slugify_attribute_name("  -Table Shape-  "), "table-shape")
		
		# Test empty string
		self.assertEqual(attr.slugify_attribute_name(""), "")
		
		# Test with numbers
		self.assertEqual(attr.slugify_attribute_name("Size 12x24"), "size-12x24")
	
	def test_generate_vendor_attribute_code(self):
		"""Test the vendor attribute code generation"""
		# Create a test vendor attribute
		attr = frappe.get_doc({
			"doctype": "PIM Vendor Attribute",
			"pim_vendor": "ASH",
			"vendor_attribute_name": "Table Shape"
		})
		
		# Test code generation
		generated_code = attr.generate_vendor_attribute_code()
		self.assertEqual(generated_code, "ASH-table-shape")
	
	def test_auto_generation_on_insert(self):
		"""Test that vendor_attribute_code is auto-generated on insert"""
		# Create a new vendor attribute without setting vendor_attribute_code
		attr = frappe.get_doc({
			"doctype": "PIM Vendor Attribute",
			"pim_vendor": "ASH",
			"vendor_attribute_name": "Table Shape"
		})
		
		# Call before_insert to simulate the hook
		attr.before_insert()
		
		# Check that vendor_attribute_code was generated
		self.assertEqual(attr.vendor_attribute_code, "ASH-table-shape")
	
	def tearDown(self):
		"""Clean up test data"""
		# Delete test records
		frappe.db.delete("PIM Vendor Attribute", {"pim_vendor": "ASH"})
		frappe.db.delete("PIM Vendor", {"vendor_code": "ASH"})
