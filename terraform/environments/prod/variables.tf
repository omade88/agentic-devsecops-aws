variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "public_subnet_count" {
  description = "Number of public subnets"
  type        = number
  default     = 2
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "instance_type" {
  description = "The type of EC2 instance to launch (t3.small recommended for production)"
  type        = string
  default     = "t3.small"
}

variable "ami_id" {
  description = "The AMI ID to use for the EC2 instance"
  type        = string
}

variable "allowed_ip_ranges" {
  description = "The IP ranges that are allowed to access resources"
  type        = list(string)
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "agentic-devsecops"
}

variable "sns_email" {
  description = "Email address for SNS notifications (Lambda alerts)"
  type        = string
}

variable "auto_fix_enabled" {
  description = "Enable automatic remediation (false = dry-run mode, true = auto-fix)"
  type        = bool
  default     = false
}