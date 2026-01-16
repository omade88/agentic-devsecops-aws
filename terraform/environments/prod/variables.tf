variable "instance_type" {
  description = "The type of EC2 instance to launch"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID to use for the EC2 instance"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the EC2 instance will be deployed"
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet where the EC2 instance will be deployed"
  type        = string
}

variable "allowed_ip_ranges" {
  description = "The IP ranges allowed to access the EC2 instance"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}