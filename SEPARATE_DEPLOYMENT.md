# Vercel Frontend + Frappe Site Backend Deployment Guide

This guide explains how to deploy the PIM application with the frontend on Vercel and backend on a standard Frappe site, communicating via API.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTPS API      ┌─────────────────┐
│   Frontend      │ ◄──────────────► │    Backend      │
│   (Vercel)      │    Calls          │  (Frappe Site)  │
│   Static Files  │                   │   Database      │
└─────────────────┘                   └─────────────────┘
    Vercel CDN                        Your Server/Cloud
```

## 📁 Project Structure

```
pim-experiment/
├── frontend/                 # Next.js frontend for Vercel
│   ├── .env.production      # Production environment variables
│   ├── .env.development     # Development environment variables
│   ├── .env.local.example   # Environment template
│   ├── vercel.json          # Vercel deployment configuration
│   └── scripts/
│       ├── build.sh         # Frontend build script
│       └── deploy.sh        # Vercel deployment script
├── backend/                  # Frappe app for standard deployment
│   ├── imperium_pim/        # Main app directory
│   ├── scripts/
│   │   ├── build.sh         # App preparation script
│   │   └── deploy.sh        # Frappe site configuration script
│   ├── setup.py             # Frappe app setup
│   └── requirements.txt     # Python dependencies
└── scripts/                  # Utility scripts
    ├── setup.sh             # Initial setup
    └── validate_setup.sh    # Validation scripts
```

## 🚀 Quick Start

### 1. Environment Configuration

#### Frontend Environment Variables (Vercel)

Set these in your Vercel dashboard or update `frontend/.env.production`:
```bash
# API Configuration - Your Frappe site URL
NEXT_PUBLIC_API_BASE_URL=https://your-frappe-site.com/api
DEPLOYMENT_MODE=separate
VERCEL_ENV=production

# Optional: Analytics, monitoring, etc.
# NEXT_PUBLIC_GA_ID=your-ga-id
```

For development, update `frontend/.env.development`:
```bash
# Development API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
DEPLOYMENT_MODE=separate
NODE_ENV=development
```

#### Backend Configuration (Frappe Site)

No separate environment files needed - configuration is handled through Frappe's standard site_config.json via the deployment script.

### 2. Deploy Applications

#### Deploy Frontend to Vercel
```bash
cd frontend
./scripts/deploy.sh vercel
```

Or connect your GitHub repo to Vercel for automatic deployments.

#### Deploy Backend to Frappe Site
```bash
# From your Frappe bench directory
bench get-app imperium_pim /path/to/pim-experiment/backend
bench --site your-site install-app imperium_pim

# Configure CORS for your Vercel frontend
cd apps/imperium_pim/backend/scripts
./deploy.sh your-site https://your-vercel-app.vercel.app
```

## 🔧 Detailed Configuration

### Frontend Configuration

The frontend is configured to work as a static Next.js export that communicates with a separate backend API.

#### Key Configuration Files:

1. **`frontend/src/lib/api.ts`** - API client with cross-origin support
2. **`frontend/next.config.js`** - Next.js configuration for static export
3. **`frontend/.env.*`** - Environment-specific variables

#### API Client Features:
- Automatic API base URL detection
- Cross-origin request handling
- Enhanced error handling for CORS issues
- Health check functionality
- Session-based authentication with credentials

### Backend Configuration

The backend is configured to handle CORS requests and serve API endpoints for the separate frontend.

#### Key Configuration Files:

1. **`backend/imperium_pim/utils.py`** - CORS handling utilities
2. **`backend/imperium_pim/hooks.py`** - Request/response hooks
3. **`backend/site_config_template.json`** - Frappe site configuration
4. **`backend/cors_config.py`** - CORS setup utilities

#### CORS Configuration:
- Handles preflight OPTIONS requests
- Supports credentials for session authentication
- Configurable allowed origins
- Proper cookie settings for cross-origin

## 🐳 Docker Deployment

### Using Docker Compose (for testing)

```bash
# Start both services
docker-compose -f docker-compose.separate.yml up -d

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Individual Docker Deployment

