variable "instance_type" {
  description = "The type of EC2 instance to launch"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID to use for the EC2 instance"
  default     = "ami-0c55b159cbfafe1f0"  # Example AMI ID, replace with a valid one for your region
}

variable "vpc_id" {
  description = "The ID of the VPC where the EC2 instance will be deployed"
}

variable "subnet_id" {
  description = "The ID of the subnet where the EC2 instance will be deployed"
}

variable "allowed_ip_ranges" {
  description = "The IP ranges that are allowed to access the EC2 instance"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Replace with more restrictive ranges as needed
}