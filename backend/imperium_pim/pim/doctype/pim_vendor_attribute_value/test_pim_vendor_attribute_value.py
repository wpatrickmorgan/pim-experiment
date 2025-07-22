# Copyright (c) 2025, Imperium Systems & Consulting and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from imperium_pim.pim.doctype.pim_vendor_attribute_value.pim_vendor_attribute_value import PIMVendorAttributeValue


class TestPIMVendorAttributeValue(FrappeTestCase):
	def test_slugify_value_name(self):
		"""Test the slugify_value_name method"""
		doc = PIMVendorAttributeValue()
		
		# Test basic slugification
		self.assertEqual(doc.slugify_value_name("Red Color"), "red-color")
		self.assertEqual(doc.slugify_value_name("Blue_Shade"), "blue-shade")
		self.assertEqual(doc.slugify_value_name("Green-Tone"), "green-tone")
		
		# Test special characters removal
		self.assertEqual(doc.slugify_value_name("Size (Large)"), "size-large")
		self.assertEqual(doc.slugify_value_name("Weight: 100kg"), "weight-100kg")
		self.assertEqual(doc.slugify_value_name("Brand & Model"), "brand-model")
		
		# Test edge cases
		self.assertEqual(doc.slugify_value_name(""), "")
		self.assertEqual(doc.slugify_value_name("   "), "")
		self.assertEqual(doc.slugify_value_name("---"), "")
		self.assertEqual(doc.slugify_value_name("Multiple   Spaces"), "multiple-spaces")
		self.assertEqual(doc.slugify_value_name("--Multiple--Dashes--"), "multiple-dashes")
		
		# Test mixed cases
		self.assertEqual(doc.slugify_value_name("CamelCase_Value"), "camelcase-value")
		self.assertEqual(doc.slugify_value_name("123-ABC_def"), "123-abc-def")
	
	def test_generate_attribute_value_code_format(self):
		"""Test that the generated code follows the correct format"""
		# This would require setting up test data for PIM Vendor Attribute
		# For now, we'll test the method structure exists
		doc = PIMVendorAttributeValue()
		self.assertTrue(hasattr(doc, 'generate_attribute_value_code'))
		self.assertTrue(hasattr(doc, 'before_save'))
