#!/bin/bash

# Development startup script for Frappe/ERPNext on Railway
set -e

echo "🚀 Starting Frappe/ERPNext in Development Mode..."

# Set default values
export SITE_NAME=${SITE_NAME:-"localhost"}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-"admin123"}
export FRAPPE_ENV=${FRAPPE_ENV:-"development"}
export DEVELOPER_MODE=${DEVELOPER_MODE:-"1"}

# Parse DATABASE_URL if provided by Railway
if [ ! -z "$DATABASE_URL" ]; then
    echo "📊 Parsing Railway DATABASE_URL..."
    # Extract database connection details from Railway's DATABASE_URL
    # Format: mysql://user:password@host:port/database
    DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
    DB_PASSWORD=$(echo $DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
    
    export DB_HOST DB_PORT DB_NAME DB_USER DB_PASSWORD
    echo "✅ Database configuration parsed successfully"
else
    echo "⚠️  No DATABASE_URL provided, using defaults"
    export DB_HOST=${DB_HOST:-"localhost"}
    export DB_PORT=${DB_PORT:-"3306"}
    export DB_NAME=${DB_NAME:-"erpnext"}
    export DB_USER=${DB_USER:-"root"}
    export DB_PASSWORD=${DB_PASSWORD:-"admin"}
fi

# Parse REDIS_URL if provided by Railway
if [ ! -z "$REDIS_URL" ]; then
    echo "🔴 Parsing Railway REDIS_URL..."
    echo "📋 REDIS_URL format: ${REDIS_URL}"
    # Extract Redis connection details
    REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*:\/\/[^@]*@\([^:]*\):.*/\1/p')
    REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)$/\1/p')
    REDIS_PASSWORD=$(echo $REDIS_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
    
    export REDIS_HOST REDIS_PORT REDIS_PASSWORD
    echo "✅ Redis configuration parsed successfully"
    echo "🔍 Redis Host: ${REDIS_HOST}"
    echo "🔍 Redis Port: ${REDIS_PORT}"
    echo "🔍 Redis Password: [REDACTED]"
else
    echo "⚠️  No REDIS_URL provided, using defaults"
    export REDIS_HOST=${REDIS_HOST:-"localhost"}
    export REDIS_PORT=${REDIS_PORT:-"6379"}
    export REDIS_PASSWORD=${REDIS_PASSWORD:-""}
fi

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --silent; then
        echo "✅ Database is ready!"
        break
    else
        echo "🔄 Attempt $attempt/$max_attempts: Database not ready, waiting 5 seconds..."
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Database failed to become ready after $max_attempts attempts"
    exit 1
fi

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."

# Check if redis-cli is available
if ! command -v redis-cli > /dev/null 2>&1; then
    echo "⚠️  redis-cli not found, skipping Redis connectivity test"
    echo "✅ Assuming Redis is ready (will be tested during Frappe startup)"
else
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        # Test Redis connection with detailed error output
        if [ ! -z "$REDIS_PASSWORD" ]; then
            redis_test_output=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" ping 2>&1)
        else
            redis_test_output=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping 2>&1)
        fi
        
        if echo "$redis_test_output" | grep -q "PONG"; then
            echo "✅ Redis is ready!"
            break
        else
            echo "🔄 Attempt $attempt/$max_attempts: Redis not ready, waiting 3 seconds..."
            echo "🔍 Redis test output: $redis_test_output"
            sleep 3
            attempt=$((attempt + 1))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ Redis failed to become ready after $max_attempts attempts"
        echo "⚠️  Continuing anyway - Frappe will test Redis connection during startup"
    fi
fi

# Change to bench directory
cd /home/frappe/frappe-bench

# Create site configuration from template
echo "📝 Creating site configuration..."
envsubst < /home/frappe/site_config.json.template > sites/${SITE_NAME}/site_config.json

# Check if site exists, create if it doesn't
if [ ! -d "sites/${SITE_NAME}" ]; then
    echo "🏗️  Creating new site: ${SITE_NAME}"
    
    bench new-site ${SITE_NAME} \
        --mariadb-root-password ${DB_PASSWORD} \
        --admin-password ${ADMIN_PASSWORD} \
        --db-host ${DB_HOST} \
        --db-port ${DB_PORT} \
        --db-name ${DB_NAME} \
        --db-user ${DB_USER} \
        --db-password ${DB_PASSWORD}
    
    echo "✅ Site created successfully!"
else
    echo "✅ Site ${SITE_NAME} already exists"
fi

# Install ERPNext app if not already installed
if ! bench --site ${SITE_NAME} list-apps | grep -q "erpnext"; then
    echo "📦 Installing ERPNext app..."
    bench --site ${SITE_NAME} install-app erpnext
    echo "✅ ERPNext app installed!"
fi

# Enable developer mode
echo "🛠️  Enabling developer mode..."
bench --site ${SITE_NAME} set-config developer_mode 1
bench --site ${SITE_NAME} clear-cache

# Set site as default
bench use ${SITE_NAME}

# Update site configuration with Railway environment
echo "🔧 Updating site configuration..."
bench --site ${SITE_NAME} set-config db_host ${DB_HOST}
bench --site ${SITE_NAME} set-config db_port ${DB_PORT}

# Configure Redis with authentication if password is provided
if [ ! -z "$REDIS_PASSWORD" ]; then
    echo "🔐 Configuring Redis with authentication..."
    bench --site ${SITE_NAME} set-config redis_cache "redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/0"
    bench --site ${SITE_NAME} set-config redis_queue "redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/1"
    bench --site ${SITE_NAME} set-config redis_socketio "redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/2"
else
    echo "🔓 Configuring Redis without authentication..."
    bench --site ${SITE_NAME} set-config redis_cache "redis://${REDIS_HOST}:${REDIS_PORT}/0"
    bench --site ${SITE_NAME} set-config redis_queue "redis://${REDIS_HOST}:${REDIS_PORT}/1"
    bench --site ${SITE_NAME} set-config redis_socketio "redis://${REDIS_HOST}:${REDIS_PORT}/2"
fi

# Set CORS configuration for development
if [ ! -z "$RAILWAY_PUBLIC_DOMAIN" ]; then
    echo "🌐 Configuring CORS for Railway domain: ${RAILWAY_PUBLIC_DOMAIN}"
    bench --site ${SITE_NAME} set-config allow_cors "https://${RAILWAY_PUBLIC_DOMAIN}"
fi

# Start file watcher in background for development
echo "👀 Starting file watcher for development..."
bench --site ${SITE_NAME} watch &

# Start the development server
echo "🎉 Starting Frappe development server..."
echo "🌐 Web interface will be available on port 8000"
echo "🔌 SocketIO will be available on port 9000"
echo "👤 Admin credentials: Administrator / ${ADMIN_PASSWORD}"

# Start bench serve with development settings
exec bench serve --port 8000 --host 0.0.0.0
