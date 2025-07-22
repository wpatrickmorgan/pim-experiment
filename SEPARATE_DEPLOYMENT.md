# Separate Frontend & Backend Deployment Guide

This guide explains how to deploy the PIM application with the frontend and backend on separate servers, communicating via API.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP/HTTPS     ┌─────────────────┐
│   Frontend      │ ◄──────────────► │    Backend      │
│   (Next.js)     │    API Calls      │   (Frappe)      │
│   Static Files  │                   │   Database      │
└─────────────────┘                   └─────────────────┘
     Server A                              Server B
```

## 📁 Project Structure

```
pim-experiment/
├── frontend/                 # Next.js frontend application
│   ├── .env.production      # Production environment variables
│   ├── .env.development     # Development environment variables
│   ├── .env.local.example   # Environment template
│   ├── scripts/
│   │   ├── build.sh         # Frontend build script
│   │   └── deploy.sh        # Frontend deployment script
│   └── Dockerfile           # Frontend Docker configuration
├── backend/                  # Frappe backend application
│   ├── .env.production      # Backend production config
│   ├── site_config_template.json  # Frappe site configuration
│   ├── cors_config.py       # CORS configuration utilities
│   ├── scripts/
│   │   ├── build.sh         # Backend build script
│   │   └── deploy.sh        # Backend deployment script
│   └── Dockerfile           # Backend Docker configuration
├── deployment/
│   └── nginx-frontend.conf  # Nginx configuration for frontend
├── scripts/
│   ├── deploy-frontend.sh   # Main frontend deployment
│   └── deploy-backend.sh    # Main backend deployment
└── docker-compose.separate.yml  # Docker Compose for testing
```

## 🚀 Quick Start

### 1. Environment Configuration

#### Frontend Environment Variables

Create `frontend/.env.production`:
```bash
# API Configuration
API_BASE_URL=https://your-backend-domain.com/api
DEPLOYMENT_MODE=separate

# Optional: Analytics, monitoring, etc.
NEXT_PUBLIC_GA_ID=your-ga-id
```

Create `frontend/.env.development`:
```bash
# Development API Configuration
API_BASE_URL=http://localhost:8000/api
DEPLOYMENT_MODE=separate
```

#### Backend Environment Variables

Create `backend/.env.production`:
```bash
# Database Configuration
DB_HOST=your-db-host
DB_NAME=pim_production
DB_USER=your-db-user
DB_PASSWORD=your-secure-password

# Frontend URLs for CORS
FRONTEND_URLS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Security
ENCRYPTION_KEY=your-encryption-key-here
```

### 2. Build Applications

#### Build Frontend
```bash
cd frontend
./scripts/build.sh
```

#### Build Backend
```bash
cd backend
./scripts/build.sh
```

### 3. Deploy Applications

#### Deploy Frontend
```bash
./scripts/deploy-frontend.sh production
```

#### Deploy Backend
```bash
./scripts/deploy-backend.sh production
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

