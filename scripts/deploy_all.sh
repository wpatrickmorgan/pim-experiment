#!/bin/bash

# Deploy All Script
# Builds frontend, restarts backend, and reloads nginx

set -e

echo "🚀 Deploying Full Stack..."
echo "=========================="

# Build frontend
echo "1️⃣ Building frontend..."
./scripts/build_frontend.sh

# Restart backend services if running
echo ""
echo "2️⃣ Restarting backend services..."
cd backend

# Check if bench processes are running and restart them
if pgrep -f "bench" > /dev/null; then
    echo "🔄 Restarting bench processes..."
    pkill -f "bench" || true
    sleep 2
    
    # Start bench in background
    nohup bench start > bench.log 2>&1 &
    echo "✅ Backend restarted (running in background)"
    echo "📋 Check backend/bench.log for logs"
else
    echo "ℹ️ Backend not running. Start with: ./scripts/start_backend.sh"
fi

cd ..

# Reload nginx
echo ""
echo "3️⃣ Reloading nginx..."
sudo nginx -s reload
echo "✅ Nginx reloaded"

echo ""
echo "🎉 Deployment completed!"
echo "========================"
echo ""
echo "🌐 Frontend: http://client-a.localtest.me"
echo "🔧 Backend: http://localhost:8000"
echo "🧪 Test API: http://client-a.localtest.me/api/method/imperium_pim.api.ping"
echo ""
echo "📊 Service Status:"
echo "- Nginx: $(systemctl is-active nginx)"
echo "- MariaDB: $(systemctl is-active mariadb)"
echo "- Redis: $(systemctl is-active redis-server)"
echo "- Bench: $(pgrep -f "bench" > /dev/null && echo "active" || echo "inactive")"

