# Development Dockerfile for Frappe/ERPNext on Railway
FROM frappe/erpnext:latest

# Set environment variables for development
ENV FRAPPE_ENV=development
ENV DEVELOPER_MODE=1
ENV PYTHONUNBUFFERED=1

# Install development tools and dependencies
USER root

# Install additional development tools (only essential ones to avoid conflicts)
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    curl \
    wget \
    git \
    htop \
    tree \
    iputils-ping \
    procps \
    redis-tools \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir \
    ipython \
    ipdb \
    watchdog \
    python-dotenv

# Switch back to frappe user
USER frappe

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy startup script and configuration files
COPY --chown=frappe:frappe start-dev.sh /home/frappe/start-dev.sh
COPY --chown=frappe:frappe site_config.json.template /home/frappe/site_config.json.template
COPY --chown=frappe:frappe init_db.py /home/frappe/init_db.py

# Make startup script executable
USER root
RUN chmod +x /home/frappe/start-dev.sh /home/frappe/init_db.py
USER frappe

# Expose ports for web server and socketio
EXPOSE 8000 9000

# Health check for development
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000 || exit 1

# Set the startup command
CMD ["/home/frappe/start-dev.sh"]
