# PIM Experiment - Separate Frontend & Backend Deployment

A Product Information Management (PIM) system with **separate deployment** architecture: Next.js frontend on Vercel and Frappe backend on standard Frappe sites.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTPS API      ┌─────────────────┐
│   Frontend      │ ◄──────────────► │    Backend      │
│   (Vercel)      │    Calls          │  (Frappe Site)  │
│   Static Files  │                   │   Database      │
└─────────────────┘                   └─────────────────┘
    Vercel CDN                        Your Server/Cloud
```

This repository contains both frontend and backend code optimized for separate deployment:

- **Frontend**: Next.js application optimized for Vercel deployment
- **Backend**: Clean Frappe app for standard Frappe site installation
- **Integration**: API communication between separate deployments
- **Deployment**: Simplified deployment process for each component

## 🚀 Quick Deployment

### Frontend (Vercel)
1. **Connect GitHub to Vercel**
   - Import this repository in Vercel dashboard
   - Set root directory to `frontend/`
   - Vercel will auto-detect Next.js configuration

2. **Set Environment Variables in Vercel**
   ```bash
   NEXT_PUBLIC_API_BASE_URL=https://your-frappe-site.com/api
   DEPLOYMENT_MODE=separate
   VERCEL_ENV=production
   ```

3. **Deploy**
   - Automatic deployment on every push to main branch
   - Or manually trigger deployment in Vercel dashboard

### Backend (Frappe Site)
1. **Install the App**
   ```bash
   bench get-app imperium_pim /path/to/this/repo/backend
   bench --site your-site install-app imperium_pim
   ```

2. **Configure CORS**
   ```bash
   cd apps/imperium_pim/backend/scripts
   ./deploy.sh your-site https://your-vercel-app.vercel.app
   ```

## 📁 Repository Structure

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

## 🔧 Configuration

### Frontend Environment Variables

For **production** (set in Vercel dashboard):
```bash
# API Configuration - Your Frappe site URL
NEXT_PUBLIC_API_BASE_URL=https://your-frappe-site.com/api
DEPLOYMENT_MODE=separate
VERCEL_ENV=production
```

For **development** (`frontend/.env.development`):
```bash
# Development API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
DEPLOYMENT_MODE=separate
NODE_ENV=development
```

### Backend Configuration

No separate environment files needed - configuration is handled through Frappe's standard `site_config.json` via the deployment script.

#### Key Backend Features:
- **CORS Handling**: Automatic cross-origin request support
- **Session Authentication**: Cookie-based auth with credentials
- **API Endpoints**: RESTful API for frontend communication
- **File Handling**: Upload/download support across origins

## 🌐 Production Deployment Options

### Frontend Deployment
- **Vercel** (Recommended) - Automatic deployments, global CDN
- **Netlify** - Alternative static hosting
- **AWS S3 + CloudFront** - Custom AWS setup
- **GitHub Pages** - Free hosting for public repos

### Backend Deployment
- **Standard Frappe Hosting** - Ubuntu/CentOS with bench
- **Cloud Platforms** - AWS EC2, Google Cloud, Azure
- **Docker** - Containerized deployment
- **Managed Frappe** - ERPNext.com or similar providers

## 🚀 Development

### Local Development Setup

1. **Backend (Frappe)**
   ```bash
   # In your Frappe bench directory
   bench --site your-site serve --port 8000
   ```

2. **Frontend (Next.js)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The frontend runs on `http://localhost:3000` and connects to your local Frappe backend at `http://localhost:8000`.

### Making Changes

1. **Frontend Changes**
   - Edit files in `frontend/src/`
   - Changes auto-reload in development
   - Push to GitHub for automatic Vercel deployment

2. **Backend Changes**
   - Edit files in `backend/imperium_pim/`
   - Restart Frappe: `bench restart`
   - Changes are live immediately

## 🔐 Security & CORS

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

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify backend CORS configuration
   - Check allowed origins in site_config.json
   - Ensure credentials are properly configured

2. **API Connection Issues**
   - Verify `NEXT_PUBLIC_API_BASE_URL` in frontend environment
   - Check network connectivity between servers
   - Validate SSL certificates

3. **Authentication Issues**
   - Verify cookie settings (SameSite, Secure)
   - Check HTTPS configuration
   - Validate CSRF token handling

### Debug Commands

```bash
# Check backend CORS configuration
cd backend
bench --site your-site console
>>> import frappe
>>> print(frappe.get_site_config())

# Test API connectivity
curl -v https://your-backend-domain.com/api/method/imperium_pim.api.ping

# Check frontend build
cd frontend
npm run build
npm run start
```

### Health Checks

The frontend includes a health check that verifies backend connectivity:

```javascript
// In your frontend application
const healthStatus = await api.healthCheck();
console.log(healthStatus);
```

## 🔄 Migration from Integrated Setup

If you're migrating from an integrated deployment:

1. **Backup your data**
   ```bash
   bench --site your-site backup
   ```

2. **Update environment variables**
   - Set `NEXT_PUBLIC_API_BASE_URL` in frontend
   - Configure CORS in backend

3. **Test thoroughly**
   - Verify all API endpoints work
   - Test authentication flow
   - Check file uploads/downloads

4. **Deploy gradually**
   - Start with staging environment
   - Monitor for issues
   - Have rollback plan ready

## 📊 Key Features

- **Separate Deployments**: Frontend and backend deploy independently
- **CORS Configured**: Cross-origin requests properly handled
- **Environment Management**: Separate configs for development and production
- **API Integration**: Frontend communicates with backend via REST API
- **Clean Architecture**: No unnecessary build complexity
- **Session Authentication**: Secure cookie-based auth across origins
- **File Handling**: Upload/download support with proper CORS
- **Health Monitoring**: Built-in connectivity checks

## 📞 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Verify environment variables are set correctly
3. Check that both frontend and backend are deployed and accessible
4. Review logs for specific error messages
5. Test with the provided development setup

---

**🎉 You're all set!** Your PIM system now runs with modern separate deployment architecture - frontend on Vercel's global CDN and backend on your Frappe site.
