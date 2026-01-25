# Dev Environment Backend Configuration
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket" # Replace with your S3 bucket name
    key            = "terraform/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "Your-terraform-state-lock" # Replace with your DynamoDB table name
    encrypt        = true
  }
}
