# PIM Platform - Frontend/Backend Separation

A clean separation of frontend and backend for the PIM (Product Information Management) platform, with a standalone Next.js frontend and Frappe backend communicating via REST API.

## 🏗️ Architecture Overview

```
my-platform/
├── backend/                  # Frappe app and site
│   └── frappe-bench/
│       └── sites/my-site/
│           └── imperium_pim/ # PIM app with DocTypes and APIs
│
├── frontend/                 # Standalone Next.js app
│   ├── src/
│   │   ├── app/             # Next.js 13+ app directory
│   │   ├── components/      # React components
│   │   └── lib/            # Utilities and configurations
│   ├── .env.local          # Frontend environment variables
│   └── package.json        # Frontend dependencies
│
├── nginx/                    # Nginx configuration
│   └── client-a.conf        # Reverse proxy config
│
├── scripts/                  # Deployment helpers
│   ├── build_frontend.sh    # Build and export frontend
│   ├── start_backend.sh     # Start Frappe backend
│   └── deploy_all.sh        # Complete deployment
│
├── .env.example             # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+ and pip
- **Frappe Framework** (for backend)
- **Nginx** (for production deployment)

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables as needed
nano .env
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend/frappe-bench

# Install Frappe dependencies (if not already done)
pip install frappe-bench

# Create a new site (if not already created)
bench new-site my-site

# Install the PIM app
bench --site my-site install-app imperium_pim

# Start the backend
cd ../../
./scripts/start_backend.sh
```

### 3. Frontend Setup

```bash
# Install frontend dependencies
cd frontend
npm install

# Start development server
npm run dev
```

### 4. Complete Deployment

```bash
# Run complete deployment (builds frontend, starts backend, configures nginx)
./scripts/deploy_all.sh
```

### 5. Local Testing Setup

Add to your `/etc/hosts` file:
```
127.0.0.1 client-a.localtest.me
```

## 🌐 Access URLs

- **Frontend**: http://client-a.localtest.me
- **API Test**: http://client-a.localtest.me/api/method/imperium_pim.api.ping
- **Backend Direct**: http://localhost:8000 (development only)

## 📡 API Documentation

### Authentication

The frontend authenticates with the backend using session cookies:

```javascript
// Login example
const response = await fetch('/api/method/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Important for session cookies
  body: JSON.stringify({
    usr: 'username',
    pwd: 'password'
  })
});
```

### Available API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/method/imperium_pim.api.ping` | GET | Test connectivity |
| `/api/method/imperium_pim.api.get_dashboard_stats` | GET | Dashboard statistics |
| `/api/method/imperium_pim.api.get_products` | GET | Product list with pagination |
| `/api/method/imperium_pim.api.get_vendor_list` | GET | Vendor list |
| `/api/method/imperium_pim.api.get_item_list` | GET | Item list |
| `/api/method/imperium_pim.api.get_attribute_list` | GET | Attribute list |
| `/api/resource/[DocType]` | GET/POST/PUT/DELETE | Standard Frappe resource API |

### Sample API Calls

#### Using fetch (JavaScript)

```javascript
// Test API connectivity
const pingResponse = await fetch('/api/method/imperium_pim.api.ping');
const pingData = await pingResponse.json();
console.log(pingData); // { "message": "pong" }

// Get products with pagination
const productsResponse = await fetch('/api/method/imperium_pim.api.get_products?limit=10&offset=0');
const productsData = await productsResponse.json();
```

#### Using axios (JavaScript)

```javascript
import axios from 'axios';

// Configure axios with base URL
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  withCredentials: true, // Important for session cookies
});

// Test API
const pingResponse = await api.get('/method/imperium_pim.api.ping');
console.log(pingResponse.data);

// Get dashboard stats
const statsResponse = await api.get('/method/imperium_pim.api.get_dashboard_stats');
console.log(statsResponse.data);
```

#### Using curl (Command Line)

```bash
# Test API connectivity
curl http://client-a.localtest.me/api/method/imperium_pim.api.ping

# Get products
curl http://client-a.localtest.me/api/method/imperium_pim.api.get_products

# Login (get session cookie)
curl -c cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -d '{"usr":"Administrator","pwd":"admin"}' \
  http://client-a.localtest.me/api/method/login

# Use session cookie for authenticated requests
curl -b cookies.txt http://client-a.localtest.me/api/method/imperium_pim.api.get_dashboard_stats
```

