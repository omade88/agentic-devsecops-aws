#!/bin/bash
# Deploy Lambda Functions Script
# Packages and deploys Lambda functions to AWS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "Lambda Functions Deployment"
echo "========================================"
echo ""

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured or credentials invalid"
    echo "Run: aws configure"
    exit 1
fi

echo "✅ AWS credentials valid"
echo "Account: $(aws sts get-caller-identity --query Account --output text)"
echo "Region: $(aws configure get region)"
echo ""

# Get environment
read -p "Enter environment (dev/staging/prod) [dev]: " ENVIRONMENT
ENVIRONMENT=${ENVIRONMENT:-dev}

echo ""
echo "Deploying to environment: $ENVIRONMENT"
echo ""

# Navigate to Terraform directory
cd "$PROJECT_ROOT/terraform/environments/$ENVIRONMENT"

# Check if terraform is initialized
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
fi

# Package Lambda functions
echo "Packaging Lambda functions..."
cd "$PROJECT_ROOT/lambda"

for func_dir in */; do
    func_name=$(basename "$func_dir")
    echo "  - Packaging $func_name..."
    
    cd "$func_dir"
    
    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt -t .
    fi
    
    # Create deployment package
    zip -r "../${func_name}.zip" . -x "*.pyc" "**/__pycache__/*"
    
    cd ..
done

echo "✅ Lambda functions packaged"
echo ""

# Deploy with Terraform
cd "$PROJECT_ROOT/terraform/environments/$ENVIRONMENT"

echo "Planning deployment..."
terraform plan -out=tfplan

echo ""
read -p "Apply this plan? (yes/no): " APPLY

if [ "$APPLY" = "yes" ]; then
    echo "Applying Terraform configuration..."
    terraform apply tfplan
    
    echo ""
    echo "========================================"
    echo "✅ Deployment Complete!"
    echo "========================================"
    echo ""
    
    # Show outputs
    terraform output
    
    echo ""
    echo "Lambda functions deployed:"
    aws lambda list-functions \
        --query "Functions[?contains(FunctionName, 'agentic-devsecops')].FunctionName" \
        --output table
    
else
    echo "Deployment cancelled"
    rm tfplan
fi
