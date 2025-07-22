#!/bin/bash

# Pre-installation validation script
# Checks system requirements and dependencies before setup

set -e

echo "🔍 Validating System Requirements..."
echo "===================================="

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

# Track validation results
VALIDATION_PASSED=true

# Check operating system
check_os() {
    print_status "Checking operating system..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            print_success "Ubuntu/Debian Linux detected"
        else
            print_warning "Linux detected but not Ubuntu/Debian - some commands may need adjustment"
        fi
    else
        print_error "This script is designed for Ubuntu/Debian Linux"
        VALIDATION_PASSED=false
    fi
}

# Check sudo access
check_sudo() {
    print_status "Checking sudo access..."
    
    if sudo -n true 2>/dev/null; then
        print_success "Sudo access available"
    else
        print_warning "Sudo access required - you may be prompted for password during setup"
    fi
}

# Check system dependencies
check_dependencies() {
    print_status "Checking system dependencies..."
    
    local deps=("python3" "python3-pip" "node" "npm" "git" "curl" "wget")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if command -v "$dep" &> /dev/null; then
            print_success "$dep is installed"
        else
            print_error "$dep is not installed"
            missing_deps+=("$dep")
            VALIDATION_PASSED=false
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_status "Run: sudo apt-get update && sudo apt-get install -y python3-dev python3-pip nodejs npm git curl wget"
    fi
}

# Check Python version
check_python_version() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        local major_version=$(echo $python_version | cut -d'.' -f1)
        local minor_version=$(echo $python_version | cut -d'.' -f2)
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 8 ]; then
            print_success "Python $python_version (compatible)"
        else
            print_error "Python $python_version detected - requires Python 3.8+"
            VALIDATION_PASSED=false
        fi
    fi
}

# Check Node.js version
check_node_version() {
    print_status "Checking Node.js version..."
    
    if command -v node &> /dev/null; then
        local node_version=$(node --version | sed 's/v//')
        local major_version=$(echo $node_version | cut -d'.' -f1)
        
        if [ "$major_version" -ge 18 ]; then
            print_success "Node.js $node_version (compatible)"
        else
            print_error "Node.js $node_version detected - requires Node.js 18+"
            VALIDATION_PASSED=false
        fi
    fi
}

# Check available disk space
check_disk_space() {
    print_status "Checking available disk space..."
    
    local available_space=$(df . | tail -1 | awk '{print $4}')
    local available_gb=$((available_space / 1024 / 1024))
    
    if [ "$available_gb" -ge 5 ]; then
        print_success "Available disk space: ${available_gb}GB"
    else
        print_warning "Available disk space: ${available_gb}GB - recommend at least 5GB"
    fi
}

# Check memory
check_memory() {
    print_status "Checking available memory..."
    
    local total_mem=$(free -m | awk 'NR==2{print $2}')
    local available_mem=$(free -m | awk 'NR==2{print $7}')
    
    if [ "$total_mem" -ge 2048 ]; then
        print_success "Total memory: ${total_mem}MB"
    else
        print_warning "Total memory: ${total_mem}MB - recommend at least 2GB"
    fi
    
    if [ "$available_mem" -ge 1024 ]; then
        print_success "Available memory: ${available_mem}MB"
    else
        print_warning "Available memory: ${available_mem}MB - may need to close other applications"
    fi
}

# Check network connectivity
check_network() {
    print_status "Checking network connectivity..."
    
    if ping -c 1 google.com &> /dev/null; then
        print_success "Internet connectivity available"
    else
        print_error "No internet connectivity - required for downloading dependencies"
        VALIDATION_PASSED=false
    fi
}

# Check if ports are available
check_ports() {
    print_status "Checking port availability..."
    
    local ports=(80 3000 8000 3306 6379)
    
    for port in "${ports[@]}"; do
        if netstat -tuln 2>/dev/null | grep ":$port " &> /dev/null; then
            print_warning "Port $port is in use - may cause conflicts"
        else
            print_success "Port $port is available"
        fi
    done
}

# Check project structure
check_project_structure() {
    print_status "Checking project structure..."
    
    local required_dirs=("backend" "frontend" "nginx" "scripts")
    local required_files=("backend/imperium_pim/hooks.py" "backend/setup.py" "frontend/package.json" "nginx/client-a.conf")
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_success "Directory $dir exists"
        else
            print_error "Directory $dir is missing"
            VALIDATION_PASSED=false
        fi
    done
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "File $file exists"
        else
            print_error "File $file is missing"
            VALIDATION_PASSED=false
        fi
    done
}

# Main validation function
main() {
    print_status "Starting pre-installation validation..."
    echo ""
    
    check_os
    check_sudo
    check_dependencies
    check_python_version
    check_node_version
    check_disk_space
    check_memory
    check_network
    check_ports
    check_project_structure
    
    echo ""
    echo "======================================"
    
    if [ "$VALIDATION_PASSED" = true ]; then
        print_success "✅ All validations passed! Ready to run setup."
        echo ""
        echo "Next steps:"
        echo "1. Run: chmod +x scripts/setup.sh"
        echo "2. Run: ./scripts/setup.sh"
        exit 0
    else
        print_error "❌ Validation failed! Please fix the issues above before running setup."
        exit 1
    fi
}

# Run main function
main "$@"

