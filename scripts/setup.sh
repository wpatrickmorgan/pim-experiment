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
    
    cd backend
    
    # Install bench if not already installed
    if ! command -v bench &> /dev/null; then
        print_status "Installing Frappe Bench..."
        pip3 install frappe-bench
    fi
    
    # Initialize frappe-bench
    print_status "Initializing frappe-bench..."
    bench init --skip-assets --frappe-branch version-15 .
    
    # Get imperium_pim app
    print_status "Cloning imperium_pim app..."
    bench get-app imperium_pim https://github.com/wpatrickmorgan/imperium-pim.git
    
    # Create new site
    print_status "Creating new site: client-a.local..."
    bench new-site client-a.local --no-mariadb-socket --admin-password admin
    
    # Install app on site
    print_status "Installing imperium_pim app on site..."
    bench --site client-a.local install-app imperium_pim
    
    # Enable CORS
    print_status "Enabling CORS..."
    echo '{"allow_cors": true, "cors_headers": ["Content-Type", "Authorization"]}' > sites/client-a.local/site_config.json
    
    # Build assets
    print_status "Building Frappe assets..."
    bench build --app imperium_pim
    
    cd ..
    print_success "Backend setup completed"
}

# Setup Next.js Frontend
setup_frontend() {
    print_status "Setting up Next.js frontend..."
    
    # Clone frontend repo
    print_status "Cloning pim-experiment-frontend repo..."
    if [ -d "frontend/.git" ]; then
        rm -rf frontend/*
        rm -rf frontend/.*
    fi
    
    git clone https://github.com/wpatrickmorgan/pim-experiment-frontend.git temp_frontend
    mv temp_frontend/* frontend/ 2>/dev/null || true
    mv temp_frontend/.* frontend/ 2>/dev/null || true
    rm -rf temp_frontend
    
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
    
    # Build frontend
    print_status "Building Next.js application..."
    npm run build
    
    # Export static files (if using static export)
    if npm run export 2>/dev/null; then
        print_status "Exporting static files..."
        # Create web directory
        sudo mkdir -p /var/www/client-a-frontend
        sudo cp -r out/* /var/www/client-a-frontend/
        sudo chown -R www-data:www-data /var/www/client-a-frontend
    else
        print_warning "Static export not available, using build output"
        sudo mkdir -p /var/www/client-a-frontend
        sudo cp -r .next/static /var/www/client-a-frontend/_next/
        sudo cp -r public/* /var/www/client-a-frontend/
        sudo chown -R www-data:www-data /var/www/client-a-frontend
    fi
    
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

# Create test API endpoint
create_test_api() {
    print_status "Creating test API endpoint..."
    
    # Create api.py file in imperium_pim app
    cat > backend/apps/imperium_pim/imperium_pim/api.py << 'EOF'
import frappe

@frappe.whitelist(allow_guest=True)
def ping():
    """Test API endpoint to verify backend connectivity"""
    return {
        "status": "success",
        "message": "PIM Backend is running!",
        "timestamp": frappe.utils.now(),
        "site": frappe.local.site
    }

@frappe.whitelist()
def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_products": 150,
        "total_categories": 25,
        "low_stock_items": 8,
        "pending_orders": 12
    }
EOF
    
    print_success "Test API endpoint created"
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
    
    # Create test API
    create_test_api
    
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

