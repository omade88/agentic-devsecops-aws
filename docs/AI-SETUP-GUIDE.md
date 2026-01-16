# 🤖 AI-Powered DevSecOps Setup Guide (FREE Version)

## Complete Guide to Setting Up Local AI for Infrastructure Automation

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start (5 Minutes)](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Using AI Features](#using-ai-features)
6. [Cost Analysis](#cost-analysis)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This project uses **100% FREE** AI tools to power your DevSecOps workflow:

### What You Get (All FREE!)

✅ **Local AI Code Review** (Ollama + LLaMA 3.1)  
✅ **Automated Security Scanning** (TFLint, tfsec, Checkov, Trivy)  
✅ **AI Policy Generation** (Natural language → OPA/Sentinel)  
✅ **Auto-Remediation** (AWS Lambda - free tier)  
✅ **ChatOps Notifications** (Discord/Slack webhooks)  
✅ **PR-Driven Deployments** (GitHub Actions - 2000 min/month free)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Repository                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Pull Request Created                              │     │
│  └──────────────┬─────────────────────────────────────┘     │
│                 ▼                                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  GitHub Actions Workflows (FREE)                   │     │
│  │  ├─ AI Code Review (Ollama)                        │     │
│  │  ├─ Security Scans (TFLint, tfsec, Checkov)        │     │
│  │  ├─ Terraform Validation                           │     │
│  │  └─ OPA Policy Checks                              │     │
│  └──────────────┬─────────────────────────────────────┘     │
└─────────────────┼──────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Local AI (Your Machine)                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Ollama + LLaMA 3.1 (FREE)                         │     │
│  │  ├─ Code analysis                                  │     │
│  │  ├─ Security recommendations                       │     │
│  │  ├─ Policy generation                              │     │
│  │  └─ Best practice suggestions                      │     │
│  └──────────────┬─────────────────────────────────────┘     │
└─────────────────┼──────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   AWS (Free Tier)                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Lambda Functions (1M requests/month FREE)         │     │
│  │  ├─ Auto-remediation (fix security issues)         │     │
│  │  ├─ Security response (isolate threats)            │     │
│  │  └─ Cost optimization                              │     │
│  └──────────────┬─────────────────────────────────────┘     │
│                 ▼                                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  EventBridge (FREE tier)                           │     │
│  │  ├─ Security group changes                         │     │
│  │  ├─ EC2 state changes                              │     │
│  │  └─ S3 bucket modifications                        │     │
│  └──────────────┬─────────────────────────────────────┘     │
└─────────────────┼──────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────┐
│               ChatOps (Discord/Slack - FREE)                 │
│  ├─ Deployment notifications                                │
│  ├─ Security alerts                                         │
│  ├─ Cost optimization recommendations                       │
│  └─ PR review summaries                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required (Must Have)

- **OS**: Linux, macOS, or Windows WSL2
- **RAM**: 8GB minimum (16GB recommended for AI models)
- **Disk**: 10GB free space (for AI models)
- **AWS Account**: Free tier eligible
- **GitHub Account**: Free tier (2000 min/month Actions)

### Optional (Nice to Have)

- Discord or Slack account (for notifications)
- GPU (speeds up AI inference, but not required)

---

## Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

This automated approach will set up your complete Agentic AI DevSecOps environment on AWS in approximately 15-20 minutes.

#### Prerequisites Before Starting

1. **AWS Account** - Sign up at https://aws.amazon.com (Free tier eligible)
2. **GitHub Account** - Sign up at https://github.com (Free tier with 2000 Actions minutes/month)
3. **System Requirements**:
   - 8GB RAM minimum (16GB recommended)
   - 10GB free disk space
   - Linux, macOS, or Windows WSL2

---

#### Detailed Step-by-Step Instructions

##### Step 1: Prepare AWS Credentials

1. **Log in to AWS Console**: https://console.aws.amazon.com

2. **Create IAM User for Terraform**:
   - Navigate to **IAM → Users → Add users**
   - Username: `terraform-deployer`
   - Select **"Access key - Programmatic access"**
   - Click **Next: Permissions**

3. **Attach Policies**:
   - Click **"Attach existing policies directly"**
   - Select these policies:
     - `AmazonEC2FullAccess`
     - `AmazonVPCFullAccess`
     - `AmazonS3FullAccess`
     - `IAMFullAccess`
     - `CloudWatchFullAccess`
     - `AWSLambda_FullAccess`
     - `AmazonEventBridgeFullAccess`
     - `AmazonDynamoDBFullAccess`
   - Click **Next** → **Create user**

4. **Save Your Credentials**:
   - ⚠️ **CRITICAL**: Download the CSV file or copy:
     - `Access Key ID` (e.g., AKIAIOSFODNN7EXAMPLE)
     - `Secret Access Key` (e.g., wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)
   - You won't see the Secret Key again!

5. **Create S3 Bucket for Terraform State**:
   - Go to **S3 → Create bucket**
   - Bucket name: `agentic-devsecops-terraform-state-<your-initials>` (must be globally unique)
   - Region: `us-east-1` (or your preferred region)
   - Enable **"Bucket Versioning"**
   - Enable **"Default encryption"** (SSE-S3)
   - Click **Create bucket**

6. **Create DynamoDB Table for State Locking**:
   - Go to **DynamoDB → Create table**
   - Table name: `terraform-state-lock`
   - Partition key: `LockID` (String)
   - Use default settings
   - Click **Create table**

---

##### Step 2: Clone and Configure Repository

```bash
# Clone the repository
git clone https://github.com/omade88/agentic-devsecops-aws.git
cd agentic-devsecops-aws

# Make setup script executable
chmod +x scripts/setup-ai.sh
```

---

##### Step 3: Configure AWS Credentials Locally

```bash
# Install AWS CLI (if not already installed)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure

# When prompted, enter:
# AWS Access Key ID: <paste your Access Key ID>
# AWS Secret Access Key: <paste your Secret Access Key>
# Default region name: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
# Should show your account ID, user ARN, and user ID
```

---

##### Step 4: Update Terraform Backend Configuration

```bash
# Edit the backend configuration
nano terraform/backend.tf

# Update with your S3 bucket name:
terraform {
  backend "s3" {
    bucket         = "agentic-devsecops-terraform-state-<your-initials>"
    key            = "terraform/state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

# Save and exit (Ctrl+X, Y, Enter)
```

---

##### Step 5: Run the Automated Setup Script

```bash
# Execute the setup script
./scripts/setup-ai.sh

# The script will automatically:
# ✅ Detect your OS (Linux/macOS/WSL2)
# ✅ Install Python 3, pip, git, curl
# ✅ Install Terraform 1.6.0
# ✅ Install security tools (TFLint, tfsec, Checkov, Trivy)
# ✅ Install Ollama (local AI runtime)
# ✅ Download LLaMA 3.1:8b model (~4.7GB, one-time)
# ✅ Install OPA (Open Policy Agent)
# ✅ Install Python dependencies (requests, boto3, etc.)
# ✅ Set up pre-commit hooks for git
# ✅ Validate all installations

# This will take 10-15 minutes depending on your internet speed
```

**What to expect during installation**:
- Progress bars for downloading Ollama model
- Terraform version check
- Security tool installations
- Python package installations
- Final validation summary

---

##### Step 6: Initialize and Deploy Infrastructure

```bash
# Navigate to dev environment
cd terraform/environments/dev

# Create terraform.tfvars file
cat > terraform.tfvars << EOF
environment    = "dev"
project_name   = "agentic-devsecops"
aws_region     = "us-east-1"
vpc_cidr       = "10.0.0.0/16"
EOF

# Initialize Terraform
terraform init

# Review the infrastructure plan
terraform plan

# Expected resources to be created:
# - VPC with public/private subnets
# - Security groups with guardrails
# - Lambda functions (auto-remediation, security-response)
# - EventBridge rules for automated triggers
# - SNS topics for notifications
# - CloudWatch log groups
# - IAM roles and policies

# Apply the infrastructure (creates AWS resources)
terraform apply

# Type 'yes' when prompted
# This will take 5-10 minutes to complete
```

---

##### Step 7: Configure GitHub Repository Secrets

1. **Go to your GitHub repository**:
   - URL: `https://github.com/omade88/agentic-devsecops-aws`

2. **Navigate to Settings**:
   - Click **Settings** tab
   - Click **Secrets and variables** → **Actions**

3. **Add these secrets** (click **New repository secret** for each):

   | Secret Name | Value | Description |
   |-------------|-------|-------------|
   | `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID | From Step 1 |
   | `AWS_SECRET_ACCESS_KEY` | Your Secret Access Key | From Step 1 |
   | `AWS_REGION` | `us-east-1` | Your AWS region |
   | `DISCORD_WEBHOOK_URL` | Your Discord webhook (optional) | For notifications |
   | `SLACK_WEBHOOK_URL` | Your Slack webhook (optional) | For notifications |

4. **Verify secrets are added**:
   - You should see 3 required secrets (AWS credentials + region)
   - Optional: 2 additional secrets for ChatOps

---

##### Step 8: Test the AI-Powered Workflows

```bash
# Return to project root
cd ../../..

# Create a test feature branch
git checkout -b test/ai-review

# Make a test change to trigger AI review
echo "# Test change" >> README.md

# Commit and push
git add README.md
git commit -m "test: Trigger AI code review"
git push origin test/ai-review

# Create Pull Request on GitHub
# Go to: https://github.com/omade88/agentic-devsecops-aws/pulls
# Click "New pull request"
# Select: base: main ← compare: test/ai-review
# Click "Create pull request"
```

**What happens next**:
1. GitHub Actions workflows trigger automatically
2. AI code review analyzes your changes (using Ollama locally)
3. Security scans run (TFLint, tfsec, Checkov, Trivy)
4. OPA policies validate compliance
5. Results appear as PR comments
6. Notifications sent to Discord/Slack (if configured)

---

##### Step 9: Monitor AWS Lambda Functions

```bash
# Check Lambda function deployment
aws lambda list-functions --query "Functions[?contains(FunctionName, 'agentic')].FunctionName"

# Expected output:
# [
#     "agentic-devsecops-dev-auto-remediation",
#     "agentic-devsecops-dev-security-response"
# ]

# View Lambda logs
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow

# Test auto-remediation (create a security group with 0.0.0.0/0 open)
# Lambda will automatically detect and fix it
```

---

##### Step 10: Verify AI Assistant is Running

```bash
# Test local AI code reviewer
cd ai-assistant
python3 pr-reviewer.py

# Test AI policy generator
python3 policy-generator.py --interactive

# When prompted, try:
# "Create a policy to block all SSH access from the internet"
# AI will generate complete OPA policy code!
```

---

#### Setup Complete! 🎉

Your Agentic AI DevSecOps environment is now fully operational:

✅ **AWS Infrastructure**: Lambda, EventBridge, VPC, Security Groups  
✅ **Local AI**: Ollama + LLaMA 3.1 ready for code review  
✅ **Security Tools**: TFLint, tfsec, Checkov, Trivy installed  
✅ **GitHub Actions**: Automated workflows running  
✅ **Auto-Remediation**: Lambda functions monitoring AWS  
✅ **ChatOps**: Notifications configured (if setup)

**Cost Tracking**: $0/month (all within free tiers)

---

#### Next Steps

1. **Create infrastructure changes** → Open PR → Watch AI review
2. **Deploy workloads** using Terraform modules in `terraform/modules/`
3. **Customize OPA policies** in `policies/templates/`
4. **Set up ChatOps** for team notifications
5. **Monitor costs** in AWS Cost Explorer

For troubleshooting, see [Troubleshooting Section](#troubleshooting) below.

```

### Option 2: Manual Setup

If you prefer manual installation, see [Detailed Setup](#detailed-setup) below.

---

## Detailed Setup

### Step 1: Install Core Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3 python3-pip git curl unzip
```

#### On macOS:
```bash
brew install python3 git curl
```

#### On Windows (WSL2):
```bash
wsl --install Ubuntu
# Then follow Ubuntu instructions
```

### Step 2: Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### Step 3: Install Terraform

```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
terraform --version
```

### Step 4: Install Security Tools

```bash
# TFLint
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# tfsec
curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash

# OPA
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod 755 opa
sudo mv opa /usr/local/bin/

# Checkov
pip3 install checkov
```

### Step 5: Install Ollama (Local AI)

```bash
# On Linux
curl -fsSL https://ollama.ai/install.sh | sh

# On macOS
brew install ollama

# Start Ollama service
ollama serve &

# Pull LLaMA 3.1 model (one-time download ~4.7GB)
ollama pull llama3.1:8b

# Test it
ollama run llama3.1:8b "Hello, are you ready?"
```

### Step 6: Install Python Dependencies

```bash
# AI Assistant dependencies
cd ai-assistant
pip3 install -r requirements.txt

# ChatOps dependencies
cd ../chatops
pip3 install -r requirements.txt
```

### Step 7: Configure AWS

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-west-2
# Default output format: json

# Verify
aws sts get-caller-identity
```

### Step 8: Set Up GitHub Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Agentic AI DevSecOps"

# Create GitHub repository and push
gh repo create agentic-devsecops-aws --public
git push -u origin main
```

### Step 9: Configure GitHub Secrets

Navigate to your GitHub repository:  
`Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: us-west-2 (or your preferred region)

### Step 10: Enable Branch Protection

Navigate to: `Settings → Branches → Add rule`

For `main` branch:
- ✅ Require pull request reviews (1 approval)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- Select: `validate`, `terraform`, `security-scan`

---

## Using AI Features

### Feature 1: AI-Powered PR Reviews

**How it works:**
1. Create a feature branch
2. Make changes to Terraform files
3. Open a pull request
4. AI automatically reviews and comments

**Example:**

```bash
# Create feature branch
git checkout -b feature/add-s3-bucket

# Make changes
cat > terraform/environments/dev/s3.tf << EOF
resource "aws_s3_bucket" "example" {
  bucket = "my-test-bucket"
}
EOF

# Commit and push
git add .
git commit -m "feat: Add S3 bucket"
git push origin feature/add-s3-bucket

# Open PR on GitHub
# AI will automatically review and comment on security issues!
```

**AI will detect:**
- ❌ Missing encryption
- ❌ No versioning enabled
- ❌ Public access not blocked
- ❌ Missing required tags

### Feature 2: AI Policy Generation

**Generate OPA policies from natural language:**

```bash
cd ai-assistant

# Interactive mode
python3 policy-generator.py --interactive

# Example prompt:
# "Block all EC2 instances without IMDSv2 enabled"

# AI generates complete OPA policy:
package terraform.security

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    resource.change.after.metadata_options[0].http_tokens != "required"
    msg := sprintf("EC2 instance %s does not enforce IMDSv2", [resource.address])
}
```

**Command-line mode:**

```bash
python3 policy-generator.py \
    --requirement "Require encryption for all EBS volumes" \
    --type opa \
    --output ebs-encryption.rego
```

### Feature 3: Local AI Code Analysis

**Review code changes locally:**

```bash
cd ai-assistant

# Make sure Ollama is running
ollama serve &

# Run AI code review
python3 pr-reviewer.py

# Output:
# 🤖 AI-Powered PR Reviewer (Ollama)
# ✅ Connected to Ollama
# 📦 Using model: llama3.1:8b
# 🔍 Analyzing: terraform/environments/dev/main.tf
# ✅ Complete
```

### Feature 4: Auto-Remediation

**Deploy Lambda functions:**

```bash
chmod +x scripts/deploy-lambdas.sh
./scripts/deploy-lambdas.sh

# Select environment: dev
# Review Terraform plan
# Confirm deployment

# Lambda functions will now automatically:
# ✅ Close open security groups
# ✅ Add missing tags to EC2 instances
# ✅ Enable S3 encryption
# ✅ Enforce IMDSv2 on EC2
```

**Configure auto-fix behavior:**

Edit `terraform/environments/dev/terraform.tfvars`:

```hcl
# Dry-run mode (detect only, don't fix)
auto_fix_enabled = false

# Production mode (auto-fix enabled)
auto_fix_enabled = true
```

### Feature 5: ChatOps Notifications

**Set up Discord notifications:**

```bash
# Get Discord webhook URL
# Server Settings → Integrations → Webhooks → New Webhook

export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Test notification
cd chatops
python3 discord-bot.py

# ✅ Test notification sent successfully!
```

**Set up Slack notifications:**

```bash
# Get Slack webhook URL
# Slack App → Incoming Webhooks → Add New Webhook

export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Test notification
python3 slack-webhook.py
```

**Add to GitHub Actions:**

Edit `.github/workflows/terraform-apply.yml`:

```yaml
- name: Notify Deployment
  env:
    DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
  run: |
    python3 chatops/notifications.py \
      --type deployment \
      --data '{
        "status": "success",
        "environment": "dev",
        "pr_number": "${{ github.event.pull_request.number }}",
        "commit_sha": "${{ github.sha }}"
      }'
```

---

## Cost Analysis

### Monthly Cost Breakdown (Personal Project)

| Service | Free Tier | Typical Usage | Cost |
|---------|-----------|---------------|------|
| **GitHub Actions** | 2,000 min/month | ~500 min | $0 |
| **AWS Lambda** | 1M requests | ~10K requests | $0 |
| **AWS EventBridge** | 14M events | ~1M events | $0 |
| **CloudWatch** | 10 metrics | 10 metrics | $0 |
| **SNS** | 1M publishes | ~1K publishes | $0 |
| **DynamoDB** | 25GB storage | <1GB | $0 |
| **S3** | 5GB storage | <1GB | $0 |
| **Ollama (Local AI)** | Unlimited | Unlimited | $0 |
| **TFLint/tfsec/OPA** | Open source | Unlimited | $0 |
| **Discord/Slack** | Webhooks | Unlimited | $0 |
| **TOTAL** | | | **$0/month** 🎉 |

### If You Exceed Free Tier

Worst case scenario (very heavy usage):

- Lambda overages: $1-3/month
- CloudWatch logs: $1-2/month
- Data transfer: $0.50-1/month

**Maximum: $5-6/month**

---

## Troubleshooting

### Issue: Ollama not connecting

```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve &

# Check connection
curl http://localhost:11434/api/tags
```

### Issue: AI model not found

```bash
# List installed models
ollama list

# Pull LLaMA 3.1 if missing
ollama pull llama3.1:8b

# Try alternative models
ollama pull codellama:7b  # Smaller, faster
ollama pull mistral:7b    # Good alternative
```

### Issue: AWS Lambda deployment fails

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check Terraform state
cd terraform/environments/dev
terraform state list

# Re-initialize if needed
rm -rf .terraform
terraform init
```

### Issue: GitHub Actions failing

**Check secrets:**
- Go to: `Settings → Secrets → Actions`
- Verify: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`

**Check workflow logs:**
- Go to: `Actions` tab
- Click on failed workflow
- Expand failed step
- Review error messages

### Issue: Out of memory running AI models

```bash
# Use smaller model
ollama pull mistral:7b  # Only 4.1GB

# Or use quantized version
ollama pull llama3.1:8b-q4_0  # Smaller, still good quality

# Monitor memory usage
htop  # or top
```

---

## Next Steps

1. ✅ **Run the setup script**: `./scripts/setup-ai.sh`
2. ✅ **Test AI locally**: `python3 ai-assistant/pr-reviewer.py`
3. ✅ **Deploy to AWS**: `./scripts/deploy-lambdas.sh`
4. ✅ **Set up notifications**: Configure Discord/Slack webhooks
5. ✅ **Create your first PR**: Test the full workflow

---

## Additional Resources

- **Ollama Documentation**: https://ollama.ai/library
- **LLaMA Models**: https://ollama.ai/library/llama3.1
- **AWS Free Tier**: https://aws.amazon.com/free
- **GitHub Actions**: https://docs.github.com/en/actions
- **OPA Documentation**: https://www.openpolicyagent.org/docs

---

## Support

Need help? Check:

1. [Main SOP](../step_by_step.md)
2. [README](../README.md)
3. GitHub Issues
4. Community Discord

---

**Congratulations! You now have a fully automated, AI-powered DevSecOps pipeline at ZERO cost!** 🚀
