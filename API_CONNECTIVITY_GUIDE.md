# API Connectivity Guide

This guide helps you set up and troubleshoot API connectivity between the Next.js frontend and Frappe backend.

## Quick Diagnosis

Visit `/api-test` on your deployed frontend to run comprehensive API connectivity tests.

## Configuration Steps

### 1. Frontend Configuration

Update your environment variables:

**For Production (Vercel):**
```bash
# In Vercel dashboard or .env.production
NEXT_PUBLIC_API_BASE_URL=https://your-frappe-site.com/api
DEPLOYMENT_MODE=separate
```

**For Local Development:**
```bash
# In .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
DEPLOYMENT_MODE=separate
```

### 2. Backend Configuration (Frappe)

The backend includes CORS handling, but you need to configure it for your frontend domain:

```python
# In Frappe console or custom script
from imperium_pim.utils import setup_cors_for_site

# Configure CORS for your frontend URLs
setup_cors_for_site([
    "https://your-vercel-app.vercel.app",  # Your Vercel domain
    "http://localhost:3000"  # Local development
])
```

### 3. Available API Endpoints

The backend exposes these endpoints:

- **Ping/Health Check:**
  - `GET /api/method/imperium_pim.api.ping.ping` (guest access)
  - `GET /api/method/imperium_pim.api.ping.health_check` (authenticated)

- **Dashboard:**
  - `GET /api/method/imperium_pim.api.dashboard.get_dashboard_stats`
  - `GET /api/method/imperium_pim.api.dashboard.get_recent_items`
  - `GET /api/method/imperium_pim.api.dashboard.get_recent_vendors`

- **Items:**
  - `GET /api/method/imperium_pim.api.items.get_item_list`
  - `GET /api/method/imperium_pim.api.items.get_item_details`
  - `GET /api/method/imperium_pim.api.items.get_items_by_status`
  - `GET /api/method/imperium_pim.api.items.get_items_by_brand`

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure your frontend domain is added to CORS origins
   - Check browser console for specific CORS error messages
   - Verify the backend is returning proper CORS headers

2. **404 Not Found**
   - Check if the Frappe site is running
   - Verify the API endpoint paths are correct
   - Ensure the Imperium PIM app is installed in Frappe

3. **Network Errors**
   - Verify the backend URL is accessible from your deployment environment
   - Check if the backend server is running
   - Test the backend URL directly in a browser

4. **Authentication Issues**
   - Some endpoints require authentication
   - Check if session cookies are being sent correctly
   - Verify CSRF token handling if required

### Testing Backend Directly

Test your backend endpoints directly:

```bash
# Test ping endpoint (no auth required)
curl https://your-frappe-site.com/api/method/imperium_pim.api.ping.ping

# Test with authentication
curl -X POST https://your-frappe-site.com/api/method/login \
  -H "Content-Type: application/json" \
  -d '{"usr": "your-username", "pwd": "your-password"}'
```

### Frontend Testing

1. Visit `/api-test` on your deployed frontend
2. Run the API connectivity tests
3. Check browser developer tools for network requests
4. Review console logs for detailed error information

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL for API calls | `https://your-site.com/api` |
| `NEXT_PUBLIC_BACKEND_URL` | Backend URL (optional) | `https://your-site.com` |
| `DEPLOYMENT_MODE` | Deployment mode | `separate` |

## Architecture Overview

```
Frontend (Vercel)     Backend (Frappe)
┌─────────────────┐   ┌──────────────────┐
│ Next.js App     │   │ Frappe Site      │
│                 │   │                  │
│ API Client ────────→│ API Endpoints    │
│ (CORS requests) │   │ (CORS enabled)   │
│                 │   │                  │
│ /api-test       │   │ /api/method/...  │
└─────────────────┘   └──────────────────┘
```

The frontend makes cross-origin requests to the Frappe backend, which handles CORS and returns JSON responses.
