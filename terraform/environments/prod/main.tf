# AWS Provider Configuration
# Region is set via variable to support multi-region deployments
provider "aws" {
  region = var.region
}

# Main VPC - Isolated network for production environment
# DNS support enabled for service discovery and hostname resolution
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Public Subnets - For resources requiring internet access
# Distributed across multiple availability zones for high availability
resource "aws_subnet" "public" {
  count = var.public_subnet_count
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.public_subnet_cidrs, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = "${var.environment}-public-subnet-${count.index + 1}"
  }
}

# Internet Gateway - Enables internet connectivity for VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.environment}-igw"
  }
}

# Public Route Table - Routes traffic to internet gateway
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.environment}-public-rt"
  }
}

# Route Table Associations - Connect subnets to route table
resource "aws_route_table_association" "public" {
  count = var.public_subnet_count
  subnet_id = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security Module - Manages security groups and rules
module "security" {
  source = "../../modules/security"

  vpc_id = aws_vpc.main.id
  environment = var.environment
  allowed_ip_ranges = var.allowed_ip_ranges
}

# Lambda Functions Module - Auto-remediation and security response
module "lambda_functions" {
  source = "../../modules/lambda-functions"

  environment = var.environment
  vpc_id = aws_vpc.main.id
  security_group_id = module.security.lambda_security_group_id
  sns_email = var.sns_email
  auto_fix_enabled = var.auto_fix_enabled
}

output "vpc_id" {
  value = aws_vpc.main.id
  description = "Production VPC ID"
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
  description = "Production public subnet IDs"
}

output "lambda_function_arns" {
  value = module.lambda_functions.function_arns
  description = "Production Lambda function ARNs"
}

output "sns_topic_arn" {
  value = module.lambda_functions.sns_topic_arn
  description = "Production SNS topic ARN for security alerts"
}