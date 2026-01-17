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

Before you begin, ensure you have the following prerequisites ready. This checklist ensures a smooth setup experience.

---

### 🖥️ System Requirements

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

### ☁️ Cloud & Services Prerequisites

#### 1. AWS Account (Required)
- ✅ **Active AWS Account** (Free tier eligible)
- ✅ **IAM User** with programmatic access:
  - Access Key ID
  - Secret Access Key
- ✅ **IAM Policies Attached**:
  - `AmazonEC2FullAccess`
  - `AmazonVPCFullAccess`
  - `AmazonS3FullAccess`
  - `IAMFullAccess`
  - `CloudWatchFullAccess`
  - `AWSLambda_FullAccess`
  - `AmazonEventBridgeFullAccess`
  - `AmazonDynamoDBFullAccess`
- ✅ **S3 Bucket** for Terraform state (unique name)
- ✅ **DynamoDB Table** for state locking (LockID partition key)
- ✅ **Region**: `us-east-1` recommended (or your preferred region)

**Cost**: $0/month (within free tier limits)

#### 2. GitHub Account (Required)
- ✅ **GitHub Account** (Free tier)
- ✅ **Repository Created** (public or private)
- ✅ **GitHub Actions Enabled** (2000 minutes/month free)
- ✅ **Repository Secrets** configured (AWS credentials)

**Cost**: $0/month (2000 Actions minutes free)

#### 3. Slack or Discord (Optional)
- 🔔 **Slack Workspace** (for notifications)
  - Free tier workspace
  - Webhook URL from incoming webhook app
- 🔔 **Discord Server** (alternative to Slack)
  - Free server
  - Webhook URL from channel settings

**Cost**: $0/month (free tier)

---

### 🛠️ Required Software & Tools

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

### 🔧 Tools Installed by Setup Script

These will be **automatically installed** when you run `./scripts/setup-ai.sh`:

#### Core Tools
- ✅ **Terraform** 1.6.0+ (Infrastructure as Code)
- ✅ **AWS CLI** v2 (AWS automation)
- ✅ **Ollama** (AI runtime for LLaMA models)
- ✅ **LLaMA 3.1:8b** model (~4.7GB download)

#### Security Scanners
- ✅ **TFLint** (Terraform linter)
- ✅ **tfsec** (Terraform security scanner)
- ✅ **Checkov** (Infrastructure-as-Code security scanner)
- ✅ **Trivy** (Vulnerability scanner)

#### Policy Engine
- ✅ **OPA** (Open Policy Agent)
- ✅ **Conftest** (Policy testing)

#### Python Packages
- ✅ **boto3** (AWS SDK for Python)
- ✅ **requests** (HTTP library)
- ✅ Other dependencies from `requirements.txt`

**Note**: The setup script handles all installations automatically based on your OS.

---

### 📋 Pre-Installation Checklist

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

### ⚙️ Installation Order

The automated setup follows this sequence:

1. **System Detection** → Identifies your OS (Linux/macOS/Windows)
2. **Package Manager Update** → Updates apt/brew/chocolatey
3. **Core Dependencies** → Installs Python, pip, git, curl
4. **Terraform** → Downloads and installs Terraform 1.6.0
5. **AWS CLI** → Installs AWS CLI v2
6. **Security Tools** → Installs TFLint, tfsec, Checkov, Trivy
7. **Ollama** → Installs Ollama AI runtime
8. **LLaMA Model** → Downloads LLaMA 3.1:8b (~4.7GB)
9. **OPA** → Installs Open Policy Agent
10. **Python Dependencies** → Installs boto3, requests, etc.
11. **Validation** → Verifies all tools installed correctly

**Estimated Time**: 10-15 minutes (depending on internet speed)

---

### 🚨 Common Issues & Solutions

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

---

### 🎯 What Happens Next?

After completing the prerequisites:

1. **Clone the repository** → Your local workspace
2. **Run setup script** → Automated tool installation
3. **Configure AWS** → Connect to your AWS account
4. **Deploy infrastructure** → Terraform creates VPC, Lambda, etc.
5. **Test AI workflows** → Create PR, watch AI review
6. **Monitor & maintain** → Check Lambda logs, costs

**You're now ready to proceed with the Quick Start!** 👇

---

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

##### Step 2: Choose Your Deployment Environment

**IMPORTANT**: You will run all commands on your **LOCAL MACHINE** (laptop/desktop), not on AWS EC2.

**Why Local and Not EC2?**

