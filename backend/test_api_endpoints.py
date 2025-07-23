#!/usr/bin/env python3
"""
API Endpoint Test Script for Imperium PIM

This script tests all the API endpoints that the frontend expects to ensure
they're working correctly.

Usage:
    python test_api_endpoints.py [base_url]

Example:
    python test_api_endpoints.py http://138.197.71.50:8000
"""

import requests
import json
import sys

def test_endpoint(base_url, endpoint, description):
    """Test a single API endpoint"""
    url = f"{base_url}/api/method/{endpoint}"
    
    try:
        print(f"Testing {description}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {description}")
            print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ FAILED: {description}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {description}")
        print(f"   Exception: {str(e)}")
        return False
    
    print("-" * 50)

def main():
    """Main test function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://138.197.71.50:8000"
    
    print("🧪 Imperium PIM API Endpoint Tests")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print()
    
    # List of endpoints to test
    endpoints = [
        ("imperium_pim.api.ping.ping", "Ping endpoint"),
        ("imperium_pim.api.ping.health_check", "Health check endpoint"),
        ("imperium_pim.api.api.get_api_info", "API info endpoint"),
        ("imperium_pim.api.dashboard.get_dashboard_stats", "Dashboard stats"),
        ("imperium_pim.api.dashboard.get_recent_items", "Recent items"),
        ("imperium_pim.api.dashboard.get_recent_vendors", "Recent vendors"),
        ("imperium_pim.api.items.get_item_list", "Items list"),
        ("imperium_pim.api.vendors.get_vendor_list", "Vendors list"),
        ("imperium_pim.api.attributes.get_attribute_list", "Attributes list"),
        ("imperium_pim.api.api.get_stats", "Stats alias"),
        ("imperium_pim.api.api.get_items", "Items alias"),
        ("imperium_pim.api.api.get_dashboard_data", "Dashboard data"),
    ]
    
    successful = 0
    total = len(endpoints)
    
    for endpoint, description in endpoints:
        if test_endpoint(base_url, endpoint, description):
            successful += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {successful}/{total} endpoints working")
    
    if successful == total:
        print("🎉 All API endpoints are working correctly!")
        return 0
    else:
        print("⚠️  Some API endpoints are not working. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
