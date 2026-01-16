# Lambda Functions Module for Agentic AI Auto-Remediation

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "agentic-devsecops"
}

variable "sns_email" {
  description = "Email address for SNS notifications"
  type        = string
}

variable "auto_fix_enabled" {
  description = "Enable automatic remediation (set to false for dry-run mode)"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
