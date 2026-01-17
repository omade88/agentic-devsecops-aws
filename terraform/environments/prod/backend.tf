# Production Environment Backend Configuration
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"  # Replace with your S3 bucket name
    key            = "terraform/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "your-terraform-state-lock"  # Replace with your DynamoDB table name
    encrypt        = true
  }
}