## 🛠️ Development

### Frontend Development

```bash
cd frontend

# Start development server
npm run dev

# Run type checking
npm run type-check

# Run linting
npm run lint

# Build for production
npm run build
```

### Backend Development

```bash
cd backend/frappe-bench

# Access Frappe console
bench --site my-site console

# Run migrations
bench --site my-site migrate

# Install/update app
bench --site my-site install-app imperium_pim

# Restart backend
bench restart
```

### Adding New API Endpoints

1. Add new methods to `backend/frappe-bench/sites/my-site/imperium_pim/api.py`:

```python
@frappe.whitelist()
def my_new_endpoint():
    return {"message": "Hello from new endpoint"}
```

2. The endpoint will be available at `/api/method/imperium_pim.api.my_new_endpoint`

## 🔧 Configuration

### Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost/api
NODE_ENV=development
NEXT_PUBLIC_ENABLE_DEVTOOLS=true
```

### Backend Configuration

The backend CORS settings are configured in `backend/frappe-bench/sites/my-site/imperium_pim/utils.py` in the `handle_cors()` function.

### Nginx Configuration

The nginx configuration in `nginx/client-a.conf` handles:
- Serving frontend static files
- Proxying API requests to backend
- Serving uploaded files
- CORS headers
- Caching strategies

## 🚀 Deployment

### Production Deployment

1. **Build and deploy everything**:
   ```bash
   ./scripts/deploy_all.sh
   ```

2. **Or deploy components separately**:
   ```bash
   # Build frontend only
   ./scripts/build_frontend.sh
   
   # Start backend only
   ./scripts/start_backend.sh
   
   # Deploy frontend and configure nginx
   sudo cp -r frontend/out/* /var/www/client-a-frontend/
   sudo nginx -s reload
   ```

### SSL Configuration (Production)

For production with SSL, update `nginx/client-a.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/private.key;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 🏢 Multi-Tenant Setup

To add new tenants (multiple clients), duplicate the setup:

### 1. Create New Tenant Structure

```bash
# Copy the platform structure
cp -r my-platform client-b-platform

# Update configuration
cd client-b-platform
sed -i 's/client-a/client-b/g' nginx/client-b.conf
sed -i 's/my-site/client-b-site/g' scripts/*.sh
```

### 2. Update Environment Variables

```bash
# Update .env file
sed -i 's/client-a/client-b/g' .env
```

### 3. Create New Frappe Site

```bash
cd backend/frappe-bench
bench new-site client-b-site
bench --site client-b-site install-app imperium_pim
```

### 4. Deploy New Tenant

```bash
./scripts/deploy_all.sh
```

### 5. Update DNS/Hosts

Add to `/etc/hosts`:
```
127.0.0.1 client-b.localtest.me
```

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check that `handle_cors()` is properly configured in `utils.py`
   - Verify allowed origins in the CORS configuration
   - Ensure `withCredentials: true` is set in frontend requests

2. **API Not Responding**
   - Check if Frappe backend is running: `curl http://localhost:8000`
   - Verify nginx is proxying correctly: `sudo nginx -t`
   - Check nginx logs: `sudo tail -f /var/log/nginx/client-a-error.log`

3. **Frontend Not Loading**
   - Verify files are deployed: `ls -la /var/www/client-a-frontend/`
   - Check nginx configuration: `sudo nginx -t`
   - Verify domain in `/etc/hosts`

4. **Build Failures**
   - Check Node.js version: `node --version` (should be 18+)
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Useful Commands

```bash
# Check service status
sudo systemctl status nginx
ps aux | grep bench

# View logs
tail -f backend/frappe-bench/bench.log
sudo tail -f /var/log/nginx/client-a-access.log
sudo tail -f /var/log/nginx/client-a-error.log

# Restart services
sudo nginx -s reload
cd backend/frappe-bench && bench restart

# Test API connectivity
curl -v http://client-a.localtest.me/api/method/imperium_pim.api.ping
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review nginx and backend logs
- Ensure all prerequisites are installed
- Verify environment configuration

