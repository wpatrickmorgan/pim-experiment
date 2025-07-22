#!/bin/bash

# Complete Deployment Script for PIM Platform
# This script builds frontend, starts backend, and deploys everything

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend/frappe-bench"
NGINX_DIR="$PROJECT_ROOT/nginx"

# Deployment configuration
FRONTEND_DEPLOY_PATH="/var/www/client-a-frontend"
NGINX_CONFIG_SOURCE="$NGINX_DIR/client-a.conf"
NGINX_CONFIG_TARGET="/etc/nginx/sites-available/client-a.conf"
NGINX_CONFIG_ENABLED="/etc/nginx/sites-enabled/client-a.conf"

echo -e "${PURPLE}🚀 Starting Complete PIM Platform Deployment...${NC}"
echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"

# Function to check if running as root for nginx operations
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Some operations require sudo privileges${NC}"
        echo -e "${BLUE}💡 You may be prompted for your password${NC}"
    fi
}

# Function to validate prerequisites
validate_prerequisites() {
    echo -e "${BLUE}🔍 Validating prerequisites...${NC}"
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js is not installed${NC}"
        exit 1
    fi
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm is not installed${NC}"
        exit 1
    fi
    
    # Check if nginx is installed
    if ! command -v nginx &> /dev/null; then
        echo -e "${YELLOW}⚠️  nginx is not installed. Install it with: sudo apt install nginx${NC}"
    fi
    
    echo -e "${GREEN}✅ Prerequisites validated${NC}"
}

# Function to build frontend
build_frontend() {
    echo -e "${YELLOW}🏗️  Step 1: Building frontend...${NC}"
    
    if [ -x "$SCRIPT_DIR/build_frontend.sh" ]; then
        "$SCRIPT_DIR/build_frontend.sh"
    else
        echo -e "${RED}❌ build_frontend.sh not found or not executable${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Frontend build completed${NC}"
}

# Function to deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}📦 Step 2: Deploying frontend...${NC}"
    
    # Check if build output exists
    if [ ! -d "$FRONTEND_DIR/out" ]; then
        echo -e "${RED}❌ Frontend build output not found. Run build first.${NC}"
        exit 1
    fi
    
    # Create deployment directory
    echo -e "${BLUE}📁 Creating deployment directory: $FRONTEND_DEPLOY_PATH${NC}"
    sudo mkdir -p "$FRONTEND_DEPLOY_PATH"
    
    # Copy files
    echo -e "${BLUE}📋 Copying frontend files...${NC}"
    sudo cp -r "$FRONTEND_DIR/out/"* "$FRONTEND_DEPLOY_PATH/"
    
    # Set proper permissions
    sudo chown -R www-data:www-data "$FRONTEND_DEPLOY_PATH"
    sudo chmod -R 755 "$FRONTEND_DEPLOY_PATH"
    
    echo -e "${GREEN}✅ Frontend deployed to $FRONTEND_DEPLOY_PATH${NC}"
}

# Function to configure nginx
configure_nginx() {
    echo -e "${YELLOW}🔧 Step 3: Configuring nginx...${NC}"
    
    # Check if nginx config exists
    if [ ! -f "$NGINX_CONFIG_SOURCE" ]; then
        echo -e "${RED}❌ Nginx config not found: $NGINX_CONFIG_SOURCE${NC}"
        exit 1
    fi
    
    # Copy nginx configuration
    echo -e "${BLUE}📋 Installing nginx configuration...${NC}"
    sudo cp "$NGINX_CONFIG_SOURCE" "$NGINX_CONFIG_TARGET"
    
    # Enable the site
    if [ ! -L "$NGINX_CONFIG_ENABLED" ]; then
        sudo ln -s "$NGINX_CONFIG_TARGET" "$NGINX_CONFIG_ENABLED"
        echo -e "${GREEN}✅ Nginx site enabled${NC}"
    else
        echo -e "${BLUE}ℹ️  Nginx site already enabled${NC}"
    fi
    
    # Test nginx configuration
    echo -e "${BLUE}🧪 Testing nginx configuration...${NC}"
    if sudo nginx -t; then
        echo -e "${GREEN}✅ Nginx configuration is valid${NC}"
    else
        echo -e "${RED}❌ Nginx configuration has errors${NC}"
        exit 1
    fi
    
    # Reload nginx
    echo -e "${BLUE}🔄 Reloading nginx...${NC}"
    sudo nginx -s reload
    
    echo -e "${GREEN}✅ Nginx configured and reloaded${NC}"
}

