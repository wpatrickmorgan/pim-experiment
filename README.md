# PIM Experiment Repository

This is an experimental repository containing the backend components of the Imperium PIM application, copied from the main `imperium-pim` repository. This repo is designed for testing different build methods and experimenting with alternative frontend implementations.

## What's Included

This repository contains **only the backend/core Frappe app components**:

### ✅ Included (Backend Components)
- **Core App Files**: `setup.py`, `requirements.txt`, `MANIFEST.in`
- **App Configuration**: `hooks.py` (modified to remove frontend references)
- **API Endpoints**: All API modules for frontend integration
- **Doctype Definitions**: All 8 PIM doctypes with their JSON schemas and Python controllers
- **Module Configuration**: Desktop, workspace, and module definitions
- **Utility Functions**: Setup, migration, and utility scripts
- **Templates & Static Assets**: Basic template structure and public assets

### ❌ Excluded (Frontend Components)
- **Frontend Directory**: Complete React frontend implementation
- **Build Scripts**: Frontend-specific build and integration scripts
- **Frontend Documentation**: React integration guides and documentation

## Repository Structure

```
pim-experiment/
├── setup.py                    # Python package configuration
├── requirements.txt             # Dependencies (frappe)
├── MANIFEST.in                  # Package manifest
├── README.md                    # This file
└── imperium_pim/               # Main app directory
    ├── __init__.py             # App version (0.0.1)
    ├── hooks.py                # App configuration (frontend refs removed)
    ├── modules.txt             # Module list (Pim)
    ├── patches.txt             # Migration patches
    ├── api.py                  # Main API endpoints
    ├── commands.py             # Custom bench commands
    ├── utils.py                # Utility functions
    ├── api/                    # API modules
    ├── config/                 # App configuration
    ├── pim/                    # Core PIM functionality
    │   ├── doctype/           # All 8 PIM doctypes
    │   └── module_def/        # Module definition
    ├── templates/              # HTML templates
    ├── public/                 # Static assets
    └── www/                    # Web pages
```

## Purpose

This experimental repository allows for:

1. **Testing Alternative Build Methods**: Experiment with different ways to build and deploy the PIM backend
2. **Frontend Experimentation**: Build alternative frontend implementations on top of the core Frappe app
3. **Isolated Development**: Make changes without affecting the main repository
4. **Architecture Testing**: Test different architectural approaches for the PIM system

## Usage

This is a standard Frappe app that can be installed in any Frappe/ERPNext environment:

```bash
# Install the app
bench get-app pim-experiment https://github.com/wpatrickmorgan/pim-experiment
bench --site [site-name] install-app imperium_pim

# Run migrations
bench --site [site-name] migrate

# Clear cache and restart
bench --site [site-name] clear-cache
bench restart
```

## API Endpoints

The backend provides several API endpoints for frontend integration:

- `GET /api/method/imperium_pim.api.ping` - Test connectivity
- `GET /api/method/imperium_pim.api.get_dashboard_stats` - Dashboard statistics
- `GET /api/method/imperium_pim.api.get_vendor_list` - List all vendors
- `GET /api/method/imperium_pim.api.get_item_list` - List all items
- `GET /api/method/imperium_pim.api.get_attribute_list` - List all attributes

## Doctypes

The following PIM doctypes are included:

1. **PIM Item** - Core product/item management
2. **PIM Vendor** - Vendor/supplier management
3. **PIM Attribute** - Product attribute definitions
4. **PIM Attribute Value** - Attribute value management
5. **PIM Vendor Attribute** - Vendor-specific attributes
6. **PIM Vendor Attribute Mapping** - Vendor attribute mappings
7. **PIM Vendor Attribute Value** - Vendor attribute values
8. **PIM Vendor Attribute Value Mapping** - Vendor attribute value mappings

## Notes

- This repository is for **experimental purposes only**
- No changes should be made to the original `imperium-pim` repository
- Frontend components have been intentionally excluded
- The `hooks.py` file has been modified to remove frontend-related configurations
- All backend functionality remains intact and ready for use

## Next Steps

Use this repository to:
- Build alternative frontend implementations
- Test different deployment strategies
- Experiment with API integrations
- Validate architectural changes

---

*Created by copying backend files from imperium-pim repository, excluding all frontend components.*

