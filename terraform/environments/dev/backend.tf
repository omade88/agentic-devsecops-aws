# Dev Environment Backend Configuration
terraform {
  backend "s3" {
    bucket         = "agentic-devsecops-terraform-state" # Replace with your S3 bucket name
    key            = "terraform/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "agentic-devsecops-terraform-lock-table" # Replace with your DynamoDB table name
    encrypt        = true
  }
}
