environment = "prod"

region = "us-east-1"

vpc_cidr = "10.1.0.0/16"

public_subnet_cidrs = ["10.1.1.0/24", "10.1.2.0/24"]

private_subnet_cidrs = ["10.1.3.0/24", "10.1.4.0/24"]

instance_type = "t3.small" # Production uses larger instances

# Amazon Linux 2023 AMI for us-east-1 (recommended)
ami_id = "ami-0453ec754f44f9a4a" # Amazon Linux 2023 - production ready

# Security: Replace with YOUR production IP ranges
# Find your IP: https://whatismyipaddress.com/
# Format: "YOUR.IP.ADDRESS.HERE/32"
# Example: allowed_ip_ranges = ["203.0.113.45/32"]
allowed_ip_ranges = ["YOUR.IP.ADDRESS.HERE/32"]

# Project Configuration
project_name = "agentic-devsecops"

# Lambda Auto-Remediation Configuration
# IMPORTANT: Replace with your actual production email address
sns_email = "your-email@example.com" # Replace with your actual email

# Auto-fix mode: false = dry-run (detect only), true = auto-fix issues
# RECOMMENDED: Start with false in production, enable after testing
auto_fix_enabled = false # Start with dry-run mode for safety

# If you need to allow multiple IPs or ranges:
# allowed_ip_ranges = ["203.0.113.45/32", "198.51.100.0/24", "192.0.2.0/24"]
