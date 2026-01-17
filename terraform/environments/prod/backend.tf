# Production Environment Backend Configuration
terraform {
  backend "s3" {
    bucket         = "agentic-devsecops-terraform-state"
    key            = "terraform/prod/terraform.tfstate"  # Different key for prod
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
