# Deployment Setup Guide

This guide will help you deploy the PIM Experiment app with separate frontend and backend servers.

## 🏗️ Architecture Overview

- **Frontend**: Next.js app deployed on Vercel
- **Backend**: Frappe/ERPNext app running on your server
- **Communication**: REST API with CORS configuration

## 🚀 Quick Setup

### 1. Backend CORS Configuration

Your backend already has CORS handling built-in! Just run this script on your Frappe server:

```bash
cd /path/to/your/frappe-bench/sites/your-site
python /path/to/backend/setup_cors.py
```

Or manually add to your `site_config.json`:

```json
{
  "allow_cors": "*",
  "cors_origins": [
    "https://your-vercel-app.vercel.app",
    "http://localhost:3000"
  ],
  "cors_headers": [
    "Authorization",
    "Content-Type",
    "X-Requested-With",
    "Accept",
    "Origin",
    "Cache-Control",
    "X-Frappe-CSRF-Token",
    "X-Frappe-CMD"
  ],
  "allow_cors_credentials": true,
  "session_cookie_samesite": "None",
  "session_cookie_secure": true,
  "csrf_cookie_samesite": "None",
  "csrf_cookie_secure": true
}
```

Then restart your Frappe server:
```bash
bench restart
```

### 2. Frontend Environment Variables

In your Vercel deployment, set:

```
NEXT_PUBLIC_API_BASE_URL=http://138.197.71.50:8000/api
DEPLOYMENT_MODE=separate
```

### 3. Test the Connection

Visit your deployed frontend and check:
- Dashboard loads without "Backend connection failed" errors
- API calls work in the browser console
- No CORS errors in the network tab

## 🔧 Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure your `site_config.json` includes your Vercel domain
2. **404 API Errors**: Verify your API base URL is correct
3. **SSL Issues**: Use HTTPS for production deployments

### Debug Steps:

1. Test API directly: `curl http://138.197.71.50:8000/api/method/imperium_pim.api.ping.ping`
2. Check browser network tab for specific error messages
3. Verify Frappe server logs for CORS-related errors

## 📁 File Structure

```
pim-experiment/
├── frontend/           # Next.js frontend (deploy to Vercel)
│   ├── src/
│   │   ├── lib/api.ts  # API client with CORS handling
│   │   └── ...
│   └── package.json
├── backend/            # Frappe backend (deploy to your server)
│   ├── imperium_pim/
│   │   ├── api/        # API endpoints
│   │   ├── utils.py    # CORS handling functions
│   │   └── hooks.py    # CORS hooks configuration
│   └── setup_cors.py   # CORS configuration script
└── DEPLOYMENT_SETUP.md # This file
```

## 🌐 API Endpoints

Your backend exposes these endpoints:

- `GET /api/method/imperium_pim.api.ping.ping` - Health check
- `GET /api/method/imperium_pim.api.dashboard.get_stats` - Dashboard stats
- `GET /api/method/imperium_pim.api.items.get_items` - Get items list

All endpoints are configured with proper CORS headers automatically.

## ✅ Verification Checklist

- [ ] Backend CORS is configured in `site_config.json`
- [ ] Frappe server has been restarted
- [ ] Frontend environment variables are set in Vercel
- [ ] Frontend builds successfully on Vercel
- [ ] API calls work without CORS errors
- [ ] Dashboard loads with real data from backend

## 🆘 Need Help?

If you're still seeing connection errors:

1. Check your Frappe server logs: `tail -f /path/to/frappe-bench/logs/web.log`
2. Test API endpoints directly with curl or Postman
3. Verify your Vercel environment variables are deployed
4. Make sure your backend server is accessible from the internet

The backend already has comprehensive CORS handling built-in - you just need to configure it for your specific frontend domain!
