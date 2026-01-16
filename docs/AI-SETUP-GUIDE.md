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

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-devsecops-aws.git
cd agentic-devsecops-aws

# Run the setup script
chmod +x scripts/setup-ai.sh
./scripts/setup-ai.sh

# The script will:
# ✅ Install all dependencies
# ✅ Set up Ollama with LLaMA 3.1
# ✅ Configure AWS CLI
# ✅ Install security tools
# ✅ Set up pre-commit hooks
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