✅ **Local Machine (Recommended)**:
- Ollama AI models run locally (free, no compute costs)
- Easy development workflow (edit code, test, commit)
- Direct access to your IDE and tools
- GitHub Actions handles AWS deployments remotely
- No EC2 costs ($0/month vs $10-50/month for EC2)

❌ **EC2 Instance (NOT Recommended)**:
- Additional costs (~$10-50/month for compute)
- Requires SSH access and remote development
- More complex setup (VPN, security groups, SSH keys)
- Still need local machine for development anyway

**Architecture Flow**:
```
┌─────────────────────────────────────────────────────┐
│  YOUR LOCAL MACHINE (Development)                   │
│  ├─ Clone repo                                      │
│  ├─ Ollama + LLaMA 3.1 (AI runs here)              │
│  ├─ AWS CLI (configured with credentials)          │
│  ├─ Terraform (deploys to AWS from here)           │
│  ├─ Git (push code to GitHub)                      │
│  └─ Code editor (VS Code, etc.)                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼ (git push)
┌─────────────────────────────────────────────────────┐
│  GITHUB (Code Repository & CI/CD)                   │
│  ├─ GitHub Actions (runs workflows)                │
│  ├─ Security scans                                  │
│  └─ Terraform apply (via Actions)                  │
└──────────────┬──────────────────────────────────────┘
               │
               ▼ (terraform apply)
┌─────────────────────────────────────────────────────┐
│  AWS (Production Infrastructure)                    │
│  ├─ Lambda functions                                │
│  ├─ VPC, EC2, Security Groups                      │
│  ├─ EventBridge, CloudWatch                        │
│  └─ S3, DynamoDB                                    │
└─────────────────────────────────────────────────────┘
```

**Summary**: 
- **Setup & Development**: Your local machine
- **CI/CD & Automation**: GitHub Actions (free)
- **Production Infrastructure**: AWS (deployed via Terraform)

---

##### Step 3: Prepare Your Local Machine

Choose your operating system:

<details>
<summary><b>🐧 Linux (Ubuntu/Debian)</b></summary>

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
<summary><b>🍎 macOS</b></summary>

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
<summary><b>🪟 Windows (Option 1: Git Bash - Recommended for Windows Users)</b></summary>

**Git Bash** provides a Linux-like terminal on Windows without WSL2. This is the easiest option for Windows users.

```bash
# Step 1: Download and Install Git for Windows
# Visit: https://git-scm.com/download/win
# Download the installer (64-bit recommended)
# During installation:
#   ✅ Check "Git Bash Here"
#   ✅ Check "Git from the command line and also from 3rd-party software"
#   ✅ Use default options for everything else

# Step 2: Launch Git Bash
# Right-click anywhere → "Git Bash Here"
# Or: Start Menu → "Git Bash"

# Step 3: Verify Git Bash is working
git --version
# Expected: git version 2.x.x

# Step 4: Install Python (if not already installed)
# Download Python from: https://www.python.org/downloads/
# During installation:
#   ⚠️ IMPORTANT: Check "Add Python to PATH"
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

# ✅ Git Bash is ready!
# You can now run all Linux commands in the rest of this guide
```

**Advantages of Git Bash**:
- ✅ No system restart required (unlike WSL2)
- ✅ Lightweight and fast
- ✅ Native Windows integration
- ✅ Run Linux commands directly (bash, curl, grep, etc.)
- ✅ Perfect for this project

**Note**: All commands in this guide work in Git Bash!

</details>

<details>
<summary><b>🪟 Windows (Option 2: WSL2 - Ubuntu)</b></summary>

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

# Clone the repository to your local machine
git clone https://github.com/omade88/agentic-devsecops-aws.git
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

✅ **Success**: You can now deploy infrastructure to AWS from your local machine!

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

✅ **Backend configured**: Terraform will use S3 for state storage!

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

**6.1: Review Terraform Configuration**

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

**6.2: Update Required Configuration**

⚠️ **IMPORTANT**: You must update these values:

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

**6.3: Initialize Terraform**

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

**6.4: Review Infrastructure Plan**

```bash
# Generate and review the execution plan
terraform plan

# Expected output summary:
# Plan: 21 to add, 0 to change, 0 to destroy.

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

**6.5: Deploy Infrastructure**

```bash
# Apply the configuration (creates AWS resources)
terraform apply

# Review the plan again, then type 'yes' when prompted
# 
# Do you want to perform these actions?
#   Terraform will perform the actions described above.
#   Only 'yes' will be accepted to approve.
# 
#   Enter a value: yes

