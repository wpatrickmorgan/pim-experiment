# Frontend - Next.js PIM Application

This directory contains the Next.js frontend for the PIM system.

## Structure

After running `./scripts/setup.sh`, this directory will contain the complete Next.js application cloned from the `pim-experiment-frontend` repository.

Expected structure:
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and API clients
│   └── styles/              # CSS and styling
├── public/                  # Static assets
├── package.json             # Dependencies
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── .env.local               # Environment variables
```

## Setup

The frontend is automatically set up by the main setup script:

```bash
# From project root
./scripts/setup.sh
```

## Manual Setup (if needed)

```bash
# Clone frontend repository
git clone https://github.com/wpatrickmorgan/pim-experiment-frontend.git temp_frontend
mv temp_frontend/* frontend/
rm -rf temp_frontend

cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://client-a.localtest.me/api
NEXT_PUBLIC_FILES_BASE_URL=http://client-a.localtest.me/files
NEXT_PUBLIC_ASSETS_BASE_URL=http://client-a.localtest.me/assets
EOF

# Build application
npm run build
```

## Development

### Development Server

```bash
cd frontend
npm run dev
# Visit http://localhost:3000
```

### Production Build

```bash
# From project root
./scripts/build_frontend.sh

# Or manually
cd frontend
npm run build
npm run export  # If using static export
```

## API Integration

The frontend communicates with the Frappe backend through the Nginx proxy:

```javascript
// API calls go through the proxy
const response = await fetch('/api/method/imperium_pim.api.get_dashboard_stats');
const data = await response.json();
```

## Environment Variables

Key environment variables in `.env.local`:

- `NEXT_PUBLIC_API_BASE_URL` - Backend API endpoint
- `NEXT_PUBLIC_FILES_BASE_URL` - File upload/download endpoint  
- `NEXT_PUBLIC_ASSETS_BASE_URL` - Static assets endpoint

## Deployment

The frontend is deployed as static files served by Nginx:

1. Build the application: `npm run build`
2. Export static files: `npm run export` (if available)
3. Copy to web directory: `/var/www/client-a-frontend`
4. Nginx serves the files at `http://client-a.localtest.me`

## Available Scripts

- `npm run dev` - Development server
- `npm run build` - Production build
- `npm run export` - Static export (if configured)
- `npm run lint` - Code linting
- `npm run type-check` - TypeScript checking

