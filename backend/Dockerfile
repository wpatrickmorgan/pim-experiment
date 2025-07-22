# Backend Dockerfile for separate Frappe deployment
FROM frappe/frappe:v15

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy the imperium_pim app
COPY --chown=frappe:frappe imperium_pim ./apps/imperium_pim

# Copy requirements and setup files
COPY --chown=frappe:frappe requirements.txt ./apps/imperium_pim/
COPY --chown=frappe:frappe setup.py ./apps/imperium_pim/

# Install the app
USER frappe
RUN bench get-app --skip-assets imperium_pim file:///home/frappe/frappe-bench/apps/imperium_pim

# Create a new site (this will be overridden in production)
RUN bench new-site pim.local \
    --admin-password admin \
    --mariadb-root-password admin \
    --install-app imperium_pim

# Configure CORS for separate frontend deployment
RUN echo '{\n\
  "allow_cors": "*",\n\
  "cors_headers": [\n\
    "Authorization",\n\
    "Content-Type",\n\
    "X-Requested-With",\n\
    "Accept",\n\
    "Origin",\n\
    "Cache-Control"\n\
  ]\n\
}' > sites/pim.local/site_config.json

# Expose port
EXPOSE 8000

# Start command
CMD ["bench", "start"]

