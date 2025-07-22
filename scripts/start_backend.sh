#!/bin/bash

# Start Backend Script
# Starts the Frappe backend server

set -e

echo "🚀 Starting Frappe Backend..."
echo "=============================="

cd backend

# Check if bench is initialized
if [ ! -f "sites/currentsite.txt" ]; then
    echo "❌ Backend not initialized. Run ./scripts/setup.sh first."
    exit 1
fi

# Start required services
echo "🔧 Starting system services..."
sudo systemctl start mariadb || echo "MariaDB already running"
sudo systemctl start redis-server || echo "Redis already running"

# Start bench
echo "🏃 Starting bench server..."
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://client-a.localtest.me"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start bench with all processes
bench start

