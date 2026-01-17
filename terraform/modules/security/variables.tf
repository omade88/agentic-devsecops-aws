variable "vpc_id" {
  description = "VPC ID where security groups will be created"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "allowed_ip_ranges" {
  description = "List of allowed IP ranges for inbound traffic"
  type        = list(string)
}

variable "security_group_name" {
  description = "Name of the security group"
  type        = string
  default     = "default-security-group"
}

variable "iam_role_name" {
  description = "Name of the IAM role for EC2 instances"
  type        = string
  default     = "ec2-instance-role"
}