# ⏳ Deployment in progress... (5-10 minutes)
# 
# Expected output:
# module.vpc.aws_vpc.main: Creating...
# module.vpc.aws_vpc.main: Creation complete after 3s
# module.vpc.aws_internet_gateway.main: Creating...
# module.vpc.aws_subnet.public[0]: Creating...
# module.vpc.aws_subnet.public[1]: Creating...
# ...
# module.lambda_functions.aws_lambda_function.auto_remediation: Creating...
# module.lambda_functions.aws_lambda_function.security_response: Creating...
# module.lambda_functions.aws_sns_topic.notifications: Creating...
# module.lambda_functions.aws_sns_topic_subscription.email: Creating...
# ...
# 
# Apply complete! Resources: 21 added, 0 changed, 0 destroyed.
```

**6.6: Verify Deployment Success**

```bash
# Check VPC creation
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=agentic-devsecops-dev-vpc"

# Check Lambda functions
aws lambda list-functions --query "Functions[?contains(FunctionName, 'agentic')].FunctionName"

# Check SNS topic
aws sns list-topics --query "Topics[?contains(TopicArn, 'agentic-devsecops-dev-notifications')]"

# Expected output: All resources created successfully!
```

**6.7: Important Next Step**

⚠️ **CHECK YOUR EMAIL**: You should receive an SNS subscription confirmation email within 1-2 minutes.

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

---

##### Step 7: Configure GitHub Repository Secrets

1. **Go to your GitHub repository**:
   - URL: `https://github.com/<your-username>/agentic-devsecops-aws`

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

##### Step 7.1: (Optional) Set Up Slack Notifications

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
- Go back to: **Settings** → **Secrets and variables** → **Actions**
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
# Expected output: ✅ Test notification sent successfully!

# You should see a test message in your Slack channel!
```

**What Notifications Will You Receive?**
- ✅ Successful deployments
- ❌ Failed deployments  
- 🔒 Security alerts
- 🤖 AI code review summaries
- 💰 Cost optimization recommendations

**Note**: Slack notifications are completely optional. Your infrastructure works perfectly without them!

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
# Go to: https://github.com/<your-username>/agentic-devsecops-aws/pulls
# Click "New pull request"
# Select: base: main ← compare: test/ai-review
# Click "Create pull request"
```

**What happens next**:
1. ✅ **GitHub Actions workflows trigger automatically**
2. ✅ **Security scans run** (TFLint, tfsec, Checkov, Trivy)
3. ✅ **Terraform validation** checks syntax and configuration
4. ✅ **OPA policies** validate compliance rules
5. ✅ **Results appear** as workflow status on PR
6. ✅ **Notifications sent** to Discord/Slack (if configured)

**Note about AI Code Review:**
- The AI review runs **locally** on your machine, not in GitHub Actions
- To see AI review output, run `python3 ai-assistant/pr-reviewer.py` locally
- This keeps costs at $0 (no cloud AI API calls needed)

**Workflow Files Fixed (Latest Version):**
- ✅ **terraform-plan.yml**: Now uses correct working directory (`terraform/environments/dev`)
- ✅ **terraform-apply.yml**: Manual trigger only (safety feature), proper AWS credentials
- ✅ **Updated actions**: Using latest versions (v4 for checkout, v3 for Terraform)
- ✅ **Terraform version**: 1.6.0 (matches local version)
- ✅ **Added validation step**: Catches errors before planning

---

##### Step 9: Deploy and Monitor AWS Lambda Functions

**9.1: Verify Lambda Deployment**

After running `terraform apply` in Step 6, verify your Lambda functions are deployed:

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

**9.2: Confirm SNS Email Subscription**

⚠️ **IMPORTANT**: You must confirm your email subscription to receive notifications!

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

**9.3: View Lambda Resources Created**

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

**9.4: Monitor Lambda Logs (Real-Time)**

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

**9.5: Test Auto-Remediation (Dry-Run Mode)**

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

# This triggers EventBridge → Lambda within seconds!
```

**Test 2: Check Lambda Execution**

```bash
# Wait 30-60 seconds for Lambda to process the event

# View Lambda logs (should show detection)
aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --since 5m

