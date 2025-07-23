# PIM Experiment - Separate Frontend & Backend Deployment

A Product Information Management (PIM) system with **separate deployment** architecture: Next.js frontend on Vercel and Frappe backend on standard Frappe sites.

## 🏗️ Architecture Overview

This repository contains both frontend and backend code optimized for separate deployment:

- **Frontend**: Next.js application optimized for Vercel deployment
- **Backend**: Clean Frappe app for standard Frappe site installation
- **Integration**: API communication between separate deployments
- **Deployment**: Simplified deployment process for each component

## 🚀 Quick Deployment

**For detailed deployment instructions, see [SEPARATE_DEPLOYMENT.md](SEPARATE_DEPLOYMENT.md)**

### Frontend (Vercel)
1. Connect this GitHub repo to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Backend (Frappe Site)
```bash
bench get-app imperium_pim /path/to/this/repo/backend
bench --site your-site install-app imperium_pim
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

## 🔧 Key Features

- **Separate Deployments**: Frontend and backend deploy independently
- **CORS Configured**: Cross-origin requests properly handled
- **Environment Management**: Separate configs for development and production
- **API Integration**: Frontend communicates with backend via REST API
- **Clean Architecture**: No unnecessary build complexity

## 📖 Documentation

- [SEPARATE_DEPLOYMENT.md](SEPARATE_DEPLOYMENT.md) - Complete deployment guide
- [frontend/README.md](frontend/README.md) - Frontend-specific documentation
- [backend/README.md](backend/README.md) - Backend-specific documentation

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your Vercel domain is configured in the backend CORS settings
2. **API Connection**: Check that `NEXT_PUBLIC_API_BASE_URL` points to your Frappe site
3. **App Installation**: Make sure the backend directory path is correct when using `bench get-app`

### Getting Help

If you encounter issues:
1. Check the deployment guide: [SEPARATE_DEPLOYMENT.md](SEPARATE_DEPLOYMENT.md)
2. Verify environment variables are set correctly
3. Check that both frontend and backend are deployed and accessible

## 🚀 Development

For local development:

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend (in your Frappe bench)
bench --site your-site serve --port 8000
```

The frontend will run on `http://localhost:3000` and connect to your local Frappe backend.

