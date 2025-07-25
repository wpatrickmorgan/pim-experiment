#!/bin/bash

# Production startup script for Frappe/ERPNext on Railway
set -e

echo "🚀 Starting Frappe/ERPNext in Production Mode..."

# Set default values
export SITE_NAME=${SITE_NAME:-"mysite"}
export FRAPPE_ENV=${FRAPPE_ENV:-"production"}
export DEVELOPER_MODE=${DEVELOPER_MODE:-"0"}
export WORKERS=${WORKERS:-"4"}
export TIMEOUT=${TIMEOUT:-"120"}

# Validate required environment variables
if [ -z "$ADMIN_PASSWORD" ]; then
    echo "❌ ADMIN_PASSWORD environment variable is required for production"
    exit 1
fi

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
    echo "❌ DATABASE_URL is required for production deployment"
    exit 1
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
    echo "❌ REDIS_URL is required for production deployment"
    exit 1
fi

# Wait for database to be ready with longer timeout for production
echo "⏳ Waiting for database to be ready..."
max_attempts=60
attempt=1

while [ $attempt -le $max_attempts ]; do
    if mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --silent; then
        echo "✅ Database is ready!"
        break
    else
        echo "🔄 Attempt $attempt/$max_attempts: Database not ready, waiting 10 seconds..."
        sleep 10
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
            echo "🔄 Attempt $attempt/$max_attempts: Redis not ready, waiting 5 seconds..."
            echo "🔍 Redis test output: $redis_test_output"
            sleep 5
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

# Initialize database SQL mode for MariaDB compatibility
echo "🔧 Initializing database SQL mode..."
python3 /home/frappe/init_db.py

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
        --db-password ${DB_PASSWORD} \
        --force
    
    echo "✅ Site created successfully!"
else
    echo "✅ Site ${SITE_NAME} already exists"
fi

# Set default values for optional environment variables
export DEVELOPER_MODE=${DEVELOPER_MODE:-false}
export FRAPPE_LOGGING_LEVEL=${FRAPPE_LOGGING_LEVEL:-INFO}
export WORKERS=${WORKERS:-4}
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
export GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}
export GUNICORN_KEEPALIVE=${GUNICORN_KEEPALIVE:-5}
export MAIL_PORT=${MAIL_PORT:-587}
export MAIL_USE_TLS=${MAIL_USE_TLS:-true}

# Generate encryption keys if not provided
if [ -z "$ENCRYPTION_KEY" ]; then
    export ENCRYPTION_KEY=$(openssl rand -base64 32)
    echo "🔐 Generated encryption key"
fi

if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(openssl rand -base64 32)
    echo "🔐 Generated secret key"
fi

# Create site configuration from template
echo "📝 Creating site configuration..."

# Use sed to replace variables with their values (envsubst doesn't handle defaults well)
sed -e "s/\${DEVELOPER_MODE:-false}/${DEVELOPER_MODE}/g" \
    -e "s/\${FRAPPE_LOGGING_LEVEL:-INFO}/${FRAPPE_LOGGING_LEVEL}/g" \
    -e "s/\${MAIL_PORT:-587}/${MAIL_PORT}/g" \
    -e "s/\${MAIL_USE_TLS:-true}/${MAIL_USE_TLS}/g" \
    -e "s/\${WORKERS:-4}/${WORKERS}/g" \
    -e "s/\${GUNICORN_WORKERS:-4}/${GUNICORN_WORKERS}/g" \
    -e "s/\${GUNICORN_TIMEOUT:-120}/${GUNICORN_TIMEOUT}/g" \
    -e "s/\${GUNICORN_KEEPALIVE:-5}/${GUNICORN_KEEPALIVE}/g" \
    /home/frappe/site_config.json.template | envsubst > sites/${SITE_NAME}/site_config.json

# Validate JSON syntax
if ! python3 -m json.tool sites/${SITE_NAME}/site_config.json > /dev/null 2>&1; then
    echo "❌ Invalid JSON in site_config.json"
    echo "🔍 Contents of site_config.json:"
    cat sites/${SITE_NAME}/site_config.json
    exit 1
else
    echo "✅ Site configuration JSON is valid"
fi

# Install ERPNext app if not already installed
if ! bench --site ${SITE_NAME} list-apps | grep -q "erpnext"; then
    echo "📦 Installing ERPNext app..."
    bench --site ${SITE_NAME} install-app erpnext
    echo "✅ ERPNext app installed!"
fi

# Disable developer mode for production
echo "🔒 Configuring production settings..."
bench --site ${SITE_NAME} set-config developer_mode 0

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

# Set production CORS configuration
if [ ! -z "$RAILWAY_PUBLIC_DOMAIN" ]; then
    echo "🌐 Configuring CORS for production domain: ${RAILWAY_PUBLIC_DOMAIN}"
    bench --site ${SITE_NAME} set-config allow_cors "https://${RAILWAY_PUBLIC_DOMAIN}"
fi

# Run database migrations
echo "🔄 Running database migrations..."
bench --site ${SITE_NAME} migrate

# Clear cache
echo "🧹 Clearing cache..."
bench --site ${SITE_NAME} clear-cache

# Build assets for production
echo "🏗️  Building production assets..."
bench build --production

# Start background workers
echo "👷 Starting background workers..."
bench --site ${SITE_NAME} scheduler enable
bench worker --queue default,long,short &

# Start the production server with gunicorn
echo "🎉 Starting Frappe production server..."
echo "🌐 Web interface will be available on port 8000"
echo "👤 Admin credentials: Administrator / ${ADMIN_PASSWORD}"

# Start gunicorn with production settings
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers ${WORKERS} \
    --timeout ${TIMEOUT} \
    --keepalive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    frappe.app:application
