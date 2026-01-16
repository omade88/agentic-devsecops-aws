#!/bin/bash

# Validate Terraform configurations
terraform validate

# Check for formatting issues
terraform fmt -check

# Run TFLint for linting
tflint

# Run tfsec for security checks
tfsec . 

# Exit with status code based on the success of the checks
if [ $? -ne 0 ]; then
  echo "Validation failed."
  exit 1
else
  echo "Validation succeeded."
  exit 0
fi