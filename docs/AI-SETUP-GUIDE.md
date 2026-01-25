# ðŸ¤– AI-Powered DevSecOps Setup Guide (FREE Version)

## Complete Guide to Setting Up Local AI for Infrastructure Automation

---

## Table of Contents

1. [Quick Command Reference](#quick-command-reference) â­ **START HERE**
2. [Overview](#overview)
3. [Prerequisites](#prerequisites)
4. [Quick Start (5 Minutes)](#quick-start)
5. [Detailed Setup](#detailed-setup)
6. [Using AI Features](#using-ai-features)
7. [Cost Analysis](#cost-analysis)
8. [Troubleshooting](#troubleshooting)

---

## Quick Command Reference

**â­ Copy and paste these commands to deploy the entire project from scratch!**

### Step 1: Initial Setup (5 minutes)

```bash
# Create workspace and clone repository
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/<your-username>/agentic-devsecops-aws.git
cd agentic-devsecops-aws
chmod +x scripts/*.sh

# Install AWS CLI (choose your OS):
# Linux:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install && rm -rf aws awscliv2.zip

# macOS:
brew install awscli

# Windows Git Bash:
# Download from: https://awscli.amazonaws.com/AWSCLIV2.msi

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, us-east-1, json
```

### Step 2: Install All Tools (10-15 minutes)

```bash
# Run automated setup (installs Terraform, Ollama, security tools, etc.)
./scripts/setup-ai.sh

# Verify installations
terraform --version
aws --version
ollama --version
python3 --version
```

### Step 3: Create AWS Backend Resources

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://your-terraform-state-bucket-$(whoami) --region us-east-1
aws s3api put-bucket-versioning \
  --bucket your-terraform-state-bucket-$(whoami) \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Verify backend resources
aws s3 ls | grep terraform-state
aws dynamodb describe-table --table-name terraform-state-lock
```

### Step 4: Configure Terraform (2 minutes)

```bash
cd terraform/environments/dev

# Update terraform.tfvars with your values
cat > terraform.tfvars << EOF
environment          = "dev"
region              = "us-east-1"
vpc_cidr            = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
instance_type       = "t3.micro"
ami_id              = "ami-0453ec754f44f9a4a"
allowed_ip_ranges   = ["$(curl -s https://api.ipify.org)/32"]
project_name        = "agentic-devsecops"
sns_email           = "your-email@example.com"  # CHANGE THIS!
auto_fix_enabled    = false
EOF

# Update backend.tf with your bucket name
sed -i 's/your-terraform-state-bucket/your-terraform-state-bucket-'$(whoami)'/g' backend.tf
```

### Step 5: Deploy Infrastructure (5-10 minutes)

```bash
# Initialize Terraform
terraform init

# Review plan
terraform plan

# Deploy (creates 25 AWS resources)
terraform apply -auto-approve

# âš ï¸ If you get KMS permission error, add inline KMS policy (see Real-World Deployment section)

# Expected output:
# Apply complete! Resources: 25 added, 0 changed, 0 destroyed.
```

### Step 6: Verify Deployment

```bash
# Check VPC
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=agentic-devsecops-dev-vpc"

# Check Lambda functions
aws lambda list-functions | grep agentic

# Check EventBridge rules
aws events list-rules | grep security

# Check CloudWatch logs
aws logs describe-log-groups | grep lambda

# âš ï¸ CHECK YOUR EMAIL for SNS subscription confirmation!
```

### Step 7: Configure GitHub Secrets

```bash
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/settings/secrets/actions
# Add these secrets:
# - AWS_ACCESS_KEY_ID: <your-access-key>
# - AWS_SECRET_ACCESS_KEY: <your-secret-key>
# - AWS_REGION: us-east-1
```

### Step 8: Test AI Code Review

```bash
cd ~/projects/agentic-devsecops-aws

# Create test branch
git checkout -b test/ai-review

# Make a test change
echo "# Test AI review" >> README.md
git add README.md
git commit -m "test: Trigger AI code review"
git push origin test/ai-review

# Create PR on GitHub and watch AI review in action!
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/pulls
```

### Step 9: Test Lambda Auto-Remediation

```bash
# Trigger a security event (create an overly permissive security group)
aws ec2 create-security-group \
  --group-name test-security-issue \
  --description "Test security group for auto-remediation" \
  --vpc-id $(terraform output -raw vpc_id)

# Add a permissive rule (triggers Lambda)
aws ec2 authorize-security-group-ingress \
  --group-name test-security-issue \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Check Lambda logs (auto-remediation should trigger)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow

# Clean up test security group
aws ec2 delete-security-group --group-name test-security-issue
```

### Step 10: Monitor Costs

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '1 month ago' +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=SERVICE

# Expected: $0-2/month (within free tier)
```

### Step 11: Destroy Infrastructure (when done testing)

```bash
cd terraform/environments/dev

# Destroy all resources
terraform destroy -auto-approve

# Expected: Destroy complete! Resources: 21 destroyed.

# Keep S3 bucket and DynamoDB table for future deployments
# Or delete them if you're done:
aws s3 rb s3://your-terraform-state-bucket-$(whoami) --force
aws dynamodb delete-table --table-name terraform-state-lock
```

**âœ… Complete!** You now have a fully functional AI-powered DevSecOps pipeline!

---

## Overview

This project uses **100% FREE** AI tools to power your DevSecOps workflow:

### What You Get (All FREE!)

âœ… **Local AI Code Review** (Ollama + LLaMA 3.1)
âœ… **Automated Security Scanning** (TFLint, tfsec, Checkov, Trivy)
âœ… **AI Policy Generation** (Natural language â†’ OPA/Sentinel)
âœ… **Auto-Remediation** (AWS Lambda - free tier)
âœ… **ChatOps Notifications** (Discord/Slack webhooks)
âœ… **PR-Driven Deployments** (GitHub Actions - 2000 min/month free)

### Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   GitHub Repository                          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
â”‚  â”‚  Pull Request Created                              â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
â”‚                 â–¼                                            â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
â”‚  â”‚  GitHub Actions Workflows (FREE)                   â”‚     â”‚
â”‚  â”‚  â”œâ”€ AI Code Review (Ollama)                        â”‚     â”‚
â”‚  â”‚  â”œâ”€ Security Scans (TFLint, tfsec, Checkov)        â”‚     â”‚
â”‚  â”‚  â”œâ”€ Terraform Validation                           â”‚     â”‚
â”‚  â”‚  â””â”€ OPA Policy Checks                              â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                  â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   Local AI (Your Machine)                    â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
â”‚  â”‚  Ollama + LLaMA 3.1 (FREE)                         â”‚     â”‚
â”‚  â”‚  â”œâ”€ Code analysis                                  â”‚     â”‚
â”‚  â”‚  â”œâ”€ Security recommendations                       â”‚     â”‚
â”‚  â”‚  â”œâ”€ Policy generation                              â”‚     â”‚
â”‚  â”‚  â””â”€ Best practice suggestions                      â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                  â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   AWS (Free Tier)                            â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
â”‚  â”‚  Lambda Functions (1M requests/month FREE)         â”‚     â”‚
â”‚  â”‚  â”œâ”€ Auto-remediation (fix security issues)         â”‚     â”‚
â”‚  â”‚  â”œâ”€ Security response (isolate threats)            â”‚     â”‚
â”‚  â”‚  â””â”€ Cost optimization                              â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
â”‚                 â–¼                                            â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
â”‚  â”‚  EventBridge (FREE tier)                           â”‚     â”‚
â”‚  â”‚  â”œâ”€ Security group changes                         â”‚     â”‚
â”‚  â”‚  â”œâ”€ EC2 state changes                              â”‚     â”‚
â”‚  â”‚  â””â”€ S3 bucket modifications                        â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                  â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚               ChatOps (Discord/Slack - FREE)                 â”‚
â”‚  â”œâ”€ Deployment notifications                                â”‚
â”‚  â”œâ”€ Security alerts                                         â”‚
â”‚  â”œâ”€ Cost optimization recommendations                       â”‚
â”‚  â””â”€ PR review summaries                                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Prerequisites

Before you begin, ensure you have the following prerequisites ready. This checklist ensures a smooth setup experience.

---

### ðŸ–¥ï¸ System Requirements

#### Operating System
- **Linux**: Ubuntu 20.04+, Debian 11+, or any modern Linux distribution
- **macOS**: macOS 11 (Big Sur) or later
- **Windows**:
  - Option 1: **Git Bash** (Recommended - lightweight, fast)
  - Option 2: **WSL2 with Ubuntu** (Full Linux environment)
  - **NOT supported**: PowerShell or CMD alone

#### Hardware
- **CPU**: 64-bit processor (x86_64 or ARM64)
- **RAM**:
  - Minimum: 8GB
  - Recommended: 16GB (for running AI models smoothly)
  - With GPU: 8GB is sufficient
- **Disk Space**:
  - AI Models (Ollama + LLaMA 3.1): ~5GB
  - Terraform, Security Tools: ~500MB
  - Python dependencies: ~200MB
  - **Total**: 10GB free space minimum
- **GPU** (Optional): NVIDIA GPU with CUDA support (speeds up AI inference)

#### Network
- **Internet Speed**: Stable connection for downloading 5GB+ AI model
- **Firewall**: Allow outbound HTTPS (443) for:
  - AWS API calls
  - GitHub API/repos
  - Docker Hub (if using containers)
  - Ollama model downloads

---

### â˜ï¸ Cloud & Services Prerequisites

#### 1. AWS Account (Required)
- âœ… **Active AWS Account** (Free tier eligible)
- âœ… **IAM User** with programmatic access:
  - Access Key ID
  - Secret Access Key
- âœ… **IAM Policies Attached**:
  - `AmazonEC2FullAccess`
  - `AmazonVPCFullAccess`
  - `AmazonS3FullAccess`
  - `IAMFullAccess`
  - `CloudWatchFullAccess`
  - `AWSLambda_FullAccess`
  - `AmazonEventBridgeFullAccess`
  - `AmazonDynamoDBFullAccess`
- âœ… **S3 Bucket** for Terraform state (unique name)
- âœ… **DynamoDB Table** for state locking (LockID partition key)
- âœ… **Region**: `us-east-1` recommended (or your preferred region)

**Cost**: $0/month (within free tier limits)

#### 2. GitHub Account (Required)
- âœ… **GitHub Account** (Free tier)
- âœ… **Repository Created** (public or private)
- âœ… **GitHub Actions Enabled** (2000 minutes/month free)
- âœ… **Repository Secrets** configured (AWS credentials)

**Cost**: $0/month (2000 Actions minutes free)

#### 3. Slack or Discord (Optional)
- ðŸ”” **Slack Workspace** (for notifications)
  - Free tier workspace
  - Webhook URL from incoming webhook app
- ðŸ”” **Discord Server** (alternative to Slack)
  - Free server
  - Webhook URL from channel settings

**Cost**: $0/month (free tier)

---

### ðŸ› ï¸ Required Software & Tools

The following tools will be **automatically installed** by the setup script, but verify you can install them:

#### 1. Git (Required)
- **Version**: 2.30+
- **Installation**:
  - Linux/macOS: Pre-installed or via package manager
  - Windows: [Git for Windows](https://git-scm.com/download/win) (includes Git Bash)
- **Verify**: `git --version`

#### 2. Python (Required)
- **Version**: Python 3.8+
- **pip**: Included with Python 3.4+
- **Installation**:
  - Linux: `sudo apt install python3 python3-pip`
  - macOS: `brew install python3`
  - Windows: [Python.org](https://www.python.org/downloads/) (check "Add to PATH")
- **Verify**: `python3 --version && pip3 --version`

#### 3. curl & wget (Required)
- **Purpose**: Download files and make API calls
- **Installation**:
  - Linux: `sudo apt install curl wget`
  - macOS: Pre-installed
  - Windows Git Bash: Included
- **Verify**: `curl --version && wget --version`

#### 4. unzip (Required)
- **Purpose**: Extract downloaded archives
- **Installation**:
  - Linux: `sudo apt install unzip`
  - macOS: Pre-installed
  - Windows Git Bash: Included
- **Verify**: `unzip -v`

---

### ðŸ”§ Tools Installed by Setup Script

These will be **automatically installed** when you run `./scripts/setup-ai.sh`:

#### Core Tools
- âœ… **Terraform** 1.6.0+ (Infrastructure as Code)
- âœ… **AWS CLI** v2 (AWS automation)
- âœ… **Ollama** (AI runtime for LLaMA models)
- âœ… **LLaMA 3.1:8b** model (~4.7GB download)

#### Security Scanners
- âœ… **TFLint** (Terraform linter)
- âœ… **tfsec** (Terraform security scanner)
- âœ… **Checkov** (Infrastructure-as-Code security scanner)
- âœ… **Trivy** (Vulnerability scanner)

#### Policy Engine
- âœ… **OPA** (Open Policy Agent)
- âœ… **Conftest** (Policy testing)

#### Python Packages
- âœ… **boto3** (AWS SDK for Python)
- âœ… **requests** (HTTP library)
- âœ… Other dependencies from `requirements.txt`

**Note**: The setup script handles all installations automatically based on your OS.

---

### ðŸ“‹ Pre-Installation Checklist

Before running the automated setup, verify:

- [ ] **Operating System**: Linux, macOS, or Windows Git Bash/WSL2
- [ ] **Git installed**: `git --version` works
- [ ] **Python 3.8+ installed**: `python3 --version` works
- [ ] **pip installed**: `pip3 --version` works
- [ ] **curl/wget installed**: Both commands work
- [ ] **AWS Account created**: You have access to AWS Console
- [ ] **IAM User created**: Access Key ID + Secret Key saved
- [ ] **S3 Bucket created**: For Terraform state storage
- [ ] **DynamoDB Table created**: For state locking
- [ ] **GitHub Account**: Repository ready
- [ ] **8GB RAM minimum**: Check system resources
- [ ] **10GB free disk**: Check available space (`df -h`)
- [ ] **Internet connection**: Stable for large downloads

---

### âš™ï¸ Installation Order

The automated setup follows this sequence:

1. **System Detection** â†’ Identifies your OS (Linux/macOS/Windows)
2. **Package Manager Update** â†’ Updates apt/brew/chocolatey
3. **Core Dependencies** â†’ Installs Python, pip, git, curl
4. **Terraform** â†’ Downloads and installs Terraform 1.6.0
5. **AWS CLI** â†’ Installs AWS CLI v2
6. **Security Tools** â†’ Installs TFLint, tfsec, Checkov, Trivy
7. **Ollama** â†’ Installs Ollama AI runtime
8. **LLaMA Model** â†’ Downloads LLaMA 3.1:8b (~4.7GB)
9. **OPA** â†’ Installs Open Policy Agent
10. **Python Dependencies** â†’ Installs boto3, requests, etc.
11. **Validation** â†’ Verifies all tools installed correctly

**Estimated Time**: 10-15 minutes (depending on internet speed)

---

### ðŸš¨ Common Issues & Solutions

#### Issue: "Permission denied" when running scripts
```bash
# Solution: Make scripts executable
chmod +x scripts/setup-ai.sh
```

#### Issue: Python not found
```bash
# Windows: Add Python to PATH during installation
# Linux/macOS: Install via package manager
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3                   # macOS
```

#### Issue: Insufficient disk space
```bash
# Check available space
df -h

# Free up space (remove old packages, downloads, etc.)
# Minimum 10GB required for full setup
```

#### Issue: AWS credentials not working
```bash
# Verify credentials
aws sts get-caller-identity

# Reconfigure if needed
aws configure
```

#### Issue: Ollama installation fails on Windows
```powershell
# Option 1: Install via Chocolatey (Recommended)
# First, install Chocolatey if not already installed:
# Visit: https://chocolatey.org/install
# Then run in PowerShell (as Administrator):
choco install ollama

# Option 2: Manual Installation
# Download from: https://ollama.com/download/windows
# Run OllamaSetup.exe installer (1.17GB download)
# Installation path: C:\Users\<username>\AppData\Local\Programs\Ollama\

# IMPORTANT: After installation, restart PowerShell
# Or add to PATH temporarily:
$env:Path += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama"

# Verify installation
ollama --version
# Expected: ollama version is 0.14.1 (or later)

# Pull LLaMA 3.1:8b model (~4.7GB download)
ollama pull llama3.1:8b

# Test the model
ollama run llama3.1:8b "Hello, are you ready?"
# Expected: AI responds with a greeting
```

**Windows-Specific Notes:**
- Use **PowerShell** (not Git Bash) for Ollama commands
- Git Bash doesn't recognize Windows apps in PATH automatically
- Ollama runs as a Windows service after installation
- No need for `ollama serve` on Windows (starts automatically)

#### Issue: OPA installation on Windows

The setup script may fail to install OPA on Windows due to permission issues. Here's how to install it manually:

**Option 1: PowerShell (Recommended)**

```powershell
# Create bin directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$HOME\bin"

# Download OPA for Windows
Invoke-WebRequest -Uri "https://openpolicyagent.org/downloads/latest/opa_windows_amd64.exe" -OutFile "$HOME\bin\opa.exe"

# Add to PATH for current session
$env:Path += ";$HOME\bin"

# Verify installation
opa version
# Expected: Version: 1.12.x or later

# Make PATH permanent (add to PowerShell profile)
Add-Content $PROFILE "`n# Add user bin to PATH`n`$env:Path += ';$HOME\bin'"

# Test OPA policies
cd terraform/environments/dev
opa test ../../../policies/opa/
```

**Option 2: Git Bash**

```bash
# Create bin directory if it doesn't exist
mkdir -p ~/bin

# Download OPA for Windows
curl -L -o ~/bin/opa.exe https://openpolicyagent.org/downloads/latest/opa_windows_amd64.exe

# Make executable
chmod +x ~/bin/opa.exe

# Add to PATH for current session
export PATH="$HOME/bin:$PATH"

# Verify installation
opa version
# Expected: Version: 1.12.x or later

# Make PATH permanent (add to .bashrc)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc

# Test OPA policies
cd terraform/environments/dev
opa test ../../../policies/opa/
```

**Fix OPA Policy Syntax for v1:**

If you get `rego_parse_error: 'if' keyword is required` errors, update your policy files:

```bash
# The newer OPA v1 requires 'if' keyword before rule bodies
# Edit policies/opa/policy.rego and add 'if' before each rule body:

# OLD syntax (deprecated):
allow {
    input.method = "GET"
}

# NEW syntax (OPA v1):
allow if {
    input.method = "GET"
}
```

**Permanent PATH Setup (Windows):**

To make OPA available permanently across all terminals:
1. Press `Win + X` â†’ System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", select `Path` â†’ Click "Edit"
5. Click "New" â†’ Add: `C:\Users\<your-username>\bin`
6. Click OK on all dialogs
7. Restart PowerShell/Git Bash

---

### ðŸŽ¯ What Happens Next?

After completing the prerequisites:

1. **Clone the repository** â†’ Your local workspace
2. **Run setup script** â†’ Automated tool installation
3. **Configure AWS** â†’ Connect to your AWS account
4. **Deploy infrastructure** â†’ Terraform creates VPC, Lambda, etc.
5. **Test AI workflows** â†’ Create PR, watch AI review
6. **Monitor & maintain** â†’ Check Lambda logs, costs

**You're now ready to proceed with the Quick Start!** ðŸ‘‡

---

### Optional (Nice to Have)

- Discord or Slack account (for notifications)
- GPU (speeds up AI inference, but not required)

---

## ðŸ’° Cost Breakdown (Actual Experience)

**After completing this guide, here's your real monthly cost**:

| Service | Cost | Notes |
|---------|------|-------|
| **Ollama AI** | $0/month | Runs locally on your machine |
| **GitHub Actions** | $0/month | 2000 free minutes/month |
| **Terraform State (S3)** | <$0.10/month | Small state files |
| **DynamoDB (State Lock)** | $0/month | On-demand, minimal reads/writes |
| **VPC** | $0/month | No NAT Gateway (using public subnets) |
| **Lambda Functions (2)** | $0/month | Free tier: 1M requests/month |
| **CloudWatch Logs** | ~$0.50/month | 14-day retention, minimal logs |
| **KMS Keys (2)** | $2/month | $1/key/month |
| **SNS Topic** | <$0.01/month | Email notifications |
| **EventBridge Rules (2)** | $0/month | Free |
| **CloudTrail** | ~$2/month | Management events only |
| **TOTAL** | **~$4.50/month** | **Very affordable!** |

**Free Tier Comparison**:
- âœ… First 12 months: Most services covered by AWS Free Tier
- âœ… After 12 months: ~$4.50/month for production-grade DevSecOps

**Cost Savings**:
- âŒ EC2 for AI: $10-50/month (AVOIDED by using local Ollama)
- âŒ Managed NAT Gateway: $32/month (AVOIDED by using public subnets)
- âŒ ChatGPT API: $20-100/month (AVOIDED by using local LLaMA 3.1)

**Total Savings**: ~$60-180/month! ðŸŽ‰

---

## ðŸ’¡ Real-World Deployment Experience

**This section documents the actual deployment process with all issues encountered and solutions.**

### Common Issues You'll Encounter (And How We Fixed Them)

#### Issue 1: KMS Permission Denied (99% of users hit this)
**Error Message:**
```
Error: creating KMS Key: User: arn:aws:iam::YOUR_ACCOUNT:user/agentic-ai
is not authorized to perform: kms:TagResource
```

**Root Cause**: The 10 AWS managed policies don't include KMS permissions.

**Solution**: Add inline KMS policy (takes 30 seconds):
```powershell
# PowerShell
$kmsPolicy = @'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["kms:*"],"Resource":"*"}]}
'@
$kmsPolicy | Out-File kms-policy.json -Encoding ASCII
aws iam put-user-policy --user-name agentic-ai --policy-name KMSAccess --policy-document file://kms-policy.json
Remove-Item kms-policy.json
```

#### Issue 2: Lambda Won't Trigger (CloudTrail Required)
**Symptom**: Security group changes don't trigger Lambda function.

**Root Cause**: EventBridge requires CloudTrail to receive AWS API call events.

**Solution**: Enable CloudTrail (~$2/month):
```powershell
# PowerShell - Complete CloudTrail setup (2 minutes)
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
aws s3 mb s3://agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID --region us-east-1

# Create CloudTrail with proper S3 permissions
aws cloudtrail create-trail --name agentic-devsecops-trail --s3-bucket-name agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID
aws cloudtrail start-logging --name agentic-devsecops-trail
```

#### Issue 3: Terraform Plan Syntax Error (PowerShell vs Bash)
**Error**: `Too many command line arguments`

**Root Cause**: PowerShell doesn't accept `=` in arguments like Bash does.

**Wrong**: `terraform plan -var-file=terraform.tfvars`
**Correct**: `terraform plan -var-file terraform.tfvars` (no equals sign)

#### Issue 4: OPA Installation Fails on Windows
**Error**: `sudo: command not found` or `permission denied`

**Solution**: Manual PowerShell installation:
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\bin"
Invoke-WebRequest -Uri "https://openpolicyagent.org/downloads/latest/opa_windows_amd64.exe" -OutFile "$HOME\bin\opa.exe"
$env:Path += ";$HOME\bin"
Add-Content $PROFILE "`n`$env:Path += ';$HOME\bin'"
```

### Actual Deployment Timeline

| Phase | Duration | What Happens |
|-------|----------|--------------|
| **Prerequisites** | 5 min | AWS account, IAM user, S3 bucket, DynamoDB table |
| **Tool Installation** | 10-15 min | Terraform, AWS CLI, Python, Ollama, OPA |
| **Terraform Init** | 1 min | Download providers and modules |
| **Terraform Plan** | 30 sec | Validate 25 resources |
| **First Apply (Fails)** | 2 min | **KMS permission error** |
| **Fix KMS + Retry** | 3 min | Add inline policy, re-apply |
| **CloudTrail Setup** | 5 min | Enable logging for Lambda triggers |
| **Test Ollama** | 2 min | Verify AI code reviews work |
| **Total Time** | **30-35 min** | Fully operational infrastructure |

### Real Cost After Deployment

```
Monthly AWS Bill Breakdown:
â”œâ”€ VPC (public subnets)      $0.00   (no NAT Gateway)
â”œâ”€ Lambda (2 functions)      $0.00   (free tier: 1M requests/month)
â”œâ”€ S3 (Terraform state)      $0.05   (tiny state files)
â”œâ”€ DynamoDB (state lock)     $0.00   (on-demand, minimal usage)
â”œâ”€ CloudWatch Logs           $0.50   (14-day retention)
â”œâ”€ KMS Keys (2)              $2.00   ($1/key/month)
â”œâ”€ CloudTrail                $2.00   (management events)
â”œâ”€ SNS (email)               $0.01   (minimal notifications)
â””â”€ EventBridge               $0.00   (free)
                             â”€â”€â”€â”€â”€
TOTAL:                       ~$4.56/month

Ollama (Local AI):           $0.00   (runs on your laptop)
GitHub Actions:              $0.00   (2000 free minutes/month)

GRAND TOTAL:                 ~$4.56/month ðŸŽ‰
```

**Avoided Costs** by using local Ollama instead of cloud AI:
- âŒ EC2 instance for AI: $10-50/month
- âŒ ChatGPT API calls: $20-100/month
- âŒ Total savings: **$30-150/month**

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

You have **TWO OPTIONS**: Use AWS Console (easier for beginners) OR use AWS CLI (faster for experienced users).

---

### **OPTION A: AWS Console (Recommended for Beginners)**

#### **1.1: Create IAM User via Console**

1. **Log in to AWS Console**: https://console.aws.amazon.com
2. **Navigate to IAM**: Search for "IAM" in the top search bar â†’ Click **IAM**
3. **Create User**:
   - Click **Users** (left sidebar) â†’ **Create user**
   - **User name**: `agentic-ai` (or your preferred name)
   - âœ… Check **"Provide user access to the AWS Management Console"** - Optional
   - âœ… Check **"I want to create an IAM user"**
   - Click **Next**

4. **Attach Policies Directly**:
   - Select **"Attach policies directly"**
   - Search and select these **10 managed policies**:
     1. `AmazonEC2FullAccess`
     2. `AmazonVPCFullAccess`
     3. `AmazonS3FullAccess`
     4. `IAMFullAccess`
     5. `CloudWatchLogsFullAccess`
     6. `CloudWatchEventsFullAccess`
     7. `AWSLambda_FullAccess`
     8. `AmazonEventBridgeFullAccess`
     9. `AmazonDynamoDBFullAccess`
     10. `AmazonSNSFullAccess`

   âš ï¸ **Note**: You'll add **KMS** and **CloudTrail** permissions later via inline policies (Step 8.5 and 8.8)

   - Click **Next** â†’ **Create user**

5. **Create Access Keys**:
   - Click on the newly created user (`agentic-ai`)
   - Go to **"Security credentials"** tab
   - Scroll to **"Access keys"** section
   - Click **"Create access key"**
   - Select **"Command Line Interface (CLI)"**
   - âœ… Check **"I understand the above recommendation..."**
   - Click **Next** â†’ **Create access key**

6. **ðŸ’¾ SAVE YOUR CREDENTIALS IMMEDIATELY**:
   ```
   Access Key ID: AKIAIOSFODNN7EXAMPLE
   Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   ```
   - Click **"Download .csv file"** (recommended)
   - âš ï¸ **CRITICAL**: You cannot retrieve the Secret Access Key later!
   - Store in a password manager (1Password, LastPass, etc.)

#### **1.2: Create S3 Bucket via Console**

1. **Navigate to S3**: Search "S3" â†’ Click **S3**
2. **Create Bucket**:
   - Click **"Create bucket"**
   - **Bucket name**: `agentic-devsecops-terraform-state-<YOUR-INITIALS>-<RANDOM-NUMBER>`
     - Example: `agentic-devsecops-terraform-state-jd-8472`
     - Must be globally unique (try adding random numbers if taken)
   - **Region**: `us-east-1` (or your preferred region)
   - **Block Public Access**: Leave all checkboxes âœ… ENABLED (default - secure!)
   - **Bucket Versioning**: Click **Enable** (required for state recovery)
   - **Default encryption**:
     - Select **Server-side encryption with Amazon S3 managed keys (SSE-S3)**
     - Click **Enable**
   - Click **"Create bucket"**

3. **Verify Bucket Created**:
   - You should see your bucket in the list
   - Click on it â†’ Check "Versioning" shows **Enabled**

#### **1.3: Create DynamoDB Table via Console**

1. **Navigate to DynamoDB**: Search "DynamoDB" â†’ Click **DynamoDB**
2. **Create Table**:
   - Click **"Create table"**
   - **Table name**: `terraform-state-lock`
   - **Partition key**: `LockID` (exactly as written, case-sensitive)
   - **Partition key type**: Select **String**
   - **Table settings**: Leave as **Default settings** (on-demand pricing)
   - Click **"Create table"**

3. **Wait for Table Creation** (takes 10-30 seconds):
   - Status will change from "Creating" to **Active**
   - Once active, you're ready to proceed!

---

### **OPTION B: AWS CLI (For Experienced Users)**

#### **Prerequisites**:
- You must have **root user** or **admin user** credentials already configured
- Run `aws configure` first with admin credentials

#### **1.1: Create IAM User via CLI**

```bash
# PowerShell:
# Create IAM user
aws iam create-user --user-name agentic-ai

# Attach managed policies (all 10 required policies)
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/CloudWatchEventsFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess

# Create access key
aws iam create-access-key --user-name agentic-ai

# Expected output (SAVE THIS IMMEDIATELY):
# {
#     "AccessKey": {
#         "UserName": "agentic-ai",
#         "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
#         "Status": "Active",
#         "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
#         "CreateDate": "2024-01-15T10:30:00Z"
#     }
# }

# âš ï¸ SAVE AccessKeyId and SecretAccessKey immediately!

# Verify policies attached
aws iam list-attached-user-policies --user-name agentic-ai
# Expected: Should list all 10 policies

# Git Bash (same commands work):
aws iam create-user --user-name agentic-ai
aws iam attach-user-policy --user-name agentic-ai --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
# ... (repeat all attach-user-policy commands)
aws iam create-access-key --user-name agentic-ai
```

#### **1.2: Create S3 Bucket via CLI**

```bash
# PowerShell & Git Bash:
# Set your bucket name (must be globally unique!)
$BUCKET_NAME = "agentic-devsecops-terraform-state-jd-8472"  # PowerShell
# OR
BUCKET_NAME="agentic-devsecops-terraform-state-jd-8472"  # Git Bash

# Create S3 bucket in us-east-1
aws s3 mb s3://$BUCKET_NAME --region us-east-1
# Expected: make_bucket: agentic-devsecops-terraform-state-jd-8472

# Enable versioning (REQUIRED for Terraform state recovery)
aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled

# Enable server-side encryption
aws s3api put-bucket-encryption --bucket $BUCKET_NAME --server-side-encryption-configuration '{
  "Rules": [
    {
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": false
    }
  ]
}'

# Verify bucket created and versioning enabled
aws s3api get-bucket-versioning --bucket $BUCKET_NAME
# Expected: { "Status": "Enabled" }

# Block public access (security best practice)
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Verify bucket exists
aws s3 ls | grep agentic-devsecops
# Expected: Shows your bucket in the list
```

#### **1.3: Create DynamoDB Table via CLI**

```bash
# PowerShell & Git Bash:
# Create DynamoDB table for Terraform state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Expected output:
# {
#     "TableDescription": {
#         "TableName": "terraform-state-lock",
#         "TableStatus": "CREATING",
#         "KeySchema": [...],
#         "BillingModeSummary": {
#             "BillingMode": "PAY_PER_REQUEST"
#         }
#     }
# }

# Wait for table to become active (takes 10-30 seconds)
aws dynamodb wait table-exists --table-name terraform-state-lock

# Verify table is active
aws dynamodb describe-table --table-name terraform-state-lock --query "Table.TableStatus"
# Expected: "ACTIVE"

# List tables to confirm
aws dynamodb list-tables
# Expected: Shows "terraform-state-lock" in the list
```

---

### **ðŸ“‹ Step 1 Completion Checklist**

Before proceeding to Step 2, verify you have:

- [ ] âœ… IAM user created: `agentic-ai` (or your chosen name)
- [ ] âœ… 10 managed policies attached to user
- [ ] âœ… Access Key ID saved securely
- [ ] âœ… Secret Access Key saved securely
- [ ] âœ… S3 bucket created with unique name
- [ ] âœ… S3 bucket versioning enabled
- [ ] âœ… S3 bucket encryption enabled
- [ ] âœ… DynamoDB table created: `terraform-state-lock`
- [ ] âœ… DynamoDB table status: ACTIVE
- [ ] âœ… All resources in same region (us-east-1 recommended)

**Save these values for later steps**:
```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET_NAME=agentic-devsecops-terraform-state-jd-8472
DYNAMODB_TABLE=terraform-state-lock
AWS_REGION=us-east-1
```

---
##### Step 2: Choose Your Deployment Environment

**IMPORTANT**: You will run all commands on your **LOCAL MACHINE** (laptop/desktop), not on AWS EC2.

**Why Local and Not EC2?**

âœ… **Local Machine (Recommended)**:
- Ollama AI models run locally (free, no compute costs)
- Easy development workflow (edit code, test, commit)
- Direct access to your IDE and tools
- GitHub Actions handles AWS deployments remotely
- No EC2 costs ($0/month vs $10-50/month for EC2)

âŒ **EC2 Instance (NOT Recommended)**:
- Additional costs (~$10-50/month for compute)
- Requires SSH access and remote development
- More complex setup (VPN, security groups, SSH keys)
- Still need local machine for development anyway

**Architecture Flow**:
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  YOUR LOCAL MACHINE (Development)                   â”‚
â”‚  â”œâ”€ Clone repo                                      â”‚
â”‚  â”œâ”€ Ollama + LLaMA 3.1 (AI runs here)              â”‚
â”‚  â”œâ”€ AWS CLI (configured with credentials)          â”‚
â”‚  â”œâ”€ Terraform (deploys to AWS from here)           â”‚
â”‚  â”œâ”€ Git (push code to GitHub)                      â”‚
â”‚  â””â”€ Code editor (VS Code, etc.)                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚
               â–¼ (git push)
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  GITHUB (Code Repository & CI/CD)                   â”‚
â”‚  â”œâ”€ GitHub Actions (runs workflows)                â”‚
â”‚  â”œâ”€ Security scans                                  â”‚
â”‚  â””â”€ Terraform apply (via Actions)                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚
               â–¼ (terraform apply)
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  AWS (Production Infrastructure)                    â”‚
â”‚  â”œâ”€ Lambda functions                                â”‚
â”‚  â”œâ”€ VPC, EC2, Security Groups                      â”‚
â”‚  â”œâ”€ EventBridge, CloudWatch                        â”‚
â”‚  â””â”€ S3, DynamoDB                                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Summary**:
- **Setup & Development**: Your local machine
- **CI/CD & Automation**: GitHub Actions (free)
- **Production Infrastructure**: AWS (deployed via Terraform)

---

##### Step 3: Prepare Your Local Machine

Choose your operating system:

<details>
<summary><b>ðŸ§ Linux (Ubuntu/Debian)</b></summary>

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y

# Install required tools
sudo apt install -y git curl wget unzip python3 python3-pip

# Verify installations
git --version
python3 --version
curl --version
```
</details>

<details>
<summary><b>ðŸŽ macOS</b></summary>

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install git curl wget python3

# Verify installations
git --version
python3 --version
curl --version
```
</details>

<details>
<summary><b>ðŸªŸ Windows (Option 1: Git Bash - Recommended for Windows Users)</b></summary>

**Git Bash** provides a Linux-like terminal on Windows without WSL2. This is the easiest option for Windows users.

```bash
# Step 1: Download and Install Git for Windows
# Visit: https://git-scm.com/download/win
# Download the installer (64-bit recommended)
# During installation:
#   âœ… Check "Git Bash Here"
#   âœ… Check "Git from the command line and also from 3rd-party software"
#   âœ… Use default options for everything else

# Step 2: Launch Git Bash
# Right-click anywhere â†’ "Git Bash Here"
# Or: Start Menu â†’ "Git Bash"

# Step 3: Verify Git Bash is working
git --version
# Expected: git version 2.x.x

# Step 4: Install Python (if not already installed)
# Download Python from: https://www.python.org/downloads/
# During installation:
#   âš ï¸ IMPORTANT: Check "Add Python to PATH"
#   Install with default options

# Step 5: Verify Python in Git Bash
python --version || python3 --version
# Expected: Python 3.x.x

# Step 6: Install pip (Python package manager)
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm get-pip.py

# Step 7: Verify installations
python --version
pip --version
git --version
curl --version

# Step 8: Set up aliases for Linux-style commands (optional but helpful)
cat >> ~/.bashrc << 'EOF'
# Aliases for Linux-style commands
alias python=python3
alias pip=pip3
alias ll='ls -la'
alias cls=clear
EOF

# Reload bash configuration
source ~/.bashrc

# âœ… Git Bash is ready!
# You can now run all Linux commands in the rest of this guide
```

**Advantages of Git Bash**:
- âœ… No system restart required (unlike WSL2)
- âœ… Lightweight and fast
- âœ… Native Windows integration
- âœ… Run Linux commands directly (bash, curl, grep, etc.)
- âœ… Perfect for this project

**Note**: All commands in this guide work in Git Bash!

</details>

<details>
<summary><b>ðŸªŸ Windows (Option 2: WSL2 - Ubuntu)</b></summary>

**WSL2** provides a full Linux environment on Windows. Use this if you prefer a complete Linux subsystem.

```bash
# Install WSL2 (run in PowerShell as Administrator)
wsl --install Ubuntu

# Restart your computer when prompted

# After restart, open Ubuntu from Start Menu
# Update and install tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget unzip python3 python3-pip

# Verify installations
git --version
python3 --version
curl --version
```
</details>

---

##### Step 4: Clone and Configure Repository

```bash
# Create a workspace directory (recommended)
mkdir -p ~/projects
cd ~/projects

# Clone the repository to your local machine (replace <your-username>)
git clone https://github.com/<your-username>/agentic-devsecops-aws.git
cd agentic-devsecops-aws

# Verify you're in the right directory
pwd
# Should show: /home/yourusername/projects/agentic-devsecops-aws

# Make setup script executable
chmod +x scripts/setup-ai.sh

# Optional: Open in your favorite code editor
# code .  # For VS Code
# or just: ls -la  # to see all files
```

**What you cloned**:
- `ai-assistant/` - AI code reviewer and policy generator
- `terraform/` - Infrastructure as Code modules
- `lambda/` - Auto-remediation functions
- `scripts/` - Setup automation scripts
- `.github/workflows/` - CI/CD pipelines
- `docs/` - Documentation (you're reading it!)

---

##### Step 5: Configure AWS Credentials on Your Local Machine

**This configures AWS CLI to communicate with your AWS account from your laptop/desktop.**

```bash
# Install AWS CLI v2 (choose your OS)

# For Linux:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# For macOS:
brew install awscli

# For Windows WSL2:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Verify installation
aws --version
# Expected: aws-cli/2.x.x Python/3.x.x

# Configure AWS credentials (from Step 1)
aws configure
```

**Interactive Prompts** (use credentials from Step 1):
```
AWS Access Key ID [None]: <paste your Access Key ID>
AWS Secret Access Key [None]: <paste your Secret Access Key>
Default region name [None]: us-east-1
Default output format [None]: json
```

**Verify AWS Configuration**:
```bash
# Test AWS connection
aws sts get-caller-identity

# Expected output:
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/terraform-deployer"
}

# Check your configured region
aws configure get region
# Should output: us-east-1

# List S3 buckets to confirm access
aws s3 ls
# Should show your terraform state bucket from Step 1
```

âœ… **Success**: You can now deploy infrastructure to AWS from your local machine!

---

##### Step 6: Verify Backend Configuration

The Terraform backend is already configured to use S3 for remote state management.

```bash
# View the backend configuration
cat terraform/environments/dev/backend.tf

# Expected output:
# terraform {
#   backend "s3" {
#     bucket         = "your-terraform-state-bucket"  # Your actual bucket name
#     key            = "terraform/dev/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "terraform-state-lock"
#     encrypt        = true
#   }
# }
```

**What This Means:**
- **State Storage**: Terraform state is stored in S3 (remote, not local)
- **State Locking**: DynamoDB prevents concurrent modifications
- **Encryption**: State file is encrypted at rest
- **Collaboration**: Team members can share the same state

**Verify S3 Backend Resources**:
```bash
# Check S3 bucket exists
aws s3 ls | grep terraform-state
# Expected: your-terraform-state-bucket

# Check DynamoDB table exists
aws dynamodb describe-table --table-name terraform-state-lock --query "Table.TableName"
# Expected: "terraform-state-lock"

# Check versioning is enabled (important for state recovery)
aws s3api get-bucket-versioning --bucket your-terraform-state-bucket
# Expected: "Status": "Enabled"
```

âœ… **Backend configured**: Terraform will use S3 for state storage!

**Note**: If you created your own S3 bucket in Step 1 with a different name (e.g., `my-company-terraform-state`), you'll need to update `backend.tf`:

```bash
# Only if you used a different bucket name
nano terraform/environments/dev/backend.tf

# Update the bucket line:
# bucket = "your-terraform-state-bucket"

# Then re-initialize:
# terraform init -reconfigure
```

---

##### Step 7: Run the Automated Setup Script

```bash
# Return to project root (if not already there)
cd ~/projects/agentic-devsecops-aws

# Verify setup script exists
ls -lh scripts/setup-ai.sh

# Execute the setup script
./scripts/setup-ai.sh

# The script will automatically:
# âœ… Detect your OS (Linux/macOS/WSL2)
# âœ… Install Python 3, pip, git, curl
# âœ… Install Terraform 1.6.0
# âœ… Install security tools (TFLint, tfsec, Checkov, Trivy)
# âœ… Install Ollama (local AI runtime)
# âœ… Download LLaMA 3.1:8b model (~4.7GB, one-time)
# âœ… Install OPA (Open Policy Agent)
# âœ… Install Python dependencies (requests, boto3, etc.)
# âœ… Set up pre-commit hooks for git
# âœ… Validate all installations

# This will take 10-15 minutes depending on your internet speed
```

**What to expect during installation**:
- Progress bars for downloading Ollama model
- Terraform version check
- Security tool installations
- Python package installations
- Final validation summary

---

##### Step 8: Initialize and Deploy Infrastructure

**8.1: Review Terraform Configuration**

```bash
# Navigate to dev environment
cd terraform/environments/dev

# View the terraform.tfvars configuration
cat terraform.tfvars

# Expected configuration (already set up):
# environment = "dev"
# region = "us-east-1"
# vpc_cidr = "10.0.0.0/16"
# public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
# private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
# instance_type = "t3.micro"
# ami_id = "ami-0453ec754f44f9a4a"  # Amazon Linux 2023
# allowed_ip_ranges = ["203.0.113.45/32", "198.51.100.0/24"]  # UPDATE THIS!
# project_name = "agentic-devsecops"
# sns_email = "your-email@example.com"  # UPDATE THIS!
# auto_fix_enabled = false  # Dry-run mode (safe)
```

**8.2: Update Required Configuration**

âš ï¸ **IMPORTANT**: You must update these values:

```bash
# 1. Get your public IP address
curl https://api.ipify.org
# Example output: 98.207.254.136

# 2. Edit terraform.tfvars
nano terraform.tfvars  # or: vim, code, notepad, etc.

# 3. Update these lines:
# BEFORE:
# allowed_ip_ranges = ["203.0.113.45/32", "198.51.100.0/24"]
# sns_email = "your-email@example.com"

# AFTER (use YOUR values):
# allowed_ip_ranges = ["98.207.254.136/32"]  # Your actual IP
# sns_email = "your-email@example.com"  # Your actual email

# Save and exit (Ctrl+X, Y, Enter in nano)
```

**8.3: Initialize Terraform**

```bash
# Initialize Terraform (downloads providers and modules)
terraform init

# Expected output:
# Initializing modules...
# - lambda_functions in ../../modules/lambda-functions
# - security in ../../modules/security
# - vpc in ../../modules/vpc
#
# Initializing the backend...
# Successfully configured the backend "s3"!
#
# Initializing provider plugins...
# - Using hashicorp/aws v6.28.0
# - Using hashicorp/archive v2.7.1
#
# Terraform has been successfully initialized!
```

**8.4: Review Infrastructure Plan**

```bash
# Generate and review the execution plan
terraform plan

# Expected output summary:
# Plan: 25 to add, 0 to change, 0 to destroy.

# Resources to be created:
#
# VPC & Networking (7 resources):
#   - aws_vpc.main (10.0.0.0/16)
#   - aws_subnet.public[0] (10.0.1.0/24, us-east-1a)
#   - aws_subnet.public[1] (10.0.2.0/24, us-east-1b)
#   - aws_subnet.private[0] (10.0.3.0/24, us-east-1a)
#   - aws_subnet.private[1] (10.0.4.0/24, us-east-1b)
#   - aws_internet_gateway.main
#   - aws_route_table.public + associations
#
# Lambda Functions (14 resources):
#   - aws_lambda_function.auto_remediation (Python 3.11, 256MB)
#   - aws_lambda_function.security_response (Python 3.11, 256MB)
#   - aws_cloudwatch_event_rule.security_group_changes
#   - aws_cloudwatch_event_rule.ec2_state_changes
#   - aws_cloudwatch_event_target (2 targets)
#   - aws_cloudwatch_log_group (2 groups, 14-day retention)
#   - aws_lambda_permission (2 permissions)
#   - aws_iam_role.lambda_role
#   - aws_iam_role_policy.lambda_policy
#   - aws_sns_topic.notifications
#   - aws_sns_topic_subscription.email (your-email@example.com)
```

**8.5: Deploy Infrastructure**

```bash
# PowerShell:
terraform apply -var-file terraform.tfvars

# Git Bash:
terraform apply -var-file terraform.tfvars

# Review the plan, then type 'yes' when prompted
#
# Do you want to perform these actions?
#   Terraform will perform the actions described above.
#   Only 'yes' will be accepted to approve.
#
#   Enter a value: yes

# â³ Deployment in progress...
#
# VPC resources will create first (3-5 seconds):
# aws_vpc.main: Creating...
# aws_vpc.main: Creation complete after 3s [id=vpc-xxxxx]
# aws_subnet.public[0]: Creating...
# aws_subnet.public[1]: Creating...
# aws_internet_gateway.main: Creating...
# aws_route_table.public: Creating...
# aws_route_table_association.public[0]: Creating...
# aws_route_table_association.public[1]: Creating...
```

âš ï¸ **COMMON ERROR**: KMS Permission Denied

If you see this error:
```
Error: creating KMS Key: operation error KMS: CreateKey, https response error
StatusCode: 400, api error AccessDeniedException: User: arn:aws:iam::YOUR_ACCOUNT:user/agentic-ai
is not authorized to perform: kms:TagResource because no identity-based policy allows
the kms:TagResource action
```

**Fix (PowerShell)**:
```powershell
# Create KMS policy file
@'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["kms:*"],
      "Resource": "*"
    }
  ]
}
'@ | Out-File -FilePath kms-policy.json -Encoding ASCII

# Add KMS permissions
aws iam put-user-policy --user-name agentic-ai --policy-name KMSAccess --policy-document file://kms-policy.json

# Verify policy added
aws iam list-user-policies --user-name agentic-ai
# Expected: {"PolicyNames": ["KMSAccess"]}

# Clean up
Remove-Item kms-policy.json

# Retry deployment
terraform apply -var-file terraform.tfvars
```

**Fix (Git Bash)**:
```bash
# Create KMS policy file
cat > kms-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["kms:*"],
      "Resource": "*"
    }
  ]
}
EOF

# Add KMS permissions
aws iam put-user-policy --user-name agentic-ai --policy-name KMSAccess --policy-document file://kms-policy.json

# Verify
aws iam list-user-policies --user-name agentic-ai

# Clean up and retry
rm kms-policy.json
terraform apply -var-file terraform.tfvars
```

**After fixing KMS permissions, deployment will complete**:
```
# KMS keys will create (10-15 seconds each):
module.lambda_functions.aws_kms_key.sns: Creating...
module.lambda_functions.aws_kms_key.cloudwatch: Creating...
module.lambda_functions.aws_kms_key.sns: Creation complete after 10s
module.lambda_functions.aws_kms_key.cloudwatch: Creation complete after 14s

# Lambda functions and other resources:
module.lambda_functions.aws_sns_topic.notifications: Creating...
module.lambda_functions.aws_lambda_function.auto_remediation: Creating...
module.lambda_functions.aws_lambda_function.security_response: Creating...
module.lambda_functions.aws_cloudwatch_log_group.auto_remediation: Creating...
module.lambda_functions.aws_cloudwatch_event_target.security_group_changes: Creating...

# âœ… Success message:
Apply complete! Resources: 25 added, 0 changed, 0 destroyed.
```

**8.6: Verify Deployment Success**

```bash
# PowerShell & Git Bash - Run these comprehensive checks:

# 1. Check VPC creation
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=agentic-devsecops-dev-vpc" --query "Vpcs[0].[VpcId,CidrBlock,State]" --output table
# Expected: vpc-xxxxx | 10.0.0.0/16 | available

# 2. Check Lambda functions (should show 2 functions)
aws lambda list-functions --query "Functions[?contains(FunctionName, 'agentic')].{Name:FunctionName,Runtime:Runtime,Status:State}" --output table
# Expected:
# agentic-devsecops-dev-auto-remediation | python3.11 | Active
# agentic-devsecops-dev-security-response | python3.11 | Active

# 3. Check KMS keys (should show 2 keys with rotation enabled)
aws kms list-aliases --query "Aliases[?contains(AliasName, 'agentic-devsecops')].AliasName" --output table
# Expected:
# alias/agentic-devsecops-dev-cloudwatch
# alias/agentic-devsecops-dev-sns

# 4. Check EventBridge rules (should show 2 rules)
aws events list-rules --query "Rules[?contains(Name, 'agentic-devsecops')].{Name:Name,State:State}" --output table
# Expected:
# agentic-devsecops-dev-ec2-state-changes | ENABLED
# agentic-devsecops-dev-security-group-changes | ENABLED

# 5. Check SNS topic
aws sns list-topics --query "Topics[?contains(TopicArn, 'agentic-devsecops-dev-notifications')]" --output text
# Expected: arn:aws:sns:us-east-1:YOUR_ACCOUNT:agentic-devsecops-dev-notifications

# 6. Check CloudWatch Log Groups
aws logs describe-log-groups --query "logGroups[?contains(logGroupName, 'agentic-devsecops')].{Name:logGroupName,RetentionDays:retentionInDays}" --output table
# Expected:
# /aws/lambda/agentic-devsecops-dev-auto-remediation | 14
# /aws/lambda/agentic-devsecops-dev-security-response | 14

# 7. Count total resources
echo "VPCs: $(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=*agentic*" --query 'Vpcs | length(@)')"
echo "Subnets: $(aws ec2 describe-subnets --filters "Name=tag:Name,Values=*agentic*" --query 'Subnets | length(@)')"
echo "Lambda Functions: $(aws lambda list-functions --query 'Functions[?contains(FunctionName, `agentic`)] | length(@)')"
echo "EventBridge Rules: $(aws events list-rules --query 'Rules[?contains(Name, `agentic`)] | length(@)')"
# Expected: VPCs=1, Subnets=2, Lambda Functions=2, EventBridge Rules=2

# âœ… If all checks pass: You have 25 resources deployed successfully!
```

**8.7: Important Next Step**

âš ï¸ **CHECK YOUR EMAIL**: You should receive an SNS subscription confirmation email within 1-2 minutes.

```
From: AWS Notifications <no-reply@sns.amazonaws.com>
Subject: AWS Notification - Subscription Confirmation

You have chosen to subscribe to the topic:
arn:aws:sns:us-east-1:123456789012:agentic-devsecops-dev-notifications

To confirm this subscription, click or visit the link below:
[Confirm subscription]
```

**You MUST click the confirmation link** to receive Lambda notifications!

---

**8.8: Enable CloudTrail (Required for Lambda Auto-Remediation)**

âš ï¸ **CRITICAL**: The Lambda functions need **CloudTrail** to detect security group changes. Without CloudTrail, EventBridge won't receive API call events.

**Cost Impact**: CloudTrail adds ~$2/month for management events.

**PowerShell Setup**:
```powershell
# Step 1: Add CloudTrail permissions to IAM user
@'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudtrail:*",
        "s3:CreateBucket",
        "s3:PutBucketPolicy",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
'@ | Out-File -FilePath cloudtrail-policy.json -Encoding ASCII

aws iam put-user-policy --user-name agentic-ai --policy-name CloudTrailAccess --policy-document file://cloudtrail-policy.json

# Step 2: Get your AWS account ID
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
Write-Host "Account ID: $ACCOUNT_ID"

# Step 3: Create S3 bucket for CloudTrail logs
aws s3 mb s3://agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID --region us-east-1

# Step 4: Create S3 bucket policy for CloudTrail
@"
{
  ""Version"": ""2012-10-17"",
  ""Statement"": [
    {
      ""Sid"": ""AWSCloudTrailAclCheck"",
      ""Effect"": ""Allow"",
      ""Principal"": {
        ""Service"": ""cloudtrail.amazonaws.com""
      },
      ""Action"": ""s3:GetBucketAcl"",
      ""Resource"": ""arn:aws:s3:::agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID""
    },
    {
      ""Sid"": ""AWSCloudTrailWrite"",
      ""Effect"": ""Allow"",
      ""Principal"": {
        ""Service"": ""cloudtrail.amazonaws.com""
      },
      ""Action"": ""s3:PutObject"",
      ""Resource"": ""arn:aws:s3:::agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID/AWSLogs/$ACCOUNT_ID/*"",
      ""Condition"": {
        ""StringEquals"": {
          ""s3:x-amz-acl"": ""bucket-owner-full-control""
        }
      }
    }
  ]
}
"@ | Out-File -FilePath s3-cloudtrail-policy.json -Encoding ASCII

aws s3api put-bucket-policy --bucket agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID --policy file://s3-cloudtrail-policy.json

# Step 5: Create CloudTrail
aws cloudtrail create-trail --name agentic-devsecops-trail --s3-bucket-name agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID

# Step 6: Start logging
aws cloudtrail start-logging --name agentic-devsecops-trail

# Step 7: Verify CloudTrail is active
aws cloudtrail get-trail-status --name agentic-devsecops-trail --query IsLogging
# Expected: true

# Clean up policy files
Remove-Item cloudtrail-policy.json, s3-cloudtrail-policy.json

Write-Host "âœ… CloudTrail enabled! Lambda will now receive security group change events."
```

**Git Bash Setup**:
```bash
# Step 1: Add CloudTrail permissions
cat > cloudtrail-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudtrail:*",
        "s3:CreateBucket",
        "s3:PutBucketPolicy",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
EOF

aws iam put-user-policy --user-name agentic-ai --policy-name CloudTrailAccess --policy-document file://cloudtrail-policy.json

# Step 2: Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"

# Step 3: Create S3 bucket
aws s3 mb s3://agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID --region us-east-1

# Step 4: Create S3 bucket policy
cat > s3-cloudtrail-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID/AWSLogs/$ACCOUNT_ID/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
EOF

aws s3api put-bucket-policy --bucket agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID --policy file://s3-cloudtrail-policy.json

# Step 5: Create CloudTrail
aws cloudtrail create-trail --name agentic-devsecops-trail --s3-bucket-name agentic-devsecops-cloudtrail-logs-$ACCOUNT_ID

# Step 6: Start logging
aws cloudtrail start-logging --name agentic-devsecops-trail

# Step 7: Verify
aws cloudtrail get-trail-status --name agentic-devsecops-trail --query IsLogging
# Expected: true

# Clean up
rm cloudtrail-policy.json s3-cloudtrail-policy.json

echo "âœ… CloudTrail enabled!"
```

**What CloudTrail Does:**
- ðŸ“ Logs all AWS API calls (who did what, when)
- ðŸ”” Sends events to EventBridge
- âš¡ Triggers Lambda when security groups change
- ðŸ”’ Provides audit trail for compliance

**Note**: CloudTrail events can take 5-15 minutes to appear in EventBridge after an API call.

---

##### Step 9: Configure GitHub Repository Secrets

1. **Go to your GitHub repository**:
   - URL: `https://github.com/<your-username>/agentic-devsecops-aws`

2. **Navigate to Settings**:
   - Click **Settings** tab
   - Click **Secrets and variables** â†’ **Actions**

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

##### Step 9.1: (Optional) Set Up Slack Notifications

If you want to receive deployment and security notifications in Slack, follow these steps:

**1. Create or Access Slack Workspace**:
- Go to https://slack.com
- Sign in to your existing workspace, OR
- Click **"Create a new workspace"** (free tier is fine)

**2. Create a Slack App**:
- Go to https://api.slack.com/apps
- Click **"Create New App"**
- Select **"From scratch"**
- App Name: `Agentic DevSecOps Notifications`
- Pick your workspace from the dropdown
- Click **"Create App"**

**3. Enable Incoming Webhooks**:
- In your app settings, find **"Incoming Webhooks"** in the left sidebar
- Toggle **"Activate Incoming Webhooks"** to **ON**
- Scroll down and click **"Add New Webhook to Workspace"**
- Select the channel where you want notifications (e.g., `#deployments`, `#devops`, or `#general`)
- Click **"Allow"**

**4. Copy Your Webhook URL**:
- After authorization, you'll see your webhook URL
- It looks like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`
- Click the **"Copy"** button to copy the full URL

**5. Add to GitHub Secrets**:
- Go back to: **Settings** â†’ **Secrets and variables** â†’ **Actions**
- Click **"New repository secret"**
- **Name**: `SLACK_WEBHOOK_URL`
- **Value**: Paste your webhook URL
- Click **"Add secret"**

**6. Test the Webhook (Optional)**:
```bash
# In your local repository
cd chatops

# Install Python dependencies (if not already installed)
pip install -r requirements.txt
# Or: python3 -m pip install -r requirements.txt

# Set the webhook URL temporarily (replace with your actual URL)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Test notification
python3 slack-webhook.py
# Expected output: âœ… Test notification sent successfully!

# You should see a test message in your Slack channel!
```

**What Notifications Will You Receive?**
- âœ… Successful deployments
- âŒ Failed deployments
- ðŸ”’ Security alerts
- ðŸ¤– AI code review summaries
- ðŸ’° Cost optimization recommendations

**Note**: Slack notifications are completely optional. Your infrastructure works perfectly without them!

---

##### Step 9.2: Test Ollama AI (Local Code Review)**

**Ollama** is your local AI that performs security code reviews without cloud API costs.

**Step 1: Verify Ollama Installation**

```bash
# PowerShell:
ollama --version
# Expected: ollama version is 0.14.1 or later

# Check installed models
ollama list
# Expected: llama3.1:8b (4.9 GB)

# Git Bash:
ollama --version
ollama list
```

**Step 2: Test Basic AI Response**

```bash
# PowerShell:
ollama run llama3.1:8b "What are the top 3 AWS security best practices?"

# Git Bash:
ollama run llama3.1:8b "What are the top 3 AWS security best practices?"
```

**Expected AI response** (within 2-5 seconds):
```
Here are the top 3 AWS security best practices:

1. **Implement Least Privilege Access**: Use IAM policies to grant users and
   services only the minimum permissions needed. Avoid using root credentials.

2. **Enable Multi-Factor Authentication (MFA)**: Require MFA for all users,
   especially those with administrative access.

3. **Encrypt Data at Rest and in Transit**: Use AWS KMS for encryption keys,
   enable encryption on S3 buckets, RDS databases, and use TLS/SSL for data
   in transit.
```

**Step 3: Test Security Code Analysis**

```bash
# PowerShell:
ollama run llama3.1:8b @'
Review this Terraform code for security issues:

resource "aws_security_group" "test" {
  name = "test-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

What are the risks and recommendations?
'@

# Git Bash:
ollama run llama3.1:8b 'Review this Terraform code for security issues:

resource "aws_security_group" "test" {
  name = "test-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

What are the risks and recommendations?'
```

**Expected AI analysis**:
```
The Terraform code has a critical security vulnerability:

**Risk**: SSH (port 22) is open to the entire internet (0.0.0.0/0), allowing
anyone to attempt connections. This exposes the server to:
- Brute force attacks
- Unauthorized access attempts
- Compliance violations (PCI-DSS, HIPAA)
- Potential data breaches

**Recommendations**:
1. Restrict SSH to specific IP addresses:
   cidr_blocks = ["YOUR_IP/32"]

2. Use a bastion host/jump box for remote access

3. Implement key-based authentication instead of passwords

4. Enable VPC Flow Logs to monitor access attempts

5. Use AWS Systems Manager Session Manager as an alternative to SSH
```

**Step 4: Performance Test**

```bash
# Quick response test (should respond in 2-5 seconds)
# PowerShell:
Measure-Command { ollama run llama3.1:8b "List 3 AWS Lambda best practices" }

# Git Bash:
time ollama run llama3.1:8b "List 3 AWS Lambda best practices"
```

**Expected timing**:
- First query: 3-7 seconds (model loading)
- Subsequent queries: 1-3 seconds (model cached)

**Step 5: Test AI Code Reviewer Script**

âš ï¸ **Note**: The Python script has encoding issues on Windows PowerShell. Use direct Ollama commands instead.

```bash
# Working alternative - Direct AI review:
ollama run llama3.1:8b @'
Analyze this Lambda function for security issues:

import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    bucket = os.environ["BUCKET_NAME"]
    s3.put_object(Bucket=bucket, Key="test.txt", Body="Hello")
    return {"statusCode": 200}

What security improvements would you recommend?
'@
```

**Expected AI recommendations**:
```
Security improvements for this Lambda function:

1. **Add error handling**: Wrap S3 operations in try-except blocks
2. **Validate environment variables**: Check if BUCKET_NAME exists before use
3. **Use least privilege IAM**: Restrict S3 permissions to specific bucket/prefix
4. **Add logging**: Use CloudWatch Logs for audit trail
5. **Encrypt data**: Use SSE-KMS for S3 object encryption
6. **Input validation**: Sanitize any user input before processing
```

**Ollama Status Summary**:
- âœ… **Installation**: Working (version 0.14.1+)
- âœ… **Model**: LLaMA 3.1:8b loaded (4.9 GB)
- âœ… **Response Time**: 2-5 seconds per query
- âœ… **Security Analysis**: Accurate vulnerability detection
- âœ… **Cost**: $0/month (runs locally)
- âœ… **Use Cases**: Code review, security analysis, compliance checks

**Interactive AI Session**:
```bash
# Start interactive chat (exit with /bye)
ollama run llama3.1:8b

# Example prompts to try:
>>> Explain AWS Lambda cold starts
>>> How do I secure an S3 bucket?
>>> What's the difference between security groups and NACLs?
>>> Review this IAM policy for least privilege
```

---

##### Step 10: Test the AI-Powered Workflows

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
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/pulls
# Click "New pull request"
# Select: base: main â† compare: test/ai-review
# Click "Create pull request"
```

**What happens next**:
1. âœ… **GitHub Actions workflows trigger automatically**
2. âœ… **Security scans run** (TFLint, tfsec, Checkov, Trivy)
3. âœ… **Terraform validation** checks syntax and configuration
4. âœ… **OPA policies** validate compliance rules
5. âœ… **Results appear** as workflow status on PR
6. âœ… **Notifications sent** to Discord/Slack (if configured)

**Note about AI Code Review:**
- The AI review runs **locally** on your machine, not in GitHub Actions
- To see AI review output, run `python3 ai-assistant/pr-reviewer.py` locally
- This keeps costs at $0 (no cloud AI API calls needed)

**Workflow Files Fixed (Latest Version):**
- âœ… **terraform-plan.yml**: Now uses correct working directory (`terraform/environments/dev`)
- âœ… **terraform-apply.yml**: Manual trigger only (safety feature), proper AWS credentials
- âœ… **Updated actions**: Using latest versions (v4 for checkout, v3 for Terraform)
- âœ… **Terraform version**: 1.6.0 (matches local version)
- âœ… **Added validation step**: Catches errors before planning

---

##### Step 11: Deploy and Monitor AWS Lambda Functions

**11.1: Verify Lambda Deployment**

After running `terraform apply` in Step 8, verify your Lambda functions are deployed:

```bash
# Check Lambda functions
aws lambda list-functions --query "Functions[?contains(FunctionName, 'agentic')].FunctionName"

# Expected output:
# [
#     "agentic-devsecops-dev-auto-remediation",
#     "agentic-devsecops-dev-security-response"
# ]

# Get function details
aws lambda get-function --function-name agentic-devsecops-dev-auto-remediation

# Expected output shows:
# - Runtime: python3.11
# - Handler: handler.lambda_handler
# - MemorySize: 256
# - Timeout: 300
# - State: Active
```

**11.2: Confirm SNS Email Subscription**

âš ï¸ **IMPORTANT**: You must confirm your email subscription to receive notifications!

```bash
# 1. Check your email inbox (the one you configured in terraform.tfvars)
# Look for: "AWS Notification - Subscription Confirmation"
# From: AWS Notifications <no-reply@sns.amazonaws.com>

# 2. Click the "Confirm subscription" link in the email

# 3. Verify subscription is active
aws sns list-subscriptions-by-topic \
    --topic-arn $(aws sns list-topics --query "Topics[?contains(TopicArn, 'agentic-devsecops-dev-notifications')].TopicArn" --output text)

# Expected output:
# {
#     "Subscriptions": [
#         {
#             "SubscriptionArn": "arn:aws:sns:us-east-1:...",
#             "Owner": "123456789012",
#             "Protocol": "email",
#             "Endpoint": "your-email@example.com",
#             "TopicArn": "arn:aws:sns:us-east-1:...:agentic-devsecops-dev-notifications"
#         }
#     ]
# }
```

**11.3: View Lambda Resources Created**

The `terraform apply` created 14 Lambda-related resources:

| Resource Type | Name | Purpose |
|--------------|------|---------|
| **Lambda Functions** | `auto-remediation` | Automatically fixes security issues |
| | `security-response` | Responds to security events |
| **EventBridge Rules** | `security_group_changes` | Triggers on SG modifications |
| | `ec2_state_changes` | Triggers on EC2 state changes |
| **CloudWatch Log Groups** | `/aws/lambda/...-auto-remediation` | 14-day retention logs |
| | `/aws/lambda/...-security-response` | 14-day retention logs |
| **EventBridge Targets** | Auto-remediation target | Routes SG events to Lambda |
| | Security response target | Routes EC2 events to Lambda |
| **Lambda Permissions** | EventBridge invoke permission | Allows EventBridge to call Lambda |
| **IAM Role** | `lambda_role` | Execution role for Lambda |
| **IAM Policy** | `lambda_policy` | EC2, S3, CloudWatch permissions |
| **SNS Topic** | `notifications` | Email/Slack notifications |
| **SNS Subscription** | Email subscription | Sends emails to your address |

**11.4: Monitor Lambda Logs (Real-Time)**

```bash
# Tail auto-remediation logs (Ctrl+C to exit)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow

# Tail security-response logs
aws logs tail /aws/lambda/agentic-devsecops-dev-security-response --follow

# View recent logs (last 1 hour)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 1h

# View logs with filter pattern (errors only)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation \
    --filter-pattern "ERROR" \
    --follow
```

**11.5: Test Auto-Remediation (Dry-Run Mode)**

By default, `auto_fix_enabled = false` means Lambda will **detect but not fix** issues (safe for testing).

**Test 1: Create Insecure Security Group**

```bash
# Create a security group with open SSH (insecure!)
aws ec2 create-security-group \
    --group-name test-insecure-sg \
    --description "Test security group for Lambda auto-remediation" \
    --vpc-id $(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=agentic-devsecops-dev-vpc" --query "Vpcs[0].VpcId" --output text)

# Get the security group ID
SG_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=test-insecure-sg" --query "SecurityGroups[0].GroupId" --output text)

# Add insecure rule (SSH open to the world - BAD!)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# This triggers: API call â†’ CloudTrail â†’ EventBridge â†’ Lambda
# â³ Note: CloudTrail events take 5-15 minutes to appear in EventBridge
# This is normal AWS CloudTrail delivery latency!
```

**Test 2: Check Lambda Execution**

```bash
# â³ Wait 5-15 minutes for CloudTrail to deliver the event to EventBridge
# This is normal AWS CloudTrail latency - NOT a bug!

# Check if CloudTrail is logging
aws cloudtrail get-trail-status --name agentic-devsecops-trail --query "IsLogging"
# Expected: true

# View Lambda logs (after the CloudTrail delay)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 20m

# Expected log output:
# ðŸ” DETECTION MODE: Auto-fix is DISABLED
# ðŸš¨ Security Issue Detected!
# â”œâ”€ Type: Overly permissive security group
# â”œâ”€ Resource: sg-xxxxx (test-insecure-sg)
# â”œâ”€ Issue: SSH (port 22) open to 0.0.0.0/0
# â”œâ”€ Risk Level: HIGH
# â””â”€ Recommendation: Restrict to specific IP ranges
#
# âš ï¸  Would fix in production mode (auto_fix_enabled = true)
# ðŸ“§ Sending notification to SNS...
```

**Test 3: Check Your Email**

You should receive an email notification:

```
Subject: [DETECTION] Security Issue Found in dev Environment

Body:
Security Group Issue Detected

Resource: sg-xxxxx (test-insecure-sg)
Issue: SSH (port 22) open to 0.0.0.0/0
Severity: HIGH
Environment: dev
Mode: Dry-run (detection only)

Recommendation: Restrict SSH access to specific IP ranges

AWS Console:
https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroups:group-id=sg-xxxxx
```

**Test 4: Verify Security Group Still Has Insecure Rule (Dry-Run)**

```bash
# Check security group rules (should still have 0.0.0.0/0 because dry-run mode)
aws ec2 describe-security-groups --group-ids $SG_ID --query "SecurityGroups[0].IpPermissions"

# Expected output shows SSH still open to 0.0.0.0/0 (not fixed in dry-run)
```

**11.6: Test Auto-Remediation (Production Mode - Auto-Fix)**

âš ï¸ **WARNING**: This will automatically modify AWS resources!

```bash
# Navigate to terraform dev environment
cd terraform/environments/dev

# Edit terraform.tfvars
nano terraform.tfvars  # or: vim, code, etc.

# Change this line:
# auto_fix_enabled = false  â†’  auto_fix_enabled = true

# Apply the change
terraform apply

# Type 'yes' when prompted

# Expected output:
# module.lambda_functions.aws_lambda_function.auto_remediation: Modifying...
# Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

**Now test with auto-fix enabled:**

```bash
# Create another insecure rule
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 3389 \
    --cidr 0.0.0.0/0

# Wait 30-60 seconds

# Check Lambda logs
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 5m

# Expected log output:
# âœ… AUTO-FIX MODE: Enabled
# ðŸš¨ Security Issue Detected!
# â”œâ”€ Type: Overly permissive security group
# â”œâ”€ Resource: sg-xxxxx (test-insecure-sg)
# â”œâ”€ Issue: RDP (port 3389) open to 0.0.0.0/0
# â”œâ”€ Risk Level: CRITICAL
# â””â”€ Action: REMOVING insecure rule
#
# ðŸ”§ Fixing security issue...
# âœ… Successfully removed insecure ingress rule
# âœ… Applied least-privilege access
# ðŸ“§ Notification sent
```

**Verify the fix was applied:**

```bash
# Check security group rules (RDP rule should be REMOVED)
aws ec2 describe-security-groups --group-ids $SG_ID --query "SecurityGroups[0].IpPermissions"

# RDP 0.0.0.0/0 rule should be gone!
```

**11.7: Clean Up Test Resources**

```bash
# Delete test security group
aws ec2 delete-security-group --group-id $SG_ID

# Verify deletion
aws ec2 describe-security-groups --group-ids $SG_ID
# Expected: An error: "does not exist" (this is correct!)
```

**11.8: Monitor Lambda Performance**

```bash
# Get Lambda metrics (invocation count, errors, duration)
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=agentic-devsecops-dev-auto-remediation \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Sum

# Check for errors
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Errors \
    --dimensions Name=FunctionName,Value=agentic-devsecops-dev-auto-remediation \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Sum

# Check average duration (execution time)
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Duration \
    --dimensions Name=FunctionName,Value=agentic-devsecops-dev-auto-remediation \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Average
```

**11.9: View Lambda in AWS Console**

**Option 1: Command Line (opens in browser)**
```bash
# Get Lambda function ARN
LAMBDA_ARN=$(aws lambda get-function \
    --function-name agentic-devsecops-dev-auto-remediation \
    --query "Configuration.FunctionArn" \
    --output text)

echo "Lambda Console: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/agentic-devsecops-dev-auto-remediation"
```

**Option 2: Manual Navigation**
1. Go to: https://console.aws.amazon.com/lambda
2. Region: **us-east-1** (top-right dropdown)
3. Click: **Functions** (left sidebar)
4. Find: `agentic-devsecops-dev-auto-remediation`
5. Explore:
   - **Code** tab: View Lambda function code
   - **Monitor** tab: Invocations, errors, duration graphs
   - **Configuration** tab: Memory, timeout, environment variables
   - **Logs** tab: CloudWatch logs (same as CLI)

**11.10: Cost Tracking (Lambda)**

Lambda is **FREE** for personal use:
- **Free Tier**: 1 million requests/month + 400,000 GB-seconds compute
- **Your Usage**: ~10-100 invocations/month (far below free tier)
- **Cost**: $0/month

```bash
# Check AWS Free Tier usage
# Go to: https://console.aws.amazon.com/billing/home#/freetier
# Filter: Lambda
# Expected: Well under 1M requests/month limit
```

---

##### Step 12: Verify AI Assistant is Running

**12.1: Install Ollama and Pull LLaMA Model**

<details>
<summary><b>ðŸªŸ Windows (PowerShell)</b></summary>

```powershell
# Install Ollama via Chocolatey
choco install ollama

# After installation, restart PowerShell or add to PATH:
$env:Path += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama"

# Verify installation
ollama --version
# Expected: ollama version is 0.14.1 (or later)

# Pull LLaMA 3.1:8b model (~4.7GB, one-time download)
ollama pull llama3.1:8b
# This will take 5-10 minutes depending on internet speed

# Test the model
ollama run llama3.1:8b "Hello, are you ready?"
# Expected output: AI responds with a greeting
# Press Ctrl+D or type /bye to exit
```
</details>

<details>
<summary><b>ðŸ§ Linux / ðŸŽ macOS</b></summary>

```bash
# Install Ollama
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# macOS:
brew install ollama

# Start Ollama service (Linux only)
ollama serve &

# Pull LLaMA 3.1:8b model (~4.7GB)
ollama pull llama3.1:8b

# Test the model
ollama run llama3.1:8b "Hello, are you ready?"
```
</details>

**10.2: Install AI Assistant Dependencies**

```bash
# Navigate to ai-assistant directory
cd ai-assistant

# Install Python dependencies
python3 -m pip install -r requirements.txt
# or: pip install -r requirements.txt

# Expected packages installed:
# - requests>=2.31.0
# - pyyaml>=6.0.1
# - jinja2>=3.1.2
```

**10.3: Test AI Code Reviewer**

```bash
# IMPORTANT: The PR reviewer needs git commits to analyze
# It compares HEAD^ (previous commit) vs HEAD (current commit)

# Option 1: Test with existing commits
python3 pr-reviewer.py
# If you see "No Terraform files changed", create a test commit (Option 2)

# Option 2: Create a test commit
# Create a test branch
cd ..
git checkout -b test/ai-code-review

# Make a small change to Terraform files
cd terraform/environments/dev
echo "# Test comment" >> variables.tf

# Commit the change
git add variables.tf
git commit -m "test: verify AI code reviewer"

# Now run the AI reviewer
cd ../../../ai-assistant
python3 pr-reviewer.py
```

**Expected Output:**
```
ðŸ¤– AI-Powered PR Reviewer (Ollama)
==================================================
âœ… Connected to Ollama at http://localhost:11434
ðŸ“¦ Using model: llama3.1:8b

ðŸ“ Analyzing 1 file(s)...

ðŸ” Analyzing: /path/to/terraform/environments/dev/variables.tf
  âœ… Complete

==================================================
âœ… Review complete! Output saved to: ai_review_output.md

Preview:
## ðŸ¤– AI-Powered Code Review (Ollama)

**Model:** `llama3.1:8b`

âœ… **No issues found!** Code looks good.

---
*AI-powered review using free local models via Ollama.*
```

**10.4: Test AI Policy Generator**

```bash
# Interactive mode
python3 policy-generator.py --interactive

# When prompted, try:
# "Create a policy to block all SSH access from the internet"
# AI will generate complete OPA policy code!

# Example output:
# package terraform.security
#
# deny[msg] {
#     resource := input.resource_changes[_]
#     resource.type == "aws_security_group_rule"
#     resource.change.after.from_port == 22
#     resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
#     msg := "SSH (port 22) should not be open to 0.0.0.0/0"
# }
```

**10.5: View AI Review Output**

```bash
# Open the generated review file
cat ai_review_output.md
# or: code ai_review_output.md  # VS Code
# or: notepad ai_review_output.md  # Windows
```

**Troubleshooting AI Reviewer:**

- **"No Terraform files changed"**: Create a commit with Terraform changes (see Option 2 above)
- **"Ollama is not running"**:
  - Windows: Restart PowerShell, Ollama service starts automatically
  - Linux/Mac: Run `ollama serve &` in background
- **"Model not found"**: Run `ollama pull llama3.1:8b` again
- **UnicodeEncodeError**: This is fixed in the latest version (UTF-8 encoding added)
- **Path not found**: The PR reviewer now works from any directory (fixed in latest update)

---

#### Setup Complete! ðŸŽ‰

Your Agentic AI DevSecOps environment is now fully operational:

âœ… **AWS Infrastructure Deployed**:
- VPC with public/private subnets (10.0.0.0/16)
- Internet Gateway and route tables
- Security groups with least-privilege access
- Lambda functions for auto-remediation
- EventBridge rules monitoring AWS events
- CloudWatch log groups (14-day retention)
- SNS notifications to your email

âœ… **Lambda Auto-Remediation**:
- 2 Lambda functions (auto-remediation, security-response)
- Python 3.11 runtime, 256MB memory, 300s timeout
- EventBridge triggers (security group + EC2 changes)
- IAM roles with appropriate permissions
- Dry-run mode enabled (safe for testing)

âœ… **Local AI Ready**:
- Ollama v0.14.1 installed
- LLaMA 3.1:8b model (~4.7GB) downloaded
- AI code reviewer working
- Policy generator available

âœ… **Security Tools Installed**:
- TFLint (Terraform linting)
- tfsec (security scanning)
- Checkov (compliance checking)
- Trivy (vulnerability scanning)
- OPA (policy validation)

âœ… **GitHub Integration**:
- Repository: <your-username>/agentic-devsecops-aws
- GitHub Actions workflows running
- S3 backend for Terraform state
- DynamoDB state locking
- Automated security scans on PRs

âœ… **ChatOps (Optional)**:
- Slack webhook configured (if you completed Step 7.1)
- SNS email notifications active

**Cost Tracking**: $0/month (all within free tiers)
- Lambda: 1M requests/month free (using ~10-100/month)
- EventBridge: 14M events free (using ~1K/month)
- CloudWatch: 10 metrics free (using 5)
- S3: 5GB free (using <1GB)
- Total: **$0/month** ðŸŽ‰

---

#### What Just Got Deployed?

**Total Resources Created: 21**

| Category | Resources | Description |
|----------|-----------|-------------|
| **Networking** | 7 | VPC, subnets (2 public, 2 private), IGW, route table, associations |
| **Lambda Functions** | 2 | Auto-remediation (370 lines Python), Security-response |
| **EventBridge** | 4 | 2 rules (SG changes, EC2 changes) + 2 targets |
| **CloudWatch Logs** | 2 | Log groups with 14-day retention |
| **Lambda Permissions** | 2 | Allow EventBridge to invoke Lambda |
| **IAM** | 2 | Lambda execution role + policy |
| **SNS** | 2 | Notification topic + email subscription |

**Infrastructure Details:**
```
VPC (10.0.0.0/16, us-east-1)
â”œâ”€â”€ Public Subnets
â”‚   â”œâ”€â”€ 10.0.1.0/24 (us-east-1a)
â”‚   â””â”€â”€ 10.0.2.0/24 (us-east-1b)
â”œâ”€â”€ Private Subnets
â”‚   â”œâ”€â”€ 10.0.3.0/24 (us-east-1a)
â”‚   â””â”€â”€ 10.0.4.0/24 (us-east-1b)
â”œâ”€â”€ Internet Gateway
â””â”€â”€ Route Tables

Lambda Auto-Remediation
â”œâ”€â”€ Function: auto-remediation (Python 3.11, 256MB)
â”‚   â”œâ”€â”€ Trigger: EventBridge (security group changes)
â”‚   â”œâ”€â”€ Trigger: EventBridge (EC2 state changes)
â”‚   â”œâ”€â”€ Logs: CloudWatch (/aws/lambda/...-auto-remediation)
â”‚   â””â”€â”€ Permissions: EC2, S3, CloudWatch access
â”œâ”€â”€ Function: security-response (Python 3.11, 256MB)
â”‚   â”œâ”€â”€ Logs: CloudWatch (/aws/lambda/...-security-response)
â”‚   â””â”€â”€ Permissions: EC2, IAM, CloudWatch access
â”œâ”€â”€ SNS Topic: agentic-devsecops-dev-notifications
â”‚   â””â”€â”€ Email: your-email@example.com (confirmed âœ…)
â””â”€â”€ Mode: Dry-run (auto_fix_enabled = false)
```

---

#### Next Steps

**Immediate Actions (Required):**

1. **âœ… Confirm SNS Email Subscription**
   - Check inbox for "AWS Notification - Subscription Confirmation"
   - Click confirmation link
   - Verify in AWS Console: SNS â†’ Subscriptions â†’ Status should show "Confirmed"

2. **ðŸ§ª Test Lambda Auto-Remediation (Dry-Run)**
   ```bash
   # Create insecure security group to trigger Lambda
   cd terraform/environments/dev

   # See Step 9.5 for complete testing instructions
   # Lambda will DETECT but not fix (safe mode)
   ```

3. **ðŸ“Š Monitor Lambda Logs**
   ```bash
   # Watch Lambda execution in real-time
   aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow

   # Press Ctrl+C to stop
   ```

**Learning & Exploration:**

4. **ðŸ¤– Test AI Code Review**
   ```bash
   # Create a test PR with Terraform changes
   git checkout -b test/lambda-monitoring
   echo "# Monitor Lambda performance" >> README.md
   git add . && git commit -m "docs: Add Lambda monitoring notes"
   git push origin test/lambda-monitoring

   # Open PR on GitHub, watch AI analysis
   ```

5. **ðŸ”’ Create Infrastructure Changes**
   - Modify Terraform files in `terraform/modules/`
   - Open PR â†’ Watch automated security scans
   - See TFLint, tfsec, Checkov, Trivy results
   - Review AI-generated recommendations

6. **ðŸ“œ Customize OPA Policies**
   - Edit policies in `policies/templates/`
   - Examples:
     - `ec2-compliance.rego` - EC2 compliance rules
     - `s3-security.rego` - S3 bucket security
     - `security-group.rego` - Security group validation
   - Test with: `opa test policies/`

7. **ðŸ’¬ Set Up ChatOps** (Optional but Recommended)
   - Complete Step 7.1 for Slack integration
   - Receive notifications for:
     - Lambda auto-remediations
     - Security violations detected
     - Deployment status
     - Cost optimization recommendations

8. **ðŸš€ Enable Auto-Fix Mode** (When Ready)
   ```bash
   # After testing dry-run mode
   cd terraform/environments/dev
   nano terraform.tfvars
   # Change: auto_fix_enabled = false â†’ true
   terraform apply

   # Lambda will now AUTOMATICALLY FIX security issues!
   ```

**Advanced Usage:**

9. **ðŸ“ˆ Monitor Costs in AWS**
   - Go to: https://console.aws.amazon.com/billing/home#/freetier
   - Filter: Lambda, EventBridge, CloudWatch
   - Expected: All within free tier ($0/month)

10. **ðŸ”„ Deploy to Staging** (Optional)
    ```bash
    # Configure staging environment
    cd terraform/environments/staging

    # Update terraform.tfvars with staging values
    nano terraform.tfvars
    # Use different VPC CIDR: 10.1.0.0/16
    # Use different email or same

    # Deploy staging
    terraform init
    terraform plan
    terraform apply
    ```

11. **ðŸ­ Production Deployment** (Portfolio Ready)
    ```bash
    # Deploy to production when ready to showcase
    cd terraform/environments/prod

    # Update terraform.tfvars
    # Use production-grade settings
    # Enable auto-fix for production

    terraform init && terraform plan && terraform apply
    ```

12. **ðŸ“š Document Your Learning**
    - Take screenshots of Lambda logs
    - Document auto-remediation examples
    - Create architecture diagrams
    - Add to portfolio/resume

**Maintenance & Best Practices:**

- **Weekly**: Review CloudWatch logs for anomalies
- **Monthly**: Check AWS Free Tier usage dashboard
- **Quarterly**: Update Terraform modules and providers
- **Regularly**: Pull latest AI model updates (`ollama pull llama3.1:8b`)

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
# Default region: us-east-1
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
`Settings â†’ Secrets and variables â†’ Actions â†’ New repository secret`

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: us-east-1 (or your preferred region)

### Step 10: Enable Branch Protection

Navigate to: `Settings â†’ Branches â†’ Add rule`

For `main` branch:
- âœ… Require pull request reviews (1 approval)
- âœ… Require status checks to pass
- âœ… Require branches to be up to date
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
- âŒ Missing encryption
- âŒ No versioning enabled
- âŒ Public access not blocked
- âŒ Missing required tags

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
# ðŸ¤– AI-Powered PR Reviewer (Ollama)
# âœ… Connected to Ollama
# ðŸ“¦ Using model: llama3.1:8b
# ðŸ” Analyzing: terraform/environments/dev/main.tf
# âœ… Complete
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
# âœ… Close open security groups
# âœ… Add missing tags to EC2 instances
# âœ… Enable S3 encryption
# âœ… Enforce IMDSv2 on EC2
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
# Server Settings â†’ Integrations â†’ Webhooks â†’ New Webhook

export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Test notification
cd chatops
python3 discord-bot.py

# âœ… Test notification sent successfully!
```

**Set up Slack notifications:**

```bash
# Get Slack webhook URL
# Slack App â†’ Incoming Webhooks â†’ Add New Webhook

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
| **TOTAL** | | | **$0/month** ðŸŽ‰ |

### If You Exceed Free Tier

Worst case scenario (very heavy usage):

- Lambda overages: $1-3/month
- CloudWatch logs: $1-2/month
- Data transfer: $0.50-1/month

**Maximum: $5-6/month**

---

## Troubleshooting

### Issue: Lambda not triggering on security group changes

**Symptom**: You created a non-compliant security group, but Lambda didn't execute.

**Root Cause**: EventBridge requires **CloudTrail** to receive AWS API call events.

**Solution**:
```bash
# 1. Check if CloudTrail is enabled
aws cloudtrail describe-trails --query "trailList[?Name=='agentic-devsecops-trail']"

# If no trail exists, enable CloudTrail (see Step 6.8)
# 2. Verify logging is active
aws cloudtrail get-trail-status --name agentic-devsecops-trail --query "IsLogging"
# Expected: true

# 3. Wait 5-15 minutes for CloudTrail event delivery
# This is normal AWS latency - NOT a bug!

# 4. Check EventBridge rules are enabled
aws events list-rules --query "Rules[?contains(Name, 'security-group-changes')].State"
# Expected: ENABLED

# 5. Check Lambda logs after the CloudTrail delay
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 20m --follow
```

### Issue: Python AI reviewer script encoding error (Windows)

**Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f916'`

**Root Cause**: Windows PowerShell uses cp1252 encoding, can't handle Unicode emojis in Python script.

**Solution**: Use direct Ollama commands instead:
```powershell
# Instead of: python pr-reviewer.py
# Use direct Ollama:
ollama run llama3.1:8b "Review this Terraform code: [paste code]"
```

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
- Go to: `Settings â†’ Secrets â†’ Actions`
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
htop  # or top on Linux/Mac
# Task Manager on Windows (Ctrl+Shift+Esc)
```

### Issue: Command not found on Windows

**Problem**: Commands like `terraform`, `ollama`, or `python3` not recognized

**Solution**:

```powershell
# Option 1: Restart PowerShell after installation
# Many installers add to PATH but require terminal restart

# Option 2: Add to PATH temporarily (current session only)
$env:Path += ";C:\Path\To\Your\Program"

# Example for Ollama:
$env:Path += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama"

# Option 3: Use full path
& "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" --version

# Verify PATH contains your programs
$env:Path -split ';' | Select-String "Ollama"
```

### Issue: Lambda not receiving events

**Problem**: Created insecure security group but Lambda didn't trigger

**Solution**:

```bash
# 1. Check EventBridge rules exist
aws events list-rules --query "Rules[?contains(Name, 'agentic')]"

# 2. Check Lambda permissions
aws lambda get-policy --function-name agentic-devsecops-dev-auto-remediation

# 3. Check CloudWatch logs for errors
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 1h

# 4. Verify EventBridge targets
aws events list-targets-by-rule --rule agentic-devsecops-dev-security-group-changes

# 5. Test Lambda directly (manual invocation)
aws lambda invoke \
    --function-name agentic-devsecops-dev-auto-remediation \
    --payload '{"detail":{"eventName":"AuthorizeSecurityGroupIngress"}}' \
    response.json

# View response
cat response.json
```

### Issue: SNS email not received

**Problem**: Didn't receive SNS subscription confirmation or notifications

**Solution**:

```bash
# 1. Check email address in terraform.tfvars
cd terraform/environments/dev
grep sns_email terraform.tfvars
# Should show your correct email

# 2. Check SNS subscription status
aws sns list-subscriptions-by-topic \
    --topic-arn $(aws sns list-topics --query "Topics[?contains(TopicArn, 'agentic-devsecops-dev-notifications')].TopicArn" --output text)

# If "SubscriptionArn" shows "PendingConfirmation", check your spam folder

# 3. Resend confirmation (if needed)
# Delete and recreate subscription:
terraform taint module.lambda_functions.aws_sns_topic_subscription.email
terraform apply

# 4. Check spam/junk folder for:
# From: AWS Notifications <no-reply@sns.amazonaws.com>
# Subject: AWS Notification - Subscription Confirmation
```

### Issue: Lambda function errors

**Problem**: Lambda showing errors in CloudWatch logs

**Solution**:

```bash
# 1. View error logs
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation \
    --filter-pattern "ERROR" \
    --since 1h

# 2. Check IAM permissions
aws lambda get-function --function-name agentic-devsecops-dev-auto-remediation \
    --query "Configuration.Role"

# Get role details
aws iam get-role --role-name <role-name-from-above>

# 3. Verify Lambda environment variables
aws lambda get-function-configuration \
    --function-name agentic-devsecops-dev-auto-remediation \
    --query "Environment"

# 4. Check function code integrity
aws lambda get-function \
    --function-name agentic-devsecops-dev-auto-remediation \
    --query "Code.Location"

# 5. Redeploy Lambda (if code is corrupted)
cd terraform/environments/dev
terraform taint module.lambda_functions.aws_lambda_function.auto_remediation
terraform apply
```

### Issue: Terraform provider version conflicts

**Problem**: `Error: locked provider ... does not match configured version constraint`

**Solution**:

```bash
# Example error:
# locked provider hashicorp/aws 6.28.0 does not match
# configured version constraint ~> 5.0

# This means different modules require different AWS provider versions

# 1. Check current provider versions
terraform version

# 2. Update all modules to use compatible versions
# Edit terraform/modules/lambda-functions/main.tf:
# Change: version = "~> 5.0"
# To:     version = "~> 6.0"

# 3. Re-initialize Terraform
terraform init -upgrade

# 4. If still failing, remove lock file and re-init
rm .terraform.lock.hcl
terraform init
```

### Issue: Auto-fix not working (dry-run mode stuck)

**Problem**: Lambda detects issues but doesn't fix them

**Solution**:

```bash
# Verify auto-fix mode setting
cd terraform/environments/dev
grep auto_fix_enabled terraform.tfvars

# Should show:
# auto_fix_enabled = false  # Dry-run (detect only)
# or
# auto_fix_enabled = true   # Auto-fix (production mode)

# To enable auto-fix:
nano terraform.tfvars
# Change: auto_fix_enabled = false
# To:     auto_fix_enabled = true

# Apply the change
terraform apply

# Verify Lambda received the updated environment variable
aws lambda get-function-configuration \
    --function-name agentic-devsecops-dev-auto-remediation \
    --query "Environment.Variables.AUTO_FIX_ENABLED"
# Should output: "true"
```

### Issue: High Lambda costs

**Problem**: Concerned about Lambda charges

**Solution**:

```bash
# Check Lambda invocation count
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=agentic-devsecops-dev-auto-remediation \
    --start-time $(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 2592000 \
    --statistics Sum

# Compare to free tier: 1,000,000 requests/month

# Check AWS Cost Explorer
# https://console.aws.amazon.com/cost-management/home#/custom

# Filter by:
# - Service: Lambda
# - Time: Last 30 days

# Expected for personal use: $0 (within free tier)

# If charges appear:
# - Reduce Lambda timeout (currently 300s)
# - Reduce memory (currently 256MB)
# - Add EventBridge filters to reduce invocations
```



### Windows Best Practices

**Use the Right Terminal for Each Tool:**

| Tool | Use Terminal | Why |
|------|-------------|-----|
| **Ollama** | PowerShell | Windows app, needs Windows PATH |
| **Git** | Git Bash | Better git integration |
| **Terraform** | Git Bash or PowerShell | Works in both |
| **Python** | PowerShell or Git Bash | Works in both |
| **AWS CLI** | PowerShell or Git Bash | Works in both |

**Quick Setup for Windows Users:**

```powershell
# 1. Install core tools via Chocolatey (PowerShell as Admin)
choco install git python terraform awscli ollama -y

# 2. Restart PowerShell (important!)
# Close and reopen PowerShell

# 3. Verify installations
git --version
python --version
terraform --version
aws --version
ollama --version

# 4. Pull AI model (PowerShell)
ollama pull llama3.1:8b

# 5. Use Git Bash for git/terraform work
# Right-click in project folder â†’ "Git Bash Here"

# 6. Use PowerShell for Ollama/AI work
# In project folder: Shift+Right-click â†’ "Open PowerShell window here"
```

**Line Ending Warning (Windows Git Bash):**

You may see: `warning: LF will be replaced by CRLF`

This is normal and safe. Git automatically converts line endings for Windows.

**To disable the warning**:
```bash
git config --global core.autocrlf true
```

---

## Next Steps

1. âœ… **Run the setup script**: `./scripts/setup-ai.sh`
2. âœ… **Test AI locally**: `python3 ai-assistant/pr-reviewer.py`
3. âœ… **Deploy to AWS**: `./scripts/deploy-lambdas.sh`
4. âœ… **Set up notifications**: Configure Discord/Slack webhooks
5. âœ… **Create your first PR**: Test the full workflow

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

## Complete Project Workflow (End-to-End Commands)

**ðŸš€ Run this entire workflow to go from zero to fully deployed!**

### Phase 1: Initial Setup (One-Time)

```bash
# 1. Clone and enter repository
git clone https://github.com/<your-username>/agentic-devsecops-aws.git
cd agentic-devsecops-aws

# 2. Configure AWS CLI
aws configure
# Enter: Access Key, Secret Key, us-east-1, json

# 3. Create S3 backend
aws s3 mb s3://my-terraform-state-$(whoami) --region us-east-1
aws s3api put-bucket-versioning --bucket my-terraform-state-$(whoami) \
  --versioning-configuration Status=Enabled

# 4. Create DynamoDB table
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# 5. Install all tools
chmod +x scripts/*.sh
./scripts/setup-ai.sh

# 6. Configure terraform.tfvars
cd terraform/environments/dev
cat > terraform.tfvars << EOF
environment = "dev"
region = "us-east-1"
vpc_cidr = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
instance_type = "t3.micro"
ami_id = "ami-0453ec754f44f9a4a"
allowed_ip_ranges = ["$(curl -s https://api.ipify.org)/32"]
project_name = "agentic-devsecops"
sns_email = "your-email@example.com"
auto_fix_enabled = false
EOF

# 7. Update backend configuration
sed -i 's/your-terraform-state-bucket/my-terraform-state-'$(whoami)'/g' backend.tf
```

### Phase 2: Infrastructure Deployment

```bash
# 8. Initialize and deploy
terraform init
terraform plan
terraform apply -auto-approve

# 9. Confirm SNS email (check inbox!)

# 10. Verify deployment
aws lambda list-functions | grep agentic
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=agentic-devsecops-dev-vpc"
```

### Phase 3: Testing & Validation

```bash
# 11. Test Lambda auto-remediation
SG_ID=$(aws ec2 create-security-group \
  --group-name test-insecure-sg \
  --description "Test SG" \
  --vpc-id $(terraform output -raw vpc_id) \
  --query 'GroupId' --output text)

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0

# 12. Check Lambda logs
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow

# 13. Clean up test resource
aws ec2 delete-security-group --group-id $SG_ID

# 14. Test AI code review
cd ~/projects/agentic-devsecops-aws
git checkout -b test/ai-review
echo "# Test change" >> README.md
git add . && git commit -m "test: AI review"
git push origin test/ai-review

# 15. Run AI reviewer locally
cd ai-assistant
python3 pr-reviewer.py
cat ai_review_output.md
```

### Phase 4: GitHub Integration

```bash
# 16. Set GitHub Secrets
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/settings/secrets/actions
# Add: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

# 17. Create PR on GitHub
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/pulls
# Click "New pull request"
# Watch automated workflows run!
```

### Phase 5: Monitoring & Maintenance

```bash
# 18. Monitor costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '1 month ago' +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost

# 19. View Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=agentic-devsecops-dev-auto-remediation \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Sum

# 20. Check overall health
aws lambda list-functions --query 'Functions[*].[FunctionName,State,LastUpdateStatus]'
aws events list-rules --query 'Rules[*].[Name,State]'
```

### Phase 6: Cleanup (When Done)

```bash
# Destroy infrastructure
cd terraform/environments/dev
terraform destroy -auto-approve

# Delete backend resources (optional)
aws s3 rb s3://my-terraform-state-$(whoami) --force
aws dynamodb delete-table --table-name terraform-state-lock
```

---

## Daily Development Workflow

**For ongoing development and changes:**

```bash
# 1. Create feature branch
git checkout -b feature/my-change

# 2. Make changes
nano terraform/modules/vpc/main.tf

# 3. Run local validation
terraform fmt -recursive
terraform validate

# 4. Run security scans
tflint --chdir=terraform/modules/vpc
tfsec terraform/modules/vpc

# 5. Test locally
cd terraform/environments/dev
terraform plan

# 6. Commit and push
git add .
git commit -m "feat: Add new VPC configuration"
git push origin feature/my-change

# 7. Create PR on GitHub
# Automated workflows run: terraform plan, security scans, policy checks

# 8. Run local AI review
cd ai-assistant
python3 pr-reviewer.py

# 9. Merge PR (if all checks pass)

# 10. Deploy to dev
git checkout main
git pull
cd terraform/environments/dev
terraform apply

# 11. Monitor deployment
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow
```

---

## Cheat Sheet: Most Used Commands

```bash
# AWS
aws configure                                  # Configure AWS credentials
aws sts get-caller-identity                    # Verify AWS connection
aws lambda list-functions                      # List Lambda functions
aws logs tail /aws/lambda/<function-name>      # View Lambda logs
aws ec2 describe-vpcs                          # List VPCs
aws s3 ls                                      # List S3 buckets

# Terraform
terraform init                                 # Initialize Terraform
terraform plan                                 # Preview changes
terraform apply                                # Apply changes
terraform apply -auto-approve                  # Apply without confirmation
terraform destroy                              # Destroy all resources
terraform destroy -auto-approve                # Destroy without confirmation
terraform output                               # Show outputs
terraform state list                           # List resources in state
terraform fmt -recursive                       # Format all .tf files
terraform validate                             # Validate configuration

# Git
git clone <url>                                # Clone repository
git checkout -b <branch>                       # Create branch
git add .                                      # Stage all changes
git commit -m "message"                        # Commit changes
git push origin <branch>                       # Push to remote
git pull                                       # Pull latest changes
git status                                     # Check status
git log --oneline -10                          # View recent commits

# Ollama (AI)
ollama serve                                   # Start Ollama server (Linux/Mac)
ollama pull llama3.1:8b                        # Download AI model
ollama list                                    # List installed models
ollama run llama3.1:8b "test"                  # Test AI model
ollama rm llama3.1:8b                          # Remove model

# Python
python3 -m pip install -r requirements.txt     # Install dependencies
python3 pr-reviewer.py                         # Run AI code reviewer
python3 policy-generator.py --interactive      # Generate OPA policy
pip list                                       # List installed packages

# Security Tools
tflint --init                                  # Initialize TFLint
tflint --chdir=terraform/modules/vpc           # Lint specific directory
tfsec terraform/                               # Security scan
checkov -d terraform/                          # Compliance check
trivy config terraform/                        # Vulnerability scan

# Monitoring
aws logs tail <log-group> --follow             # Real-time logs
aws cloudwatch get-metric-statistics ...       # Get metrics
aws ce get-cost-and-usage ...                  # Get costs
htop                                          # Monitor system resources
```

---

**Congratulations! You now have a fully automated, AI-powered DevSecOps pipeline at ZERO cost!** ðŸš€
---

## ðŸ“‹ Deployment Success Checklist

After completing this guide, verify you have:

**Infrastructure (25 AWS Resources)**:
- [x] 1 VPC (10.0.0.0/16)
- [x] 2 Public subnets (10.0.1.0/24, 10.0.2.0/24)
- [x] 1 Internet Gateway
- [x] 2 Route table associations
- [x] 2 Lambda functions (auto-remediation, security-response)
- [x] 2 KMS keys with rotation enabled
- [x] 2 CloudWatch Log Groups (14-day retention)
- [x] 2 EventBridge rules (security-group-changes, ec2-state-changes)
- [x] 2 Lambda permissions for EventBridge
- [x] 1 IAM role for Lambda
- [x] 1 IAM policy for Lambda
- [x] 1 SNS topic (encrypted with KMS)
- [x] 1 SNS email subscription (confirmed)

**Security & Compliance**:
- [x] CloudTrail enabled for API logging (~$2/month)
- [x] KMS encryption for SNS and CloudWatch Logs
- [x] Key rotation enabled on both KMS keys
- [x] Pre-commit hooks installed (terraform fmt, validate, tflint, tfsec)
- [x] OPA policies validated

**Local AI (Zero Cost)**:
- [x] Ollama 0.15.1+ installed
- [x] LLaMA 3.1:8b model downloaded (4.9 GB)
- [x] AI responding in 2-5 seconds
- [x] Security code analysis working

**Monitoring & Notifications**:
- [x] SNS email subscription confirmed
- [x] CloudWatch Logs collecting Lambda execution logs
- [x] EventBridge rules enabled and monitoring

**Testing Completed**:
- [x] terraform validate passed
- [x] terraform fmt passed
- [x] tflint passed (0 warnings)
- [x] tfsec passed (37 passed, 6 documented ignores)
- [x] pre-commit hooks passing
- [x] OPA tests passing
- [x] Ollama AI code review tested
- [x] Lambda trigger path verified (CloudTrail â†’ EventBridge â†’ Lambda)

**Cost Verification**:
- [x] Monthly AWS cost: ~$4.56/month
  - KMS: $2.00
  - CloudTrail: $2.00
  - CloudWatch: $0.50
  - S3/DynamoDB/SNS: $0.06
- [x] Ollama AI: $0/month (local)
- [x] GitHub Actions: $0/month (free tier)
- [x] **Total: ~$4.56/month** âœ…

**What You've Built**:
1. **Infrastructure as Code**: Terraform managing 25 AWS resources
2. **Automated Security**: Lambda functions auto-remediating security issues
3. **Local AI**: Ollama running LLaMA 3.1 for $0/month code reviews
4. **CI/CD Pipeline**: GitHub Actions automating deployments
5. **Policy as Code**: OPA enforcing security policies
6. **Real-time Monitoring**: CloudTrail â†’ EventBridge â†’ Lambda pipeline
7. **Cost Optimization**: $4.56/month vs $60-180/month traditional approach

**Next Steps**:
1. Enable production mode: Set `auto_fix_enabled = true` in terraform.tfvars
2. Customize security policies in `policies/opa/`
3. Add more EventBridge rules for other AWS services
4. Integrate Discord/Slack notifications (already configured in chatops/)
5. Create additional environments (staging, prod) in terraform/environments/

**ðŸŽ‰ You've saved $55-175/month by using local Ollama instead of cloud AI!**

---
