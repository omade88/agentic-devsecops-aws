# Dev Environment Backend Configuration
terraform {
  backend "s3" {
    bucket         = "agentic-devsecops-terraform-state"
    key            = "terraform/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
