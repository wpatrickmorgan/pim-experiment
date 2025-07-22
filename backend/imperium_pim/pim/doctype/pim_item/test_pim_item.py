# Copyright (c) 2025, Imperium Systems & Consulting and contributors
# For license information, please see license.txt

import frappe
import unittest
from frappe.tests.utils import FrappeTestCase
from imperium_pim.pim.doctype.pim_item.pim_item import get_items, validate_sku_uniqueness, get_vendor_info


class TestPIMItem(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Create a test vendor if it doesn't exist
		if not frappe.db.exists("PIM Vendor", "TEST_VENDOR"):
			vendor = frappe.get_doc({
				"doctype": "PIM Vendor",
				"vendor_name": "Test Vendor",
				"vendor_code": "TEST_VENDOR",
				"vendor_active": 1
			})
			vendor.insert(ignore_permissions=True)
		
		# Clean up any existing test items
		frappe.db.delete("PIM Item", {"vendor_code": "TEST_VENDOR"})
		frappe.db.commit()
	
	def tearDown(self):
		"""Clean up test data"""
		frappe.db.delete("PIM Item", {"vendor_code": "TEST_VENDOR"})
		frappe.db.delete("PIM Vendor", {"vendor_code": "TEST_VENDOR"})
		frappe.db.commit()
	
	def test_sku_generation(self):
		"""Test automatic SKU generation"""
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM001",
			"status": "New",
			"item_type": "Item"
		})
		
		# SKU should be empty before save
		self.assertFalse(item.sku)
		
		# Save the item
		item.insert(ignore_permissions=True)
		
		# SKU should be auto-generated
		self.assertEqual(item.sku, "TEST_VENDOR-ITEM001")
	
	def test_sku_uniqueness(self):
		"""Test SKU uniqueness constraint"""
		# Create first item
		item1 = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item 1",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM001",
			"status": "New",
			"item_type": "Item"
		})
		item1.insert(ignore_permissions=True)
		
		# Try to create second item with same vendor_code and vendor_sku
		item2 = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item 2",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM001",  # Same vendor_sku
			"status": "New",
			"item_type": "Item"
		})
		
		# This should fail due to duplicate SKU
		with self.assertRaises(frappe.DuplicateEntryError):
			item2.insert(ignore_permissions=True)
	
	def test_upc_validation(self):
		"""Test UPC validation logic"""
		# Test valid UPC
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM002",
			"upc": "123456789012",  # Valid 12-digit UPC
			"status": "New",
			"item_type": "Item"
		})
		
		# Should save without error
		item.insert(ignore_permissions=True)
		self.assertEqual(item.upc, "123456789012")
		
		# Test invalid UPC (too short)
		item2 = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item 2",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM003",
			"upc": "12345",  # Invalid - too short
			"status": "New",
			"item_type": "Item"
		})
		
		with self.assertRaises(frappe.ValidationError):
			item2.insert(ignore_permissions=True)
		
		# Test invalid UPC (contains letters)
		item3 = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item 3",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM004",
			"upc": "12345678901A",  # Invalid - contains letter
			"status": "New",
			"item_type": "Item"
		})
		
		with self.assertRaises(frappe.ValidationError):
			item3.insert(ignore_permissions=True)
	
	def test_select_field_validation(self):
		"""Test select field options validation"""
		# Test valid status
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Test Item",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "ITEM005",
			"status": "Current",  # Valid option
			"item_type": "Kit",   # Valid option
			"dropship": "Always Dropship",  # Valid option
			"assembly_required": "Yes"  # Valid option
		})
		
		# Should save without error
		item.insert(ignore_permissions=True)
		self.assertEqual(item.status, "Current")
		self.assertEqual(item.item_type, "Kit")
		self.assertEqual(item.dropship, "Always Dropship")
		self.assertEqual(item.assembly_required, "Yes")
	
	def test_crud_operations(self):
		"""Test basic CRUD operations"""
		# Create
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "CRUD Test Item",
			"brand": "Test Brand",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "CRUD001",
			"status": "New",
			"item_type": "Item",
			"item_width_inches": 10.5,
			"item_height_inches": 5.25,
			"item_weight_lbs": 2.75
		})
		item.insert(ignore_permissions=True)
		
		# Read
		retrieved_item = frappe.get_doc("PIM Item", item.name)
		self.assertEqual(retrieved_item.name1, "CRUD Test Item")
		self.assertEqual(retrieved_item.brand, "Test Brand")
		self.assertEqual(retrieved_item.item_width_inches, 10.5)
		
		# Update
		retrieved_item.brand = "Updated Brand"
		retrieved_item.item_weight_lbs = 3.0
		retrieved_item.save(ignore_permissions=True)
		
		# Verify update
		updated_item = frappe.get_doc("PIM Item", item.name)
		self.assertEqual(updated_item.brand, "Updated Brand")
		self.assertEqual(updated_item.item_weight_lbs, 3.0)
		
		# Delete
		updated_item.delete(ignore_permissions=True)
		
		# Verify deletion
		self.assertFalse(frappe.db.exists("PIM Item", item.name))
	
	def test_api_get_items(self):
		"""Test the get_items API endpoint"""
		# Create test items
		items_data = [
			{
				"name1": "API Test Item 1",
				"vendor_sku": "API001",
				"status": "New",
				"item_type": "Item",
				"brand": "Brand A"
			},
			{
				"name1": "API Test Item 2", 
				"vendor_sku": "API002",
				"status": "Current",
				"item_type": "Kit",
				"brand": "Brand B"
			}
		]
		
		created_items = []
		for item_data in items_data:
			item = frappe.get_doc({
				"doctype": "PIM Item",
				"vendor_code": "TEST_VENDOR",
				**item_data
			})
			item.insert(ignore_permissions=True)
			created_items.append(item)
		
		# Test API without filters
		response = get_items()
		self.assertTrue(response["success"])
		self.assertGreaterEqual(len(response["data"]), 2)
		
		# Test API with filters
		response = get_items(filters={"status": "New"})
		self.assertTrue(response["success"])
		self.assertEqual(len(response["data"]), 1)
		self.assertEqual(response["data"][0]["status"], "New")
		
		# Test API with brand filter
		response = get_items(filters={"brand": "Brand A"})
		self.assertTrue(response["success"])
		self.assertEqual(len(response["data"]), 1)
		self.assertEqual(response["data"][0]["brand"], "Brand A")
		
		# Test API with limit
		response = get_items(limit=1)
		self.assertTrue(response["success"])
		self.assertEqual(len(response["data"]), 1)
		self.assertEqual(response["returned_count"], 1)
	
	def test_api_filtering(self):
		"""Test API filtering functionality"""
		# Create test item with specific attributes
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "Filter Test Item",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "FILTER001",
			"status": "Current",
			"item_type": "Component",
			"brand": "Filter Brand",
			"upc": "999888777666"
		})
		item.insert(ignore_permissions=True)
		
		# Test filtering by different fields
		test_filters = [
			{"sku": item.sku},
			{"upc": "999888777666"},
			{"name1": "Filter Test Item"},
			{"status": "Current"},
			{"item_type": "Component"},
			{"vendor_code": "TEST_VENDOR"},
			{"vendor_sku": "FILTER001"},
			{"brand": "Filter Brand"}
		]
		
		for filter_dict in test_filters:
			response = get_items(filters=filter_dict)
			self.assertTrue(response["success"], f"Filter failed: {filter_dict}")
			self.assertEqual(len(response["data"]), 1, f"Filter returned wrong count: {filter_dict}")
			self.assertEqual(response["data"][0]["name"], item.name)
	
	def test_validate_sku_uniqueness_api(self):
		"""Test SKU uniqueness validation API"""
		# Create test item
		item = frappe.get_doc({
			"doctype": "PIM Item",
			"name1": "SKU Test Item",
			"vendor_code": "TEST_VENDOR",
			"vendor_sku": "UNIQUE001",
			"status": "New",
			"item_type": "Item"
		})
		item.insert(ignore_permissions=True)
		
		# Test with existing SKU
		result = validate_sku_uniqueness(item.sku)
		self.assertFalse(result["valid"])
		
		# Test with non-existing SKU
		result = validate_sku_uniqueness("NON-EXISTING-SKU")
		self.assertTrue(result["valid"])
		
		# Test with existing SKU but same document
		result = validate_sku_uniqueness(item.sku, item.name)
		self.assertTrue(result["valid"])
	
	def test_get_vendor_info_api(self):
		"""Test vendor info API"""
		# Test with existing vendor
		result = get_vendor_info("TEST_VENDOR")
		self.assertTrue(result["success"])
		self.assertEqual(result["vendor_code"], "TEST_VENDOR")
		self.assertEqual(result["vendor_name"], "Test Vendor")
		
		# Test with non-existing vendor
		result = get_vendor_info("NON_EXISTING")
		self.assertFalse(result["success"])
		self.assertIn("not found", result["message"])


if __name__ == '__main__':
	unittest.main()
