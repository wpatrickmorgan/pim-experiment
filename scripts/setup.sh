#!/bin/bash

# PIM Experiment Monorepo Setup Script
# This script sets up the complete decoupled Frappe + Next.js environment

set -e  # Exit on any error

echo "🚀 Starting PIM Experiment Monorepo Setup..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root for nginx setup
check_sudo() {
    if ! sudo -n true 2>/dev/null; then
        print_warning "This script requires sudo access for nginx configuration"
        print_warning "You may be prompted for your password"
    fi
}

# Install system dependencies
install_dependencies() {
    print_status "Installing system dependencies..."
    
    # Update package list
    sudo apt-get update -qq
    
    # Install required packages
    sudo apt-get install -y \
        python3-dev \
        python3-pip \
        python3-venv \
        nodejs \
        npm \
        nginx \
        git \
        curl \
        wget \
        mariadb-server \
        mariadb-client \
        redis-server \
        wkhtmltopdf
    
    print_success "System dependencies installed"
}

# Setup Frappe Backend
setup_backend() {
    print_status "Setting up Frappe backend..."
    
    # Install bench if not already installed
    if ! command -v bench &> /dev/null; then
        print_status "Installing Frappe Bench..."
        pip3 install frappe-bench
    fi
    
    # Create bench directory if it doesn't exist
    if [ ! -d "backend/frappe-bench" ]; then
        print_status "Initializing frappe-bench..."
        mkdir -p backend
        cd backend
        bench init --skip-assets --frappe-branch version-15 frappe-bench
        cd frappe-bench
    else
        print_status "Using existing frappe-bench..."
        cd backend/frappe-bench
    fi
    
    # Copy our imperium_pim app into the bench apps directory
    print_status "Installing imperium_pim app..."
    if [ -d "apps/imperium_pim" ]; then
        rm -rf apps/imperium_pim
    fi
    cp -r ../../backend/imperium_pim apps/
    
    # Setup MariaDB if needed
    print_status "Configuring MariaDB..."
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS \`client-a.local\`;" 2>/dev/null || true
    sudo mysql -e "CREATE USER IF NOT EXISTS 'frappe'@'localhost' IDENTIFIED BY 'frappe';" 2>/dev/null || true
    sudo mysql -e "GRANT ALL PRIVILEGES ON \`client-a.local\`.* TO 'frappe'@'localhost';" 2>/dev/null || true
    sudo mysql -e "FLUSH PRIVILEGES;" 2>/dev/null || true
    
    # Create new site if it doesn't exist
    if [ ! -d "sites/client-a.local" ]; then
        print_status "Creating new site: client-a.local..."
        bench new-site client-a.local --admin-password admin --db-name "client-a.local" --db-user frappe --db-password frappe
    else
        print_status "Site client-a.local already exists"
    fi
    
    # Install app on site
    print_status "Installing imperium_pim app on site..."
    bench --site client-a.local install-app imperium_pim
    
    # Configure site for API access
    print_status "Configuring site for API access..."
    cat > sites/client-a.local/site_config.json << EOF
{
    "allow_cors": true,
    "cors_headers": ["Content-Type", "Authorization", "X-Frappe-CSRF-Token"],
    "cors_origins": ["http://client-a.localtest.me", "http://localhost:3000"],
    "allow_guest_to_upload_files": false,
    "disable_website_cache": true
}
EOF
    
    # Build assets
    print_status "Building Frappe assets..."
    bench build --app imperium_pim
    
    # Set proper permissions
    print_status "Setting proper permissions..."
    sudo chown -R $(whoami):$(whoami) .
    
    cd ../..
    print_success "Backend setup completed"
}

# Setup Next.js Frontend
setup_frontend() {
    print_status "Setting up Next.js frontend..."
    
    print_status "Frontend files already available in frontend/ directory..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Create environment file
    print_status "Creating frontend environment configuration..."
    cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://client-a.localtest.me/api
NEXT_PUBLIC_FILES_BASE_URL=http://client-a.localtest.me/files
NEXT_PUBLIC_ASSETS_BASE_URL=http://client-a.localtest.me/assets
EOF
    
    # Build and export frontend
    print_status "Building Next.js application..."
    npm run build
    
    # Create web directory and copy static files
    print_status "Deploying static files..."
    sudo mkdir -p /var/www/client-a-frontend
    
    # Copy the exported static files
    if [ -d "out" ]; then
        print_status "Using static export output..."
        sudo cp -r out/* /var/www/client-a-frontend/
    else
        print_warning "No static export found, copying build output..."
        # Create basic index.html for SPA
        sudo mkdir -p /var/www/client-a-frontend
        cat > /tmp/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PIM Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div id="__next">
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: system-ui;">
            <div>Loading PIM Dashboard...</div>
        </div>
    </div>
    <script>
        // Redirect to development server for now
        if (window.location.hostname === 'client-a.localtest.me') {
            window.location.href = 'http://localhost:3000';
        }
    </script>
</body>
</html>
EOF
        sudo cp /tmp/index.html /var/www/client-a-frontend/
        rm /tmp/index.html
    fi
    
    # Set proper permissions
    sudo chown -R www-data:www-data /var/www/client-a-frontend
    sudo chmod -R 755 /var/www/client-a-frontend
    
    cd ..
    print_success "Frontend setup completed"
}

# Setup Nginx
setup_nginx() {
    print_status "Setting up Nginx configuration..."
    
    # Copy nginx config
    sudo cp nginx/client-a.conf /etc/nginx/sites-available/client-a.local
    
    # Enable site
    sudo ln -sf /etc/nginx/sites-available/client-a.local /etc/nginx/sites-enabled/
    
    # Remove default site if it exists
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    if sudo nginx -t; then
        print_success "Nginx configuration is valid"
        sudo systemctl reload nginx
    else
        print_error "Nginx configuration is invalid"
        exit 1
    fi
    
    print_success "Nginx setup completed"
}

# Setup hosts file
setup_hosts() {
    print_status "Setting up hosts file..."
    
    # Add entry to hosts file if it doesn't exist
    if ! grep -q "client-a.localtest.me" /etc/hosts; then
        echo "127.0.0.1 client-a.localtest.me" | sudo tee -a /etc/hosts
        print_success "Added client-a.localtest.me to hosts file"
    else
        print_warning "client-a.localtest.me already exists in hosts file"
    fi
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start MariaDB
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    
    # Start Redis
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Start Nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    
    print_success "Services started"
}

# Verify API endpoints
verify_api_endpoints() {
    print_status "Verifying API endpoints..."
    
    # Check if API endpoints exist in the app
    if [ -f "backend/imperium_pim/api.py" ]; then
        print_success "API endpoints found in imperium_pim app"
    else
        print_error "API endpoints not found! Please check backend/imperium_pim/api.py"
        exit 1
    fi
}

# Main execution
main() {
    print_status "Starting setup process..."
    
    # Check sudo access
    check_sudo
    
    # Install dependencies
    install_dependencies
    
    # Setup backend
    setup_backend
    
    # Setup frontend  
    setup_frontend
    
    # Verify API endpoints
    verify_api_endpoints
    
    # Setup nginx
    setup_nginx
    
    # Setup hosts
    setup_hosts
    
    # Start services
    start_services
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "================================================"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Start the backend: ./scripts/start_backend.sh"
    echo "2. Visit: http://client-a.localtest.me"
    echo "3. Test API: http://client-a.localtest.me/api/method/imperium_pim.api.ping"
    echo ""
    echo "🔐 Default Credentials:"
    echo "Username: Administrator"
    echo "Password: admin"
    echo ""
    echo "📁 Project Structure:"
    echo "├── backend/     (Frappe backend)"
    echo "├── frontend/    (Next.js frontend)"
    echo "├── nginx/       (Nginx configuration)"
    echo "└── scripts/     (Utility scripts)"
    echo ""
}

# Run main function
main "$@"
