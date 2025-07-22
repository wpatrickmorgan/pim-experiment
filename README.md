# PIM Experiment - Self-Contained Monorepo

A **self-contained** Frappe + Next.js system for Product Information Management (PIM) with complete frontend-backend integration and automated deployment.

## 🏗️ Architecture Overview

This monorepo contains **all the actual source code** from both repositories:

- **Backend**: Complete Frappe backend with imperium_pim app (copied from imperium-pim repo)
- **Frontend**: Complete Next.js application with API integration (copied from pim-experiment-frontend repo)
- **Integration**: Fully wired React Query hooks connecting to Frappe API endpoints
- **Deployment**: Nginx configuration and automation scripts for production setup

```
pim-experiment/
├── backend/                    # Complete Frappe backend files
│   ├── imperium_pim/          # PIM app with API endpoints
│   │   ├── api.py             # API endpoints for frontend
│   │   ├── pim/               # PIM doctypes and logic
│   │   └── ...                # Complete app structure
│   ├── setup.py               # App configuration
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Complete Next.js application
│   ├── src/
│   │   ├── app/               # Next.js 13+ App Router
│   │   ├── components/        # React components with real data
│   │   └── lib/               # API client & React Query hooks
│   ├── package.json           # Frontend dependencies
│   └── .env.local             # API configuration
│
├── nginx/                      # Nginx configuration
│   └── client-a.conf           # Proxy configuration
│
├── scripts/                    # Automation scripts
│   ├── setup.sh                # Complete automated setup
│   ├── build_frontend.sh       # Frontend build script
│   ├── start_backend.sh        # Backend startup script
│   └── deploy_all.sh           # Full deployment script
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Ubuntu/Debian Linux system
- Sudo access for nginx and system service configuration
- Internet connection for downloading dependencies

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/wpatrickmorgan/pim-experiment.git
cd pim-experiment

# Run the complete setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
1. ✅ Install all system dependencies (Python, Node.js, Nginx, MariaDB, Redis)
2. ✅ Initialize Frappe backend with `imperium_pim` app
3. ✅ Clone and configure Next.js frontend
4. ✅ Set up Nginx proxy configuration
5. ✅ Configure local domain (`client-a.localtest.me`)
6. ✅ Create test API endpoints
7. ✅ Start all required services

### Start the Application

```bash
# Start the backend server
./scripts/start_backend.sh

# In another terminal, visit the application
open http://client-a.localtest.me
```

## 🔗 Frontend-Backend Integration

The frontend and backend are fully integrated with:

### API Client (`frontend/src/lib/api.ts`)
- TypeScript API client with proper error handling
- Frappe session cookie authentication
- Typed interfaces for all API responses

### React Query Hooks (`frontend/src/lib/hooks.ts`)
- `usePing()` - Test backend connectivity
- `useDashboardStats()` - Real-time dashboard metrics
- `useProducts()` - Paginated product listings
- `useLogin()` / `useLogout()` - Authentication

### Backend API Endpoints (`backend/imperium_pim/api.py`)
- `/api/method/imperium_pim.api.ping` - Connectivity test
- `/api/method/imperium_pim.api.get_dashboard_stats` - Dashboard metrics
- `/api/method/imperium_pim.api.get_products` - Product listings
- `/api/method/imperium_pim.api.get_product` - Single product details

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://client-a.localtest.me | Next.js application with real data |
| **Backend API** | http://client-a.localtest.me/api | Frappe API endpoints |
| **Backend Admin** | http://localhost:8000 | Direct Frappe access |
| **Test API** | http://client-a.localtest.me/api/method/imperium_pim.api.ping | Connectivity test |

## 🔐 Default Credentials

- **Username**: `Administrator`
- **Password**: `admin`

## 📋 Available Scripts

### `./scripts/setup.sh`
Complete environment setup from scratch. Run this once to initialize everything.

### `./scripts/start_backend.sh`
Start the Frappe backend server. The frontend is served by Nginx and doesn't need a separate process.

### `./scripts/build_frontend.sh`
Build the Next.js frontend and deploy static files to Nginx.

### `./scripts/deploy_all.sh`
Full deployment: build frontend, restart backend, reload Nginx.

## 🔧 Development Workflow

### Making Frontend Changes

```bash
# Make your changes in frontend/
cd frontend
npm run dev  # For development server

