#!/bin/bash

# Update the package index
sudo apt-get update

# Install NGINX
sudo apt-get install -y nginx

# Start NGINX service
sudo systemctl start nginx

# Enable NGINX to start on boot
sudo systemctl enable nginx

# Apply basic security hardening
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Additional hardening steps can be added here

echo "NGINX installation and basic hardening completed."