# Expected log output:
# 🔍 DETECTION MODE: Auto-fix is DISABLED
# 🚨 Security Issue Detected!
# ├─ Type: Overly permissive security group
# ├─ Resource: sg-xxxxx (test-insecure-sg)
# ├─ Issue: SSH (port 22) open to 0.0.0.0/0
# ├─ Risk Level: HIGH
# └─ Recommendation: Restrict to specific IP ranges
# 
# ⚠️  Would fix in production mode (auto_fix_enabled = true)
# 📧 Sending notification to SNS...
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

**9.6: Test Auto-Remediation (Production Mode - Auto-Fix)**

⚠️ **WARNING**: This will automatically modify AWS resources!

```bash
# Navigate to terraform dev environment
cd terraform/environments/dev

# Edit terraform.tfvars
nano terraform.tfvars  # or: vim, code, etc.

# Change this line:
# auto_fix_enabled = false  →  auto_fix_enabled = true

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
# ✅ AUTO-FIX MODE: Enabled
# 🚨 Security Issue Detected!
# ├─ Type: Overly permissive security group
# ├─ Resource: sg-xxxxx (test-insecure-sg)
# ├─ Issue: RDP (port 3389) open to 0.0.0.0/0
# ├─ Risk Level: CRITICAL
# └─ Action: REMOVING insecure rule
# 
# 🔧 Fixing security issue...
# ✅ Successfully removed insecure ingress rule
# ✅ Applied least-privilege access
# 📧 Notification sent
```

**Verify the fix was applied:**

```bash
# Check security group rules (RDP rule should be REMOVED)
aws ec2 describe-security-groups --group-ids $SG_ID --query "SecurityGroups[0].IpPermissions"

# RDP 0.0.0.0/0 rule should be gone!
```

**9.7: Clean Up Test Resources**

```bash
# Delete test security group
aws ec2 delete-security-group --group-id $SG_ID

# Verify deletion
aws ec2 describe-security-groups --group-ids $SG_ID
# Expected: An error: "does not exist" (this is correct!)
```

**9.8: Monitor Lambda Performance**

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

**9.9: View Lambda in AWS Console**

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

**9.10: Cost Tracking (Lambda)**

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

##### Step 10: Verify AI Assistant is Running

**10.1: Install Ollama and Pull LLaMA Model**

<details>
<summary><b>🪟 Windows (PowerShell)</b></summary>

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
<summary><b>🐧 Linux / 🍎 macOS</b></summary>

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
🤖 AI-Powered PR Reviewer (Ollama)
==================================================
✅ Connected to Ollama at http://localhost:11434
📦 Using model: llama3.1:8b

📝 Analyzing 1 file(s)...

🔍 Analyzing: /path/to/terraform/environments/dev/variables.tf
  ✅ Complete

==================================================
✅ Review complete! Output saved to: ai_review_output.md

Preview:
## 🤖 AI-Powered Code Review (Ollama)

**Model:** `llama3.1:8b`

✅ **No issues found!** Code looks good.

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

#### Setup Complete! 🎉

Your Agentic AI DevSecOps environment is now fully operational:

✅ **AWS Infrastructure Deployed**:
- VPC with public/private subnets (10.0.0.0/16)
- Internet Gateway and route tables
- Security groups with least-privilege access
- Lambda functions for auto-remediation
- EventBridge rules monitoring AWS events
- CloudWatch log groups (14-day retention)
- SNS notifications to your email

✅ **Lambda Auto-Remediation**:
- 2 Lambda functions (auto-remediation, security-response)
- Python 3.11 runtime, 256MB memory, 300s timeout
- EventBridge triggers (security group + EC2 changes)
- IAM roles with appropriate permissions
- Dry-run mode enabled (safe for testing)

✅ **Local AI Ready**:
- Ollama v0.14.1 installed
- LLaMA 3.1:8b model (~4.7GB) downloaded
- AI code reviewer working
- Policy generator available

✅ **Security Tools Installed**:
- TFLint (Terraform linting)
- tfsec (security scanning)
- Checkov (compliance checking)
- Trivy (vulnerability scanning)
- OPA (policy validation)

✅ **GitHub Integration**:
- Repository: <your-username>/agentic-devsecops-aws
- GitHub Actions workflows running
- S3 backend for Terraform state
- DynamoDB state locking
- Automated security scans on PRs

✅ **ChatOps (Optional)**:
- Slack webhook configured (if you completed Step 7.1)
- SNS email notifications active

