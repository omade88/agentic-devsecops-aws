# Staging Environment Configuration
environment = "staging"
region = "us-east-1"

# Network Configuration - Different CIDR from dev to avoid conflicts
vpc_cidr = "10.1.0.0/16"
public_subnet_cidrs = ["10.1.1.0/24", "10.1.2.0/24"]
private_subnet_cidrs = ["10.1.3.0/24", "10.1.4.0/24"]

# Compute Configuration
instance_type = "t3.micro"  # Free tier eligible
ami_id = "ami-0453ec754f44f9a4a"  # Amazon Linux 2023 us-east-1

# Security Configuration
# IMPORTANT: Replace with your actual IP address
# Get your IP: curl https://api.ipify.org
allowed_ip_ranges = ["203.0.113.45/32", "198.51.100.0/24"]