#!/bin/bash

# Validate Terraform configurations
terraform validate

# Check for formatting issues
terraform fmt -check

# Run TFLint for linting
tflint

# Run tfsec for security checks (optional)
if command -v tfsec &> /dev/null; then
  echo "Running tfsec security scan..."
  tfsec .
else
  echo "⚠️  tfsec not found - skipping security scan (install from: https://github.com/aquasecurity/tfsec)"
fi

# Exit with status code based on the success of the checks
if [ $? -ne 0 ]; then
  echo "Validation failed."
  exit 1
else
  echo "Validation succeeded."
  exit 0
fi
