#!/bin/bash

# Backend Start Script for PIM Platform
# This script starts the Frappe backend using bench

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend/frappe-bench"

echo -e "${GREEN}🚀 Starting PIM Backend...${NC}"

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}❌ Backend directory not found: $BACKEND_DIR${NC}"
    echo -e "${YELLOW}💡 Make sure you have set up the Frappe bench in the backend directory${NC}"
    exit 1
fi

cd "$BACKEND_DIR"

# Check if this is a valid Frappe bench
if [ ! -f "sites/common_site_config.json" ]; then
    echo -e "${RED}❌ This doesn't appear to be a valid Frappe bench${NC}"
    echo -e "${YELLOW}💡 Please set up a Frappe bench in: $BACKEND_DIR${NC}"
    exit 1
fi

# Check if the site exists
SITE_NAME="my-site"
if [ ! -d "sites/$SITE_NAME" ]; then
    echo -e "${YELLOW}⚠️  Site '$SITE_NAME' not found. Available sites:${NC}"
    ls -la sites/ | grep "^d" | grep -v "\.\." | awk '{print "  - " $9}' | grep -v "^  - $"
    echo -e "${YELLOW}💡 You may need to create the site or update the SITE_NAME variable${NC}"
fi

# Function to check if bench is already running
check_bench_status() {
    if pgrep -f "bench.*start" > /dev/null; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to start bench
start_bench() {
    echo -e "${YELLOW}🔧 Starting Frappe bench...${NC}"
    
    # Start bench in background
    nohup bench start > bench.log 2>&1 &
    BENCH_PID=$!
    
    echo -e "${BLUE}📝 Bench started with PID: $BENCH_PID${NC}"
    echo -e "${BLUE}📋 Logs are being written to: $BACKEND_DIR/bench.log${NC}"
    
    # Wait a moment for startup
    sleep 3
    
    # Check if bench is still running
    if kill -0 $BENCH_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Bench is running successfully!${NC}"
        echo -e "${GREEN}🌐 Backend should be available at: http://localhost:8000${NC}"
        echo -e "${BLUE}📊 To monitor logs: tail -f $BACKEND_DIR/bench.log${NC}"
        echo -e "${BLUE}🛑 To stop: kill $BENCH_PID${NC}"
    else
        echo -e "${RED}❌ Bench failed to start. Check the logs:${NC}"
        tail -n 20 bench.log
        exit 1
    fi
}

# Function to start with supervisor (alternative)
start_with_supervisor() {
    echo -e "${YELLOW}🔧 Starting Frappe with supervisor...${NC}"
    
    if command -v supervisorctl &> /dev/null; then
        bench setup supervisor
        sudo supervisorctl reread
        sudo supervisorctl update
        sudo supervisorctl start all
        echo -e "${GREEN}✅ Frappe started with supervisor!${NC}"
    else
        echo -e "${RED}❌ Supervisor not found. Using bench start instead...${NC}"
        start_bench
    fi
}

# Main execution
echo -e "${BLUE}🔍 Checking current bench status...${NC}"

if check_bench_status; then
    echo -e "${YELLOW}⚠️  Bench appears to be already running${NC}"
    echo -e "${BLUE}💡 Current bench processes:${NC}"
    pgrep -f "bench.*start" -l || true
    
    read -p "Do you want to restart the bench? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🔄 Stopping existing bench processes...${NC}"
        pkill -f "bench.*start" || true
        sleep 2
        start_bench
    else
        echo -e "${GREEN}✅ Keeping existing bench running${NC}"
        echo -e "${GREEN}🌐 Backend should be available at: http://localhost:8000${NC}"
    fi
else
    # Check if user wants to use supervisor
    if [ "$1" = "--supervisor" ] || [ "$1" = "-s" ]; then
        start_with_supervisor
    else
        start_bench
    fi
fi

echo -e "${GREEN}🎉 Backend startup process completed!${NC}"
echo -e "${BLUE}💡 Use 'bench --site $SITE_NAME console' to access the Frappe console${NC}"
echo -e "${BLUE}💡 Use 'bench --site $SITE_NAME migrate' to run migrations${NC}"

