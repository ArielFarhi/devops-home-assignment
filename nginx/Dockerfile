# Base image must be Ubuntu (per assignment requirements)
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install nginx and clean apt cache to keep image small
RUN apt-get update && \
    apt-get install -y nginx openssl && \
    rm -rf /var/lib/apt/lists/*

# Remove default nginx configuration
RUN rm -f /etc/nginx/sites-enabled/default

# Copy nginx main configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy server block configurations
COPY sites/ /etc/nginx/conf.d/

# Copy static HTML content
COPY html/ /var/www/html/

# Copy certificates (used for HTTPS bonus)
COPY certs/ /etc/nginx/certs/

# Expose ports
# 8080 -> HTML server
# 8081 -> Error server
# 443  -> HTTPS (bonus)
EXPOSE 8080 8081 443

# Run nginx in foreground (required for Docker)
CMD ["nginx", "-g", "daemon off;"]