**Cost Tracking**: $0/month (all within free tiers)
- Lambda: 1M requests/month free (using ~10-100/month)
- EventBridge: 14M events free (using ~1K/month)
- CloudWatch: 10 metrics free (using 5)
- S3: 5GB free (using <1GB)
- Total: **$0/month** 🎉

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
├── Public Subnets
│   ├── 10.0.1.0/24 (us-east-1a)
│   └── 10.0.2.0/24 (us-east-1b)
├── Private Subnets
│   ├── 10.0.3.0/24 (us-east-1a)
│   └── 10.0.4.0/24 (us-east-1b)
├── Internet Gateway
└── Route Tables

Lambda Auto-Remediation
├── Function: auto-remediation (Python 3.11, 256MB)
│   ├── Trigger: EventBridge (security group changes)
│   ├── Trigger: EventBridge (EC2 state changes)
│   ├── Logs: CloudWatch (/aws/lambda/...-auto-remediation)
│   └── Permissions: EC2, S3, CloudWatch access
├── Function: security-response (Python 3.11, 256MB)
│   ├── Logs: CloudWatch (/aws/lambda/...-security-response)
│   └── Permissions: EC2, IAM, CloudWatch access
├── SNS Topic: agentic-devsecops-dev-notifications
│   └── Email: your-email@example.com (confirmed ✅)
└── Mode: Dry-run (auto_fix_enabled = false)
```

---

#### Next Steps

**Immediate Actions (Required):**

1. **✅ Confirm SNS Email Subscription**
   - Check inbox for "AWS Notification - Subscription Confirmation"
   - Click confirmation link
   - Verify in AWS Console: SNS → Subscriptions → Status should show "Confirmed"

2. **🧪 Test Lambda Auto-Remediation (Dry-Run)**
   ```bash
   # Create insecure security group to trigger Lambda
   cd terraform/environments/dev
   
   # See Step 9.5 for complete testing instructions
   # Lambda will DETECT but not fix (safe mode)
   ```

3. **📊 Monitor Lambda Logs**
   ```bash
   # Watch Lambda execution in real-time
   aws logs tail /aws/lambda/agentic-devsecops-dev-auto-remediation --follow
   
   # Press Ctrl+C to stop
   ```

**Learning & Exploration:**

4. **🤖 Test AI Code Review**
   ```bash
   # Create a test PR with Terraform changes
   git checkout -b test/lambda-monitoring
   echo "# Monitor Lambda performance" >> README.md
   git add . && git commit -m "docs: Add Lambda monitoring notes"
   git push origin test/lambda-monitoring
   
   # Open PR on GitHub, watch AI analysis
   ```

5. **🔒 Create Infrastructure Changes** 
   - Modify Terraform files in `terraform/modules/`
   - Open PR → Watch automated security scans
   - See TFLint, tfsec, Checkov, Trivy results
   - Review AI-generated recommendations

6. **📜 Customize OPA Policies**
   - Edit policies in `policies/templates/`
   - Examples:
     - `ec2-compliance.rego` - EC2 compliance rules
     - `s3-security.rego` - S3 bucket security
     - `security-group.rego` - Security group validation
   - Test with: `opa test policies/`

7. **💬 Set Up ChatOps** (Optional but Recommended)
   - Complete Step 7.1 for Slack integration
   - Receive notifications for:
     - Lambda auto-remediations
     - Security violations detected
     - Deployment status
     - Cost optimization recommendations

8. **🚀 Enable Auto-Fix Mode** (When Ready)
   ```bash
   # After testing dry-run mode
   cd terraform/environments/dev
   nano terraform.tfvars
   # Change: auto_fix_enabled = false → true
   terraform apply
   
   # Lambda will now AUTOMATICALLY FIX security issues!
   ```

**Advanced Usage:**

9. **📈 Monitor Costs in AWS**
   - Go to: https://console.aws.amazon.com/billing/home#/freetier
   - Filter: Lambda, EventBridge, CloudWatch
   - Expected: All within free tier ($0/month)

10. **🔄 Deploy to Staging** (Optional)
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

11. **🏭 Production Deployment** (Portfolio Ready)
    ```bash
    # Deploy to production when ready to showcase
    cd terraform/environments/prod
    
    # Update terraform.tfvars
    # Use production-grade settings
    # Enable auto-fix for production
    
    terraform init && terraform plan && terraform apply
    ```

12. **📚 Document Your Learning**
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
`Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: us-east-1 (or your preferred region)

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
# Right-click in project folder → "Git Bash Here"

# 6. Use PowerShell for Ollama/AI work
# In project folder: Shift+Right-click → "Open PowerShell window here"
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
