#!/bin/bash
# This script is executed on instance startup to configure the Linux workload.

# Update the package repository
apt-get update -y

# Install NGINX
apt-get install nginx -y

# Start and enable NGINX service
systemctl start nginx
systemctl enable nginx

# Apply basic security hardening
ufw allow 'Nginx Full'
ufw enable

# Create a sample index.html file
echo "<h1>Welcome to the Agentic DevSecOps on AWS!</h1>" > /var/www/html/index.html

# Restart NGINX to apply changes
systemctl restart nginx

# End of script
