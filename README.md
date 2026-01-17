# 🤖 Agentic AI DevSecOps on AWS

**PR-Driven Infrastructure with AI-Powered Guardrails**  
*100% FREE for Personal Projects* | GitHub Actions + Terraform + Local AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Terraform](https://img.shields.io/badge/Terraform-1.6+-purple.svg)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange.svg)](https://aws.amazon.com/free/)
[![AI](https://img.shields.io/badge/AI-Ollama%20LLaMA%203.1-blue.svg)](https://ollama.ai/)

---

## 🎯 What Is This?

A **production-ready DevSecOps pipeline** that uses **FREE AI** to automate:

✅ **AI Code Reviews** - Local LLaMA 3.1 reviews every PR  
✅ **Auto-Remediation** - Fixes security issues automatically  
✅ **Policy Generation** - Natural language → OPA/Sentinel policies  
✅ **Security Scanning** - TFLint, tfsec, Checkov, Trivy  
✅ **ChatOps** - Discord/Slack notifications  
✅ **Cost: $0/month** - Stays within AWS/GitHub free tiers

---

## 🚀 Quick Start

### 1-Command Setup

```bash
git clone https://github.com/yourusername/agentic-devsecops-aws.git
cd agentic-devsecops-aws
chmod +x scripts/setup-ai.sh && ./scripts/setup-ai.sh
```

### What Gets Installed (All FREE)

- **Ollama + LLaMA 3.1** - Local AI for code review
- **Terraform** - Infrastructure as Code
- **AWS CLI** - AWS automation
- **TFLint, tfsec, Checkov** - Security scanners
- **OPA** - Policy-as-code engine
- **Pre-commit hooks** - Git workflow automation

---

## 🏗️ Architecture

```
Pull Request → GitHub Actions → AI Review → Security Scans → Auto-Remediation → Deploy
                    ↓                ↓              ↓                ↓
                Local AI        TFLint/tfsec   OPA Policies   AWS Lambda (Free)
               (LLaMA 3.1)                                     
```

### Components

| Component | Technology | Cost |
|-----------|-----------|------|
| **AI Code Review** | Ollama (LLaMA 3.1) | FREE |
| **CI/CD** | GitHub Actions | FREE (2000 min/month) |
| **IaC** | Terraform | FREE |
| **Auto-Remediation** | AWS Lambda | FREE (1M requests/month) |
| **Notifications** | Discord/Slack Webhooks | FREE |
| **Security Scanning** | TFLint, tfsec, Checkov, Trivy | FREE |
| **Policy Engine** | OPA/Conftest | FREE |

**Total Monthly Cost: $0** 🎉

---

## 📁 Project Structure

```
agentic-devsecops-aws
├── terraform                # Terraform configurations
│   ├── modules              # Reusable Terraform modules
│   │   ├── vpc              # VPC module
│   │   ├── ec2              # EC2 module
│   │   └── security         # Security module
│   ├── environments         # Environment-specific configurations
│   │   ├── dev              # Development environment
│   │   ├── staging          # Staging environment
│   │   └── prod             # Production environment
│   ├── backend.tf           # Backend configuration for state management
│   └── versions.tf          # Terraform and provider versions
├── .github                  # GitHub Actions workflows
│   └── workflows
│       ├── terraform-plan.yml
│       ├── terraform-apply.yml
│       ├── security-scan.yml
│       └── pr-validation.yml
├── scripts                  # Scripts for setup and validation
│   ├── setup.sh
│   └── validate.sh
├── policies                 # Policy definitions
│   ├── sentinel
│   │   └── policy.sentinel
│   └── opa
│       └── policy.rego
├── workloads                # Workload configurations
│   └── linux
│       ├── user-data.sh
│       └── config.yaml
├── .gitignore               # Git ignore file
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites
- AWS account
- Terraform installed
- GitHub account for CI/CD

### Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/agentic-devsecops-aws.git
   cd agentic-devsecops-aws
   ```

2. Configure AWS credentials:
   Ensure your AWS credentials are set up in your environment. You can use the AWS CLI to configure them:
   ```
   aws configure
   ```

3. Initialize Terraform:
   Navigate to the desired environment directory (e.g., `terraform/environments/dev`) and run:
   ```
   terraform init
   ```

4. Plan and apply Terraform changes:
   To see what changes will be made:
   ```
   terraform plan
   ```
   To apply the changes:
   ```
   terraform apply
   ```

5. Set up the Linux workload:
   Run the setup script to install necessary packages and apply hardening steps:
   ```
   ./scripts/setup.sh
   ```

## CI/CD Workflows
This project includes GitHub Actions workflows for:
- Terraform plan and apply
- Security scanning
- Pull request validation

## Policies
Policies are defined using Sentinel and OPA to enforce compliance and security guardrails.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- Terraform documentation
- AWS documentation
- Open Policy Agent documentation

For more information, please refer to the respective documentation of the tools used in this project.
# Test change
