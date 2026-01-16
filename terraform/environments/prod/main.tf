resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr = var.vpc_cidr
  environment = var.environment
}

module "security" {
  source = "../../modules/security"

  allowed_ips = var.allowed_ips
}

module "ec2" {
  source = "../../modules/ec2"

  instance_type = var.instance_type
  ami_id = var.ami_id
  vpc_id = module.vpc.vpc_id
  security_group_ids = module.security.security_group_ids
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "instance_id" {
  value = module.ec2.instance_id
}

output "public_ip" {
  value = module.ec2.public_ip
}