# Imperium PIM - Experimental Build

This is an experimental Frappe app that integrates a modern Next.js frontend with a Frappe backend for Product Information Management (PIM).

## Features

- **Modern Frontend**: Next.js 13+ with TypeScript, Tailwind CSS, and React Query
- **Frappe Backend**: Full Frappe app with API endpoints and data management
- **Unified Installation**: Single app installation like Frappe CRM
- **Real-time Data**: Live API integration between frontend and backend
- **Responsive Design**: Mobile-first design with modern UI components

## Installation

### Prerequisites
- Frappe Bench setup
- Node.js 18+ and npm

### Install the App

1. **Get the app:**
   ```bash
   bench get-app https://github.com/wpatrickmorgan/pim-experiment.git
   ```

2. **Install on your site:**
   ```bash
   bench --site [your-site] install-app imperium_pim
   ```

3. **Build the frontend:**
   ```bash
   cd apps/imperium_pim/imperium_pim/frontend
   ./build.sh
   ```

4. **Restart bench:**
   ```bash
   bench restart
   ```

### Access the App

- **PIM Dashboard**: `http://your-site/pim`
- **Frappe Desk**: Standard Frappe interface for backend management

## Development

### Frontend Development
```bash
cd apps/imperium_pim/imperium_pim/frontend
npm install
npm run dev
```

### Backend Development
Standard Frappe development workflow:
- API endpoints in `imperium_pim/api.py`
- DocTypes in `imperium_pim/doctype/`
- Web pages in `imperium_pim/www/`

## Architecture

### Frontend (Next.js)
- **Location**: `imperium_pim/frontend/`
- **Framework**: Next.js 13+ with App Router
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: React Query for server state, Zustand for client state
- **API Client**: Custom Frappe API integration

### Backend (Frappe)
- **API Endpoints**: RESTful APIs for frontend integration
- **DocTypes**: Standard Frappe doctypes for data management
- **Web Integration**: Serves frontend through Frappe's web system

### Integration
- Frontend builds to static files served by Frappe
- API calls use Frappe's authentication and session management
- CSRF protection and error handling built-in

## API Endpoints

### Dashboard
- `GET /api/method/imperium_pim.api.get_dashboard_stats` - Dashboard statistics

### Products
- `GET /api/method/imperium_pim.api.get_products` - Product listing with filters
- `GET /api/method/imperium_pim.api.get_product_categories` - Product categories
- `POST /api/method/imperium_pim.api.toggle_product_star` - Toggle product star
- `POST /api/method/imperium_pim.api.bulk_update_products` - Bulk operations

## Current Status

This is an experimental build with:
- ✅ Working dashboard with live API data
- ✅ Functional products page with search and filters
- ✅ Star/unstar functionality
- ✅ Responsive design and loading states
- ✅ Error handling and user feedback
- 🔄 Mock data (ready for real DocType integration)

## Next Steps

1. **Create Real DocTypes**: Replace mock data with actual Frappe DocTypes
2. **Add More Pages**: Categories, Orders, Analytics, etc.
3. **User Management**: Role-based access control
4. **File Uploads**: Image and document management
5. **Advanced Features**: Bulk operations, import/export, etc.

## Contributing

This is an experimental repository for testing build methods and integration patterns. Feel free to explore and provide feedback!

