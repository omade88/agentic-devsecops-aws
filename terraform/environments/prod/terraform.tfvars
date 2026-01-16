variable_values = {
  "vpc_cidr" = "10.0.0.0/16"
  "public_subnet_cidrs" = ["10.0.1.0/24"]
  "private_subnet_cidrs" = ["10.0.2.0/24"]
  "instance_type" = "t2.micro"
  "ami_id" = "ami-0c55b159cbfafe1f0"  # Example AMI ID, replace with a valid one for your region
  "allowed_ip_ranges" = ["0.0.0.0/0"]  # Adjust as necessary for security
}