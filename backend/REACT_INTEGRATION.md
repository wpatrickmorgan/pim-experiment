# React Frontend Integration for PIM Dashboard

This document explains how to integrate the React frontend (`imperium-pim-front-end`) with the Frappe backend (`imperium-pim`).

## Overview

The PIM Dashboard now uses a modern React frontend instead of traditional Frappe HTML templates. The integration provides:

- **Modern UI**: Built with React, TypeScript, Tailwind CSS, and shadcn/ui components
- **API Integration**: Connects to Frappe backend via REST API endpoints
- **Real Data**: Uses existing PIM doctypes (PIM Item, PIM Vendor, PIM Attribute, etc.)
- **No Backend Changes**: Only uses existing fields and doctypes

## API Endpoints Created

The following API endpoints have been created to serve the React frontend:

### Dashboard APIs (`imperium_pim.api.dashboard`)
- `get_dashboard_stats()` - Dashboard statistics and metrics
- `get_recent_items(limit=10)` - Recently created/modified items
- `get_recent_vendors(limit=10)` - Recently created/modified vendors

### Items APIs (`imperium_pim.api.items`)
- `get_item_list(limit=50, filters=None)` - List of PIM items with filtering
- `get_item_details(item_id)` - Detailed item information
- `get_items_by_status(status=None)` - Items filtered by status
- `get_items_by_brand(brand=None)` - Items filtered by brand

### Vendors APIs (`imperium_pim.api.vendors`)
- `get_vendor_list(limit=50, filters=None)` - List of PIM vendors with filtering
- `get_vendor_details(vendor_id)` - Detailed vendor information
- `get_active_vendors()` - Active vendors only
- `get_vendors_with_integration()` - Vendors with integration enabled
- `get_vendor_items(vendor_code, limit=50)` - Items for specific vendor

### Attributes APIs (`imperium_pim.api.attributes`)
- `get_attribute_list(limit=50, filters=None)` - List of PIM attributes
- `get_attribute_details(attribute_id)` - Detailed attribute information
- `get_attribute_values(attribute_id=None, limit=100)` - Attribute values
- `get_attributes_summary()` - Attribute statistics

## Data Mapping

The APIs map existing doctype fields to frontend-expected formats:

### PIM Item Fields Used:
- `sku` → SKU/Product ID
- `name1` → Item Name
- `brand` → Brand
- `status` → Status (New/Current/Discontinued)
- `item_type` → Product Type
- `item_weight_lbs`, `item_width_inches`, etc. → Dimensions
- `upc`, `vendor_code`, `vendor_sku` → Vendor Information

### PIM Vendor Fields Used:
- `vendor_name` → Vendor Name
- `vendor_code` → Vendor Code
- `vendor_active` → Active Status
- `vendor_integration_enabled` → Integration Status
- API configuration fields for integration details

### PIM Attribute Fields Used:
- `name` → Attribute Name
- Related `PIM Attribute Value` records → Attribute Values

## Setup Instructions

### 1. Backend Setup (Already Complete)
The backend API endpoints are already created and ready to use.

### 2. Frontend Build and Deployment

#### Option A: Manual Build
1. Clone the `imperium-pim-front-end` repository
2. Install dependencies: `npm install`
3. Build the React app: `npm run build`
4. Copy build files to: `imperium_pim/public/pim-dashboard/`
5. Restart Frappe server: `bench restart`

#### Option B: Using Build Script
```bash
# From the Frappe site directory
bench execute imperium_pim.scripts.build_react_frontend.build_and_deploy_react_frontend
```

### 3. Access the Dashboard
Once deployed, access the React dashboard at: `/pim-dashboard`

## Configuration

The React frontend receives configuration via `window.pimConfig`:

```javascript
{
  user: "current_user@example.com",
  csrfToken: "csrf_token_here",
  apiBase: "/api/method/imperium_pim.api",
  basePath: "/pim-dashboard"
}
```

This configuration is automatically injected by the Frappe backend.

## Development Mode

If the React build files are not found, the page will show a development message with:
- Setup instructions
- List of available API endpoints
- Status information

## API Usage Examples

### Get Dashboard Stats
```javascript
// Frontend API call
const stats = await pimApi.getDashboardStats();

// Direct API call
fetch('/api/method/imperium_pim.api.dashboard.get_dashboard_stats', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include'
})
```

### Get Item List
```javascript
// With filters
const items = await pimApi.getItemList();

// Direct API call with filters
fetch('/api/method/imperium_pim.api.items.get_item_list', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ filters: { status: 'Current' } }),
  credentials: 'include'
})
```

## Troubleshooting

### React App Not Loading
1. Check if build files exist in `imperium_pim/public/pim-dashboard/`
2. Verify file permissions
3. Check browser console for JavaScript errors
4. Ensure Frappe server has been restarted

### API Errors
1. Check Frappe error logs
2. Verify user permissions for PIM doctypes
3. Test API endpoints directly in browser/Postman
4. Check CSRF token configuration

### Data Not Displaying
1. Verify PIM doctypes have data
2. Check API response format matches frontend expectations
3. Review browser network tab for failed requests
4. Check field mappings in API methods

## Next Steps

The integration is now complete and functional. Future enhancements could include:

1. **Real-time Updates**: WebSocket integration for live data updates
2. **Advanced Filtering**: More sophisticated search and filter options
3. **Data Visualization**: Charts and graphs for analytics
4. **Bulk Operations**: Mass edit/import/export functionality
5. **Custom Widgets**: User-configurable dashboard components

## Support

For issues with:
- **Backend APIs**: Check Frappe error logs and API method implementations
- **Frontend Build**: Review React build process and dependencies
- **Integration**: Verify configuration and file paths
- **Data Issues**: Check doctype permissions and field mappings