# Function to start backend
start_backend() {
    echo -e "${YELLOW}⚙️  Step 4: Starting backend...${NC}"
    
    if [ -x "$SCRIPT_DIR/start_backend.sh" ]; then
        "$SCRIPT_DIR/start_backend.sh"
    else
        echo -e "${RED}❌ start_backend.sh not found or not executable${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Backend startup completed${NC}"
}

# Function to verify deployment
verify_deployment() {
    echo -e "${YELLOW}🔍 Step 5: Verifying deployment...${NC}"
    
    # Check if frontend files are deployed
    if [ -f "$FRONTEND_DEPLOY_PATH/index.html" ]; then
        echo -e "${GREEN}✅ Frontend files deployed successfully${NC}"
    else
        echo -e "${RED}❌ Frontend deployment verification failed${NC}"
    fi
    
    # Check nginx status
    if sudo nginx -t &> /dev/null; then
        echo -e "${GREEN}✅ Nginx configuration is valid${NC}"
    else
        echo -e "${RED}❌ Nginx configuration has issues${NC}"
    fi
    
    # Test API connectivity (if backend is running)
    echo -e "${BLUE}🌐 Testing API connectivity...${NC}"
    sleep 2  # Give backend time to start
    
    if curl -s http://localhost:8000/api/method/imperium_pim.api.ping &> /dev/null; then
        echo -e "${GREEN}✅ Backend API is responding${NC}"
    else
        echo -e "${YELLOW}⚠️  Backend API not responding (may still be starting up)${NC}"
    fi
}

# Function to display deployment summary
show_summary() {
    echo -e "${PURPLE}🎉 Deployment Summary${NC}"
    echo -e "${BLUE}===================${NC}"
    echo -e "${GREEN}✅ Frontend: Built and deployed to $FRONTEND_DEPLOY_PATH${NC}"
    echo -e "${GREEN}✅ Backend: Started (should be running on http://localhost:8000)${NC}"
    echo -e "${GREEN}✅ Nginx: Configured and running${NC}"
    echo ""
    echo -e "${BLUE}🌐 Access URLs:${NC}"
    echo -e "${GREEN}   Frontend: http://client-a.localtest.me${NC}"
    echo -e "${GREEN}   API Test: http://client-a.localtest.me/api/method/imperium_pim.api.ping${NC}"
    echo ""
    echo -e "${BLUE}📝 Next Steps:${NC}"
    echo -e "${YELLOW}   1. Add to /etc/hosts: 127.0.0.1 client-a.localtest.me${NC}"
    echo -e "${YELLOW}   2. Test the frontend at http://client-a.localtest.me${NC}"
    echo -e "${YELLOW}   3. Test the API at http://client-a.localtest.me/api/method/imperium_pim.api.ping${NC}"
    echo ""
    echo -e "${BLUE}🔧 Useful Commands:${NC}"
    echo -e "${YELLOW}   - View nginx logs: sudo tail -f /var/log/nginx/client-a-access.log${NC}"
    echo -e "${YELLOW}   - View backend logs: tail -f $BACKEND_DIR/bench.log${NC}"
    echo -e "${YELLOW}   - Restart nginx: sudo nginx -s reload${NC}"
}

# Main execution
main() {
    check_sudo
    validate_prerequisites
    
    # Parse command line arguments
    SKIP_BACKEND=false
    SKIP_FRONTEND=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-backend)
                SKIP_BACKEND=true
                shift
                ;;
            --skip-frontend)
                SKIP_FRONTEND=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --skip-backend    Skip backend startup"
                echo "  --skip-frontend   Skip frontend build and deployment"
                echo "  --help, -h        Show this help message"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Execute deployment steps
    if [ "$SKIP_FRONTEND" = false ]; then
        build_frontend
        deploy_frontend
        configure_nginx
    else
        echo -e "${YELLOW}⏭️  Skipping frontend build and deployment${NC}"
    fi
    
    if [ "$SKIP_BACKEND" = false ]; then
        start_backend
    else
        echo -e "${YELLOW}⏭️  Skipping backend startup${NC}"
    fi
    
    verify_deployment
    show_summary
    
    echo -e "${PURPLE}🚀 Complete deployment finished successfully!${NC}"
}

# Run main function with all arguments
main "$@"

