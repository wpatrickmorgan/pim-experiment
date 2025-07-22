#!/bin/bash

# Post-installation testing script
# Tests that all components are working correctly after setup

set -e

echo "🧪 Testing Installation..."
echo "=========================="

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

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test function wrapper
run_test() {
    local test_name="$1"
    local test_function="$2"
    
    print_status "Testing: $test_name"
    
    if $test_function; then
        print_success "$test_name - PASSED"
        ((TESTS_PASSED++))
    else
        print_error "$test_name - FAILED"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Test backend directory structure
test_backend_structure() {
    [ -d "backend/frappe-bench" ] && \
    [ -d "backend/frappe-bench/apps/imperium_pim" ] && \
    [ -d "backend/frappe-bench/sites/client-a.local" ] && \
    [ -f "backend/frappe-bench/sites/client-a.local/site_config.json" ]
}

# Test frontend build output
test_frontend_build() {
    [ -d "/var/www/client-a-frontend" ] && \
    [ -f "/var/www/client-a-frontend/index.html" ] && \
    [ "$(stat -c %U /var/www/client-a-frontend)" = "www-data" ]
}

# Test nginx configuration
test_nginx_config() {
    [ -f "/etc/nginx/sites-available/client-a.local" ] && \
    [ -L "/etc/nginx/sites-enabled/client-a.local" ] && \
    sudo nginx -t &>/dev/null
}

# Test system services
test_system_services() {
    systemctl is-active --quiet mariadb && \
    systemctl is-active --quiet redis-server && \
    systemctl is-active --quiet nginx
}

# Test database connection
test_database_connection() {
    mysql -u frappe -pfrappe -e "USE \`client-a.local\`; SHOW TABLES;" &>/dev/null
}

# Test hosts file entry
test_hosts_file() {
    grep -q "client-a.localtest.me" /etc/hosts
}

# Test API endpoints (requires backend to be running)
test_api_endpoints() {
    # Check if backend is running
    if ! pgrep -f "bench start" &>/dev/null; then
        print_warning "Backend not running - skipping API tests"
        return 1
    fi
    
    # Test ping endpoint
    local response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/api/method/imperium_pim.api.ping" 2>/dev/null || echo "000")
    [ "$response" = "200" ]
}

# Test frontend accessibility
test_frontend_access() {
    # Test nginx serving static files
    local response=$(curl -s -o /dev/null -w "%{http_code}" "http://client-a.localtest.me" 2>/dev/null || echo "000")
    [ "$response" = "200" ]
}

# Test file permissions
test_file_permissions() {
    # Check backend permissions
    [ -r "backend/frappe-bench/sites/client-a.local/site_config.json" ] && \
    # Check frontend permissions
    [ -r "/var/www/client-a-frontend/index.html" ] && \
    # Check nginx config permissions
    [ -r "/etc/nginx/sites-available/client-a.local" ]
}

# Test Frappe app installation
test_frappe_app() {
    if [ -d "backend/frappe-bench" ]; then
        cd backend/frappe-bench
        # Check if app is installed
        bench --site client-a.local list-apps | grep -q "imperium_pim"
        local result=$?
        cd ../..
        return $result
    else
        return 1
    fi
}

# Generate test report
generate_report() {
    echo "======================================"
    echo "📊 Test Results Summary"
    echo "======================================"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "🎉 All tests passed! Installation is working correctly."
        echo ""
        echo "🚀 Next Steps:"
        echo "1. Start backend: ./scripts/start_backend.sh"
        echo "2. Visit: http://client-a.localtest.me"
        echo "3. Test API: http://client-a.localtest.me/api/method/imperium_pim.api.ping"
        echo ""
        echo "🔐 Default Credentials:"
        echo "Username: Administrator"
        echo "Password: admin"
        return 0
    else
        print_error "❌ Some tests failed. Please check the issues above."
        echo ""
        echo "🔧 Troubleshooting:"
        echo "1. Check system services: sudo systemctl status mariadb redis-server nginx"
        echo "2. Check nginx logs: sudo tail -f /var/log/nginx/error.log"
        echo "3. Check backend logs: cd backend/frappe-bench && bench logs"
        return 1
    fi
}

# Main testing function
main() {
    print_status "Starting post-installation tests..."
    echo ""
    
    # Run all tests
    run_test "Backend Directory Structure" test_backend_structure
    run_test "Frontend Build Output" test_frontend_build
    run_test "Nginx Configuration" test_nginx_config
    run_test "System Services" test_system_services
    run_test "Database Connection" test_database_connection
    run_test "Hosts File Entry" test_hosts_file
    run_test "File Permissions" test_file_permissions
    run_test "Frappe App Installation" test_frappe_app
    run_test "Frontend Accessibility" test_frontend_access
    run_test "API Endpoints" test_api_endpoints
    
    # Generate final report
    generate_report
}

# Run main function
main "$@"