#### Frontend Docker
```bash
cd frontend
docker build -t pim-frontend:latest .
docker run -p 3000:3000 pim-frontend:latest
```

#### Backend Docker
```bash
cd backend
docker build -t pim-backend:latest .
docker run -p 8000:8000 pim-backend:latest
```

## 🌐 Production Deployment Options

### Frontend Deployment Options

1. **Static Hosting (Recommended)**
   - AWS S3 + CloudFront
   - Netlify
   - Vercel
   - GitHub Pages

2. **Traditional Web Server**
   - Nginx (see `deployment/nginx-frontend.conf`)
   - Apache
   - Docker container

3. **CDN Integration**
   - CloudFlare
   - AWS CloudFront
   - Azure CDN

### Backend Deployment Options

1. **Traditional Hosting**
   - Ubuntu/CentOS server with Frappe bench
   - Docker container
   - Kubernetes cluster

2. **Cloud Platforms**
   - AWS EC2/ECS/EKS
   - Google Cloud Run/GKE
   - Azure Container Instances/AKS

3. **Database Options**
   - MySQL/MariaDB (recommended for Frappe)
   - PostgreSQL
   - Cloud database services

## 🔐 Security Considerations

### HTTPS Configuration
- Always use HTTPS in production
- Configure SSL certificates for both frontend and backend
- Update CORS origins to use HTTPS URLs

### Authentication
- Session-based authentication with secure cookies
- CSRF protection enabled
- Proper cookie settings for cross-origin:
  - `SameSite=None`
  - `Secure=true`

### CORS Security
- Restrict allowed origins to your actual frontend domains
- Don't use wildcard (*) origins in production
- Validate all CORS headers

## 🧪 Testing Separate Deployment

### Local Testing
```bash
# Terminal 1: Start backend
cd backend
./scripts/deploy.sh local

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### Docker Testing
```bash
# Start both services
docker-compose -f docker-compose.separate.yml up

# Test connectivity
curl http://localhost:8000/api/method/imperium_pim.api.ping
```

### Health Check
The frontend includes a health check endpoint that verifies backend connectivity:

```javascript
// In your frontend application
const healthStatus = await api.healthCheck();
console.log(healthStatus);
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify backend CORS configuration
   - Check allowed origins in site_config.json
   - Ensure credentials are properly configured

2. **Authentication Issues**
   - Verify cookie settings (SameSite, Secure)
   - Check HTTPS configuration
   - Validate CSRF token handling

3. **API Connection Issues**
   - Verify API_BASE_URL in frontend environment
   - Check network connectivity between servers
   - Validate SSL certificates

### Debug Commands

```bash
# Check backend CORS configuration
cd backend
bench --site your-site console
>>> from frappe.utils import get_site_config
>>> print(get_site_config())

# Test API connectivity
curl -v http://your-backend-domain.com/api/method/imperium_pim.api.ping

# Check frontend build
cd frontend/out
python -m http.server 3000
```

## 📊 Monitoring & Maintenance

### Health Checks
- Frontend: Built-in health check API
- Backend: Frappe system health endpoints
- Database: Connection monitoring

### Logging
- Frontend: Browser console, error tracking
- Backend: Frappe logs, access logs
- Nginx: Access and error logs

### Updates
- Frontend: Rebuild and redeploy static files
- Backend: Standard Frappe update procedures
- Database: Regular backups and maintenance

## 🔄 Migration from Monorepo

If you're migrating from the existing monorepo setup:

1. **Backup your data**
   ```bash
   bench --site your-site backup
   ```

2. **Update environment variables**
   - Set API_BASE_URL in frontend
   - Configure CORS in backend

3. **Test thoroughly**
   - Verify all API endpoints work
   - Test authentication flow
   - Check file uploads/downloads

4. **Deploy gradually**
   - Start with staging environment
   - Monitor for issues
   - Rollback plan ready

## 📞 Support

For issues with separate deployment:
1. Check this documentation
2. Review logs for specific error messages
3. Test with the provided Docker setup
4. Verify environment configuration

---

**Note**: Replace placeholder URLs and credentials with your actual values before deployment.
