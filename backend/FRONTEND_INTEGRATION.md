# Imperium PIM Frontend Integration

This document describes the complete integration of the React frontend into the Imperium PIM Frappe app, creating a unified, production-ready solution.

## Overview

The frontend has been successfully integrated into the Frappe app following all Frappe standards and best practices. This creates a single, installable app that includes both backend APIs and frontend dashboard.

## Architecture

### Unified Structure
```
imperium-pim/
├── imperium_pim/
│   ├── frontend/           # React app source
│   │   ├── client/        # React components and pages
│   │   ├── package.json   # Frontend dependencies
│   │   ├── vite.config.ts # Build configuration
│   │   └── README.md      # Frontend documentation
│   ├── public/
│   │   └── pim-dashboard/ # Built assets (auto-generated)
│   ├── www/
│   │   └── pim-dashboard/ # Frappe web page
│   ├── api/               # Backend API endpoints
│   ├── commands/          # Build automation
│   └── hooks.py           # Frappe app configuration
```

### Key Integration Points

1. **Asset Management**
   - Vite builds to `imperium_pim/public/pim-dashboard/`
   - Frappe serves from `/assets/imperium_pim/pim-dashboard/`
   - Automatic asset detection and serving

2. **API Integration**
   - React app connects to Frappe APIs
   - CSRF token and session handling
   - Real-time data from backend

3. **Build Automation**
   - Automatic build during app installation
   - Manual build command available
   - Integrated with Frappe lifecycle

## Features

### ✅ Production Ready
- Follows all Frappe standards
- Automated build and deployment
- Proper asset serving
- Session-based authentication

### ✅ Developer Friendly
- Hot reload during development
- TypeScript support
- Modern React patterns
- Comprehensive documentation

### ✅ Maintainable
- Single repository
- Unified versioning
- Integrated CI/CD ready
- Clear separation of concerns

## Installation & Setup

### 1. Install the App
```bash
# Standard Frappe app installation
bench get-app https://github.com/wpatrickmorgan/imperium-pim
bench --site [site] install-app imperium_pim
```

The frontend will be automatically built during installation.

### 2. Manual Build (if needed)
```bash
# Build frontend manually
bench --site [site] execute imperium_pim.commands.build_frontend

# Clean build artifacts
bench --site [site] execute imperium_pim.commands.build_frontend.cleanup
```

### 3. Access the Dashboard
Navigate to `/pim-dashboard` in your Frappe site to access the React dashboard.

## Development Workflow

### Frontend Development
```bash
# Navigate to frontend directory
cd imperium_pim/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The development server proxies API calls to your Frappe instance.

### Making Changes
1. Edit React components in `imperium_pim/frontend/client/`
2. Test using development server
3. Build for production: `npm run build`
4. Restart Frappe to see changes

## API Integration

### Backend APIs
The React app connects to these Frappe endpoints:
- `/api/method/imperium_pim.api.dashboard.get_dashboard_stats`
- `/api/method/imperium_pim.api.items.get_item_list`
- `/api/method/imperium_pim.api.vendors.get_vendor_list`
- `/api/method/imperium_pim.api.attributes.get_attribute_list`

### Frontend API Client
- `client/lib/api.ts` - API client with Frappe integration
- `client/hooks/useApi.ts` - React hooks for data fetching
- Automatic CSRF token handling
- Session-based authentication

## Configuration

### Vite Configuration
- Builds to correct Frappe asset paths
- Configures base URL for routing
- Sets up development proxy

### Frappe Integration
- Template serves React app
- Asset detection and serving
- Configuration injection
- Permission checking

## Benefits of Unified Approach

### ✅ Simplified Deployment
- Single app to install
- No separate frontend deployment
- Unified versioning and releases

### ✅ Better Integration
- Native Frappe authentication
- Direct API access
- Consistent user experience

### ✅ Easier Maintenance
- Single repository to manage
- Unified development workflow
- Consistent coding standards

### ✅ Production Ready
- Follows Frappe conventions
- Proper asset optimization
- Scalable architecture

## Troubleshooting

### Frontend Not Loading
1. Check if build files exist: `ls imperium_pim/public/pim-dashboard/`
2. Rebuild frontend: `bench --site [site] execute imperium_pim.commands.build_frontend`
3. Restart Frappe: `bench restart`

### API Errors
1. Verify API endpoints are accessible
2. Check user permissions
3. Ensure CSRF tokens are working

### Build Errors
1. Check Node.js version (18+ required)
2. Clear node_modules and reinstall
3. Check for missing dependencies

## Next Steps

The integration is complete and ready for:
1. **Testing** - Verify all functionality works
2. **Customization** - Add more features as needed
3. **Deployment** - Deploy to production environment
4. **Documentation** - Update user documentation

This unified solution provides a robust, maintainable, and scalable foundation for the Imperium PIM system.

