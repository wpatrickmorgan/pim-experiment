# Railway Deployment Guide for Frappe/ERPNext

This guide explains how to deploy your Frappe/ERPNext backend on Railway.app with both development and production configurations.

## 🚀 Quick Start

### Prerequisites
1. Railway account at [railway.app](https://railway.app)
2. Railway CLI installed: `npm install -g @railway/cli`
3. This repository with the Railway configuration files

### Environment Setup

#### Required Services
Your Railway project needs these services:
- **MariaDB** (managed database service)
- **Redis** (managed cache service)
- **Your Frappe App** (this backend)

## 📋 Environment Variables

### Required Variables
Set these in your Railway project:

```bash
# Site Configuration
SITE_NAME=mysite                    # Your site name
ADMIN_PASSWORD=your_secure_password # Admin user password (REQUIRED)

# Environment Mode
FRAPPE_ENV=production              # or "development"
DEVELOPER_MODE=0                   # 1 for dev, 0 for production

# Optional Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
DEFAULT_SENDER_EMAIL=your-email@gmail.com

# Security (auto-generated if not provided)
ENCRYPTION_KEY=your-32-char-key
SECRET_KEY=your-secret-key
```

### Auto-Provided by Railway
These are automatically provided by Railway services:
- `DATABASE_URL` - MariaDB connection string
- `REDIS_URL` - Redis connection string  
- `RAILWAY_PUBLIC_DOMAIN` - Your app's public domain

## 🛠️ Development Deployment

### 1. Deploy Development Mode

```bash
# Login to Railway
railway login

# Link to your project
railway link

# Set development environment
railway variables set FRAPPE_ENV=development
railway variables set DEVELOPER_MODE=1
railway variables set SITE_NAME=localhost
railway variables set ADMIN_PASSWORD=admin123

# Deploy using development configuration
railway up --dockerfile backend/Dockerfile.dev
```

### 2. Development Features
- **Hot Reload**: File changes trigger automatic reloads
- **Debug Mode**: Enhanced logging and error reporting
- **Development Tools**: IPython, debugger, file watcher
- **Ports**: Web (8000), SocketIO (9000)
- **Bench Commands**: Full access to bench CLI

### 3. Accessing Development Environment

```bash
# Get your Railway domain
railway domain

# Access Frappe Desk
https://your-app.railway.app

# Default credentials
Username: Administrator
Password: admin123 (or your ADMIN_PASSWORD)
```

## 🏭 Production Deployment

### 1. Deploy Production Mode

```bash
# Set production environment
railway variables set FRAPPE_ENV=production
railway variables set DEVELOPER_MODE=0
railway variables set SITE_NAME=mysite
railway variables set ADMIN_PASSWORD=your_secure_password

# Deploy using production configuration
railway up --dockerfile backend/Dockerfile.prod
```

### 2. Production Features
- **Optimized Performance**: Gunicorn with multiple workers
- **Security**: HTTPS enforcement, CSRF protection
- **Monitoring**: Health checks and logging
- **Scalability**: Auto-restart and worker management
- **Asset Optimization**: Minified and compressed assets

### 3. Production Configuration

```bash
# Performance tuning
railway variables set WORKERS=4
railway variables set TIMEOUT=120
railway variables set GUNICORN_WORKERS=4

# Security settings
railway variables set CORS_ORIGIN_WHITELIST=https://yourdomain.com
```

## 🔧 Configuration Files

### File Structure
```
backend/
├── Dockerfile.dev              # Development container
├── Dockerfile.prod             # Production container
├── railway.dev.toml            # Development Railway config
├── railway.prod.toml           # Production Railway config
├── start-dev.sh               # Development startup script
├── start-prod.sh              # Production startup script
├── site_config.json.template  # Site configuration template
├── .railwayignore             # Files to exclude from builds
├── requirements.txt           # Additional Python dependencies
└── RAILWAY_DEPLOYMENT.md      # This documentation
```

### Switching Between Modes

To switch from development to production:

```bash
# Update environment variables
railway variables set FRAPPE_ENV=production
railway variables set DEVELOPER_MODE=0

# Redeploy with production Dockerfile
railway up --dockerfile backend/Dockerfile.prod
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check DATABASE_URL is set
railway variables

# Verify MariaDB service is running
railway status
```

#### 2. Redis Connection Failed
```bash
# Check REDIS_URL is set
railway variables

# Verify Redis service is running
railway status
```

#### 3. Site Creation Failed
```bash
# Check logs
railway logs

# Common causes:
# - Missing ADMIN_PASSWORD
# - Database not ready
# - Incorrect DATABASE_URL format
```

#### 4. Assets Not Loading
```bash
# For production, rebuild assets
railway run bash
bench build --production
```

### Debugging Commands

```bash
# View logs
railway logs --tail

# Connect to container
railway run bash

# Check site status
railway run "bench --site mysite doctor"

# Run migrations
railway run "bench --site mysite migrate"
```

## 📊 Monitoring

### Health Checks
- **Development**: `http://localhost:8000`
- **Production**: `http://localhost:8000/api/method/frappe.utils.change_log.get_versions`

### Log Locations
- Application logs: Railway dashboard
- Frappe logs: `/home/frappe/frappe-bench/logs/`
- Site logs: `/home/frappe/frappe-bench/sites/{site_name}/logs/`

## 🔐 Security Best Practices

### Production Security
1. **Strong Passwords**: Use complex ADMIN_PASSWORD
2. **HTTPS Only**: Railway provides SSL automatically
3. **CORS Configuration**: Set specific origins, not wildcards
4. **Environment Variables**: Never commit secrets to code
5. **Regular Updates**: Keep Frappe/ERPNext updated

### Environment Variables Security
```bash
# Use Railway's secret management
railway variables set ADMIN_PASSWORD=your_secure_password --secret
railway variables set ENCRYPTION_KEY=your_32_char_key --secret
```

## 🚀 Advanced Configuration

### Custom Apps
To install custom Frappe apps:

1. Create a custom Dockerfile extending the base:
```dockerfile
FROM frappe/erpnext:latest
RUN bench get-app your_custom_app https://github.com/your/app.git
```

2. Update startup script to install the app:
```bash
bench --site ${SITE_NAME} install-app your_custom_app
```

### Scaling
Railway automatically handles scaling, but you can optimize:

```bash
# Increase workers for high traffic
railway variables set WORKERS=8
railway variables set GUNICORN_WORKERS=8

# Adjust timeouts
railway variables set TIMEOUT=300
```

### Backup Strategy
```bash
# Manual backup
railway run "bench --site mysite backup"

# Automated backups (add to cron or Railway cron service)
railway run "bench --site mysite backup --with-files"
```

## 📞 Support

### Resources
- [Frappe Documentation](https://frappeframework.com/docs)
- [ERPNext Documentation](https://docs.erpnext.com)
- [Railway Documentation](https://docs.railway.app)

### Getting Help
1. Check Railway logs: `railway logs`
2. Review Frappe logs in the container
3. Use Railway's support channels
4. Frappe community forums

---

## 🎉 Success!

Once deployed, your Frappe/ERPNext instance will be available at your Railway domain. You can access the Desk interface and start building your SaaS platform!

**Default Access:**
- URL: `https://your-app.railway.app`
- Username: `Administrator`
- Password: Your `ADMIN_PASSWORD`

