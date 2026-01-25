# AWS Provider Configuration
# Region is set via variable to support multi-region deployments
provider "aws" {
  region = var.region
}

# Main VPC - Isolated network for production environment
# DNS support enabled for service discovery and hostname resolution
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Public Subnets - For resources requiring internet access
# Distributed across multiple availability zones for high availability
resource "aws_subnet" "public" {
  count             = var.public_subnet_count
  vpc_id            = aws_vpc.main.id
  cidr_block        = element(var.public_subnet_cidrs, count.index)
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
  count          = var.public_subnet_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Lambda Functions Module - Auto-remediation and security response
module "lambda_functions" {
  source = "../../modules/lambda-functions"

  environment      = var.environment
  project_name     = var.project_name
  sns_email        = var.sns_email
  auto_fix_enabled = var.auto_fix_enabled

  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

output "vpc_id" {
  value       = aws_vpc.main.id
  description = "Production VPC ID"
}

output "public_subnet_ids" {
  value       = aws_subnet.public[*].id
  description = "Production public subnet IDs"
}

output "auto_remediation_function_arn" {
  value       = module.lambda_functions.auto_remediation_function_arn
  description = "Production auto-remediation Lambda function ARN"
}

output "security_response_function_arn" {
  value       = module.lambda_functions.security_response_function_arn
  description = "Production security response Lambda function ARN"
}

output "sns_topic_arn" {
  value       = module.lambda_functions.sns_topic_arn
  description = "Production SNS topic ARN for security alerts"
}
