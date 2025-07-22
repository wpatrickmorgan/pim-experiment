# Backend - Frappe PIM System

This directory contains the Frappe backend for the PIM system.

## Structure

After running `./scripts/setup.sh`, this directory will contain:

```
backend/
├── apps/
│   ├── frappe/              # Frappe framework
│   └── imperium_pim/        # PIM application (cloned from imperium-pim repo)
├── sites/
│   └── client-a.local/      # Site configuration
├── config/                  # Bench configuration
├── logs/                    # Application logs
└── ...                      # Other bench files
```

## Setup

The backend is automatically set up by the main setup script:

```bash
# From project root
./scripts/setup.sh
```

## Manual Setup (if needed)

```bash
cd backend

# Initialize bench
bench init --skip-assets --frappe-branch version-15 .

# Get PIM app
bench get-app imperium_pim https://github.com/wpatrickmorgan/imperium-pim.git

# Create site
bench new-site client-a.local --no-mariadb-socket --admin-password admin

# Install app
bench --site client-a.local install-app imperium_pim

# Enable CORS
echo '{"allow_cors": true}' > sites/client-a.local/site_config.json

# Build assets
bench build --app imperium_pim
```

## Starting the Backend

```bash
# From project root
./scripts/start_backend.sh

# Or manually from this directory
bench start
```

## API Endpoints

The backend provides REST API endpoints at:
- Base URL: `http://localhost:8000/api/method/`
- Through proxy: `http://client-a.localtest.me/api/method/`

### Available Endpoints

- `imperium_pim.api.ping` - Test connectivity
- `imperium_pim.api.get_dashboard_stats` - Dashboard statistics
- Standard Frappe endpoints (login, logout, etc.)

## Development

- Add new API endpoints in `apps/imperium_pim/imperium_pim/api.py`
- Restart backend after changes: `bench restart`
- View logs: `tail -f logs/bench.log`