# Or build and deploy
cd ..
./scripts/build_frontend.sh
```

### Making Backend Changes

```bash
# Make your changes in backend/apps/imperium_pim/
cd backend
bench restart  # Restart specific processes

# Or use the deploy script
cd ..
./scripts/deploy_all.sh
```

### Adding New API Endpoints

1. Edit `backend/apps/imperium_pim/imperium_pim/api.py`
2. Add your function with `@frappe.whitelist()` decorator
3. Restart backend: `./scripts/start_backend.sh`
4. Test: `http://client-a.localtest.me/api/method/imperium_pim.api.your_function`

## 🌍 Environment Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
# Edit .env with your specific configuration
```

Key environment variables:
- `NEXT_PUBLIC_API_BASE_URL`: Frontend API endpoint
- `FRAPPE_SITE_NAME`: Frappe site identifier
- `LOCAL_DOMAIN`: Local development domain

## 🔄 API Integration

The frontend communicates with the backend through the Nginx proxy:

```javascript
// Frontend API calls
const response = await fetch('/api/method/imperium_pim.api.get_dashboard_stats');
const data = await response.json();
```

```python
# Backend API endpoint
@frappe.whitelist()
def get_dashboard_stats():
    return {
        "total_products": 150,
        "total_categories": 25,
        "low_stock_items": 8
    }
```

## 🧪 Testing the Setup

### 1. Test Frontend
```bash
curl http://client-a.localtest.me
# Should return Next.js HTML
```

### 2. Test Backend API
```bash
curl http://client-a.localtest.me/api/method/imperium_pim.api.ping
# Should return JSON response
```

### 3. Test Authentication
```bash
# Login and get session
curl -X POST http://client-a.localtest.me/api/method/login \
  -H "Content-Type: application/json" \
  -d '{"usr": "Administrator", "pwd": "admin"}'
```

## 🛠️ Troubleshooting

### Backend Issues

```bash
# Check backend logs
tail -f backend/logs/bench.log

# Restart backend services
cd backend
bench restart
```

### Frontend Issues

```bash
# Rebuild frontend
./scripts/build_frontend.sh

# Check nginx logs
sudo tail -f /var/log/nginx/client-a.error.log
```

### Service Issues

```bash
# Check service status
systemctl status nginx
systemctl status mariadb
systemctl status redis-server

# Restart services
sudo systemctl restart nginx
sudo systemctl restart mariadb
sudo systemctl restart redis-server
```

### Permission Issues

```bash
# Fix web directory permissions
sudo chown -R www-data:www-data /var/www/client-a-frontend
sudo chmod -R 755 /var/www/client-a-frontend
```

## 📁 Project Structure Details

### Backend (`backend/`)
- Standard Frappe bench structure
- `apps/imperium_pim/`: Main PIM application
- `sites/client-a.local/`: Site-specific configuration
- API endpoints in `apps/imperium_pim/imperium_pim/api.py`

### Frontend (`frontend/`)
- Next.js 13+ with App Router
- TypeScript configuration
- Tailwind CSS for styling
- API client in `lib/api.ts`

### Nginx (`nginx/`)
- Proxy configuration for seamless integration
- Static file serving for frontend
- API proxying to backend
- CORS handling

## 🤝 Contributing

1. Make changes in the appropriate directory (`frontend/` or `backend/`)
2. Test locally using the provided scripts
3. Deploy using `./scripts/deploy_all.sh`
4. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review logs in `backend/logs/` and `/var/log/nginx/`
3. Open an issue in the GitHub repository

---

**🎉 You're all set!** Visit http://client-a.localtest.me to see your decoupled PIM system in action.
