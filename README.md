# Agentic AI-Powered DevSecOps on AWS

[![Terraform](https://img.shields.io/badge/Terraform-1.6+-purple?logo=terraform)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-Free_Tier-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Fully automated DevSecOps pipeline with AI-powered code review and Lambda auto-remediation - All running on AWS Free Tier!**

## 🎯 What This Project Does

This project demonstrates a **production-ready DevSecOps pipeline** that automatically:

- 🤖 **Reviews code with AI** (using local Ollama LLaMA 3.1)
- 🔒 **Detects security violations** in real-time via CloudTrail + EventBridge
- ⚡ **Auto-remediates issues** with Lambda functions
- 📊 **Enforces policies** using OPA (Open Policy Agent)
- 💰 **Costs ~$4.56/month** (stays within AWS free tier for most use cases)

## 🚀 Quick Start

**Full deployment in ~30 minutes:**

```bash
# 1. Clone the repository
git clone https://github.com/omade88/agentic-devsecops-aws.git
cd agentic-devsecops-aws

# 2. Follow the comprehensive setup guide
cat docs/AI-SETUP-GUIDE.md
# Or view it on GitHub: docs/AI-SETUP-GUIDE.md
```

## 📚 Documentation

- **[AI-SETUP-GUIDE.md](docs/AI-SETUP-GUIDE.md)** - Complete step-by-step setup guide (3988 lines)
- **[SECURITY.md](docs/SECURITY.md)** - Security policies and best practices
- **[IMPLEMENTATION-SUMMARY.md](docs/IMPLEMENTATION-SUMMARY.md)** - Technical implementation details

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud (Free Tier)                  │
│                                                             │
│  ┌──────────────┐    ┌─────────────┐    ┌──────────────┐  │
│  │  CloudTrail  │───▶│ EventBridge │───▶│   Lambda     │  │
│  │  (API Logs)  │    │   (Events)  │    │ (Auto-Fix)   │  │
│  └──────────────┘    └─────────────┘    └──────────────┘  │
│                                                   │         │
│  ┌──────────────┐    ┌─────────────┐            ▼         │
│  │     VPC      │    │     KMS     │    ┌──────────────┐  │
│  │  (Network)   │    │ (Encryption)│    │     SNS      │  │
│  └──────────────┘    └─────────────┘    │(Notifications)│  │
│                                          └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Email Alert  │
                    └───────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      Local Environment                       │
│                                                             │
│  ┌──────────────┐    ┌─────────────┐    ┌──────────────┐  │
│  │    Ollama    │───▶│  LLaMA 3.1  │───▶│  AI Review   │  │
│  │  (AI Runtime)│    │  (8B Model) │    │  (PR Check)  │  │
│  └──────────────┘    └─────────────┘    └──────────────┘  │
│                                                             │
│  ┌──────────────┐    ┌─────────────┐                       │
│  │  Terraform   │    │     OPA     │                       │
│  │    (IaC)     │    │  (Policies) │                       │
│  └──────────────┘    └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🛡️ Security Automation
- **Real-time detection** of insecure security groups (0.0.0.0/0 SSH/RDP)
- **Automatic remediation** via Lambda or detection-only mode
- **CloudTrail integration** for complete audit trail
- **KMS encryption** for all sensitive data

### 🤖 AI-Powered Code Review
- **Local AI** (Ollama LLaMA 3.1) - no cloud AI costs!
- **Pull request reviews** with security recommendations
- **Policy violations** detected before merge
- **GitHub Actions** integration

### 📊 Policy Enforcement
- **OPA policies** for Terraform validation
- **Pre-commit hooks** for local checks
- **CI/CD pipeline** with automated security scans

### 💰 Cost Optimization
- **~$4.56/month** actual cost (real-world deployment)
- **FREE AI** (local Ollama instead of $60-180/month cloud AI)
- **AWS Free Tier eligible** for most resources
- **Detailed cost breakdown** in documentation

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Infrastructure** | Terraform | Infrastructure as Code |
| **Cloud Platform** | AWS | VPC, Lambda, CloudTrail, EventBridge, SNS, KMS |
| **AI/ML** | Ollama + LLaMA 3.1 | Local AI for code review |
| **Policy Engine** | OPA (Open Policy Agent) | Security policy enforcement |
| **CI/CD** | GitHub Actions | Automated workflows |
| **Languages** | Python, HCL, Bash | Lambda functions, IaC, scripts |

## 📋 Prerequisites

- **AWS Account** (Free tier eligible)
- **GitHub Account**
- **System Requirements:**
  - 8GB+ RAM (16GB recommended for AI)
  - 10GB free disk space
  - Linux/macOS/Windows (WSL2 or Git Bash)

## 🎓 Learning Outcomes

By completing this project, you'll learn:

- ✅ Building production DevSecOps pipelines
- ✅ Terraform infrastructure automation
- ✅ AWS Lambda serverless functions
- ✅ CloudTrail + EventBridge event-driven architecture
- ✅ AI-powered code review with local LLMs
- ✅ OPA policy enforcement
- ✅ Security automation and auto-remediation
- ✅ Cost optimization strategies

## 📊 Real-World Results

**After Deployment:**
- 25 AWS resources created automatically
- Lambda auto-remediation working in <2 minutes
- AI code review on every pull request
- Email alerts for all security events
- Complete audit trail via CloudTrail
- **Total cost: $4.56/month** ✅

## 🤝 Contributing

Contributions are welcome! Please read [SECURITY.md](docs/SECURITY.md) for security guidelines.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** for making local AI accessible
- **HashiCorp** for Terraform
- **AWS** for comprehensive cloud services
- **Open Policy Agent** for policy engine

## 📧 Contact

- **GitHub:** [@omade88](https://github.com/omade88)
- **Repository:** [agentic-devsecops-aws](https://github.com/omade88/agentic-devsecops-aws)

---

**⭐ If this project helped you, please consider giving it a star!**

**🎥 Watch the YouTube tutorial:** [Coming Soon]

---

*Built with ❤️ for the DevOps community*
