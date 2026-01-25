terraform {
  backend "s3" {
    bucket         = "agentic-devsecops-terraform-state" # Replace with your S3 bucket name
    key            = "terraform/state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table" # Replace with your DynamoDB table name
    encrypt        = true
  }
}
