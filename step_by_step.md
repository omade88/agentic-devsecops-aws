# Standard Operating Procedure (SOP)
## Agentic DevSecOps on AWS: PR-Driven Infrastructure with Guardrails

---

## Table of Contents
1. [Initial Setup](#1-initial-setup)
2. [Development Workflow](#2-development-workflow)
3. [Pull Request Process](#3-pull-request-process)
4. [Security & Compliance](#4-security--compliance)
5. [Deployment Process](#5-deployment-process)
6. [Troubleshooting](#6-troubleshooting)
7. [Maintenance & Operations](#7-maintenance--operations)

---

## 1. Initial Setup

### 1.1 Prerequisites Installation

**Step 1.1.1: Install Required Tools**

**Windows (PowerShell - Recommended):**
```powershell
# Install Chocolatey if not already installed
# Run PowerShell as Administrator first
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Terraform
choco install terraform -y

# Verify installation
terraform --version

# Install AWS CLI
choco install awscli -y

# Verify AWS CLI
aws --version

# Install TFLint
choco install tflint -y
# Or manual: Download from https://github.com/terraform-linters/tflint/releases

# Install tfsec
choco install tfsec -y
# Or manual: Download from https://github.com/aquasecurity/tfsec/releases

# Install Python and pip (if not installed)
choco install python -y

# Install pre-commit
python -m pip install pre-commit
```

**Windows (Git Bash - Alternative):**
```bash
# Install Terraform (Manual Download)
# 1. Download Windows 64-bit version from: https://releases.hashicorp.com/terraform/1.6.0/
cd ~/Downloads
unzip terraform_1.6.0_windows_amd64.zip
mkdir -p ~/bin
mv terraform.exe ~/bin/
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc

# Verify installation
terraform --version

# Install AWS CLI (if not installed via installer)
# Download MSI from: https://awscli.amazonaws.com/AWSCLIV2.msi
# Or use existing AWS CLI from PATH
aws --version

# Install TFLint (Manual Download)
curl -L -o tflint.zip https://github.com/terraform-linters/tflint/releases/download/v0.50.0/tflint_windows_amd64.zip
unzip tflint.zip -d ~/bin/
rm tflint.zip

# Install tfsec (Manual Download)
curl -L -o tfsec.exe https://github.com/aquasecurity/tfsec/releases/download/v1.28.0/tfsec-windows-amd64.exe
mv tfsec.exe ~/bin/

# Install pre-commit
python -m pip install pre-commit

# Verify installations
terraform --version
aws --version
tflint --version
tfsec --version
pre-commit --version
```

**Linux/macOS:**
```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify AWS CLI
aws --version

# Install TFLint
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Install tfsec
curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash

# Install OPA
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod 755 ./opa
sudo mv opa /usr/local/bin/

# Install pre-commit
pip3 install pre-commit
```

**Step 1.1.2: Verify Installations**

**Windows (PowerShell):**
```powershell
terraform --version
aws --version
tflint --version
tfsec --version
python --version
pre-commit --version
```

**Windows (Git Bash):**
```bash
terraform --version
aws --version
tflint --version
tfsec --version
python --version
pre-commit --version
```

**Linux/macOS:**
```bash
terraform --version
aws --version
tflint --version
tfsec --version
opa version
pre-commit --version
```

### 1.2 AWS Account Configuration

**Step 1.2.1: Configure AWS Credentials**
```bash
aws configure
# AWS Access Key ID: [Enter your access key]
# AWS Secret Access Key: [Enter your secret key]
# Default region name: us-west-2
# Default output format: json
```

**Step 1.2.2: Verify AWS Access**
```bash
aws sts get-caller-identity
```

**Step 1.2.3: Create S3 Bucket for Terraform State**

**PowerShell:**
```powershell
# Create S3 bucket for state storage
aws s3api create-bucket `
    --bucket your-terraform-state-bucket-unique-name `
    --region us-west-2 `
    --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning
aws s3api put-bucket-versioning `
    --bucket your-terraform-state-bucket-unique-name `
    --versioning-configuration Status=Enabled

# Enable encryption
$encryptionConfig = @'
{
    "Rules": [{
        "ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": "AES256"
        }
    }]
}
'@

aws s3api put-bucket-encryption `
    --bucket your-terraform-state-bucket-unique-name `
    --server-side-encryption-configuration $encryptionConfig
```

**Git Bash / Linux / macOS:**
```bash
# Create S3 bucket for state storage
aws s3api create-bucket \
    --bucket your-terraform-state-bucket-unique-name \
    --region us-west-2 \
    --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket your-terraform-state-bucket-unique-name \
    --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
    --bucket your-terraform-state-bucket-unique-name \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

**Step 1.2.4: Create DynamoDB Table for State Locking**

**PowerShell:**
```powershell
aws dynamodb create-table `
    --table-name terraform-lock-table `
    --attribute-definitions AttributeName=LockID,AttributeType=S `
    --key-schema AttributeName=LockID,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --region us-west-2
```

**Git Bash / Linux / macOS:**
```bash
aws dynamodb create-table \
    --table-name terraform-lock-table \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-west-2
```

**Step 1.2.5: Update Backend Configuration**

Update `terraform/backend.tf`:
```tf
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket-unique-name"
    key            = "terraform/state"
    region         = "us-west-2"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}
```

### 1.3 GitHub Repository Setup

**Step 1.3.1: Clone Repository**

**All Platforms (PowerShell / Git Bash / Linux / macOS):**
```bash
git clone https://github.com/yourusername/agentic-devsecops-aws.git
cd agentic-devsecops-aws
```

**Step 1.3.2: Configure GitHub Secrets**

Navigate to: `GitHub Repository → Settings → Secrets and variables → Actions`

Add the following secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: us-west-2

**Step 1.3.3: Enable Branch Protection**

Navigate to: `GitHub Repository → Settings → Branches → Add rule`

Configure for `main` branch:
- ✅ Require pull request reviews before merging (1 approval)
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- Select required status checks:
  - `validate`
  - `terraform`
  - `security-scan`
- ✅ Include administrators

**Step 1.3.4: Initialize Pre-commit Hooks**

**All Platforms (PowerShell / Git Bash / Linux / macOS):**
```bash
cd agentic-devsecops-aws
pre-commit install
pre-commit run --all-files
```

**Note for Windows users:** Pre-commit works in both PowerShell and Git Bash. If you encounter issues in PowerShell, try using Git Bash.

---

## 2. Development Workflow

### 2.1 Environment Selection

**Step 2.1.1: Choose Target Environment**

Available environments:
- **dev**: Development environment for testing
- **staging**: Pre-production environment
- **prod**: Production environment

**Step 2.1.2: Navigate to Environment Directory**
```bash
cd terraform/environments/dev  # or staging/prod
```

### 2.2 Local Development & Testing

**Step 2.2.1: Initialize Terraform**
```bash
terraform init
```

**Expected output:**
```
Initializing the backend...
Successfully configured the backend "s3"
Terraform has been successfully initialized!
```

**Step 2.2.2: Validate Configuration**
```bash
# Format check
terraform fmt -check -recursive

# Validate syntax
terraform validate

# Run custom validation script
bash ../../../scripts/validate.sh
```

**Step 2.2.3: Run Security Scans Locally**
```bash
# TFLint
tflint --init
tflint

# tfsec
tfsec .

# OPA policy check (if applicable)
opa test ../../../policies/opa/
```

**Step 2.2.4: Generate Terraform Plan**
```bash
terraform plan -var-file=terraform.tfvars -out=tfplan
```

**Step 2.2.5: Review Plan Output**

Check for:
- ✅ Resources to be created/modified/destroyed
- ✅ No unexpected changes
- ✅ Security group rules are restrictive
- ✅ Required tags are present
- ✅ IMDSv2 is enforced
- ✅ EBS volumes are encrypted

**Step 2.2.6: View Plan Details**
```bash
terraform show tfplan
```

---

## 3. Pull Request Process

### 3.1 Creating a Feature Branch

**Step 3.1.1: Create New Branch**
```bash
git checkout -b feature/add-monitoring-ec2

# Naming conventions:
# feature/description    - New features
# fix/description        - Bug fixes
# security/description   - Security improvements
# docs/description       - Documentation updates
```

**Step 3.1.2: Make Infrastructure Changes**

Example: Update `terraform/environments/dev/main.tf`

```tf
// filepath: terraform/environments/dev/main.tf
// ...existing code...

# Add CloudWatch monitoring
resource "aws_cloudwatch_metric_alarm" "ec2_cpu" {
  alarm_name          = "${var.environment}-ec2-cpu-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  
  dimensions = {
    InstanceId = module.ec2.instance_id
  }
}

// ...existing code...
```

**Step 3.1.3: Update Variables if Needed**

Update `terraform/environments/dev/variables.tf` if new variables are required.

**Step 3.1.4: Update terraform.tfvars**

Update `terraform/environments/dev/terraform.tfvars` with new values.

### 3.2 Pre-commit Validation

**Step 3.2.1: Run Pre-commit Hooks**
```bash
pre-commit run --all-files
```

**Step 3.2.2: Fix Any Issues**
```bash
# Auto-format Terraform files
terraform fmt -recursive

# Fix trailing whitespace
# (pre-commit will show specific files)
```

### 3.3 Committing Changes

**Step 3.3.1: Stage Changes**
```bash
git add .
```

**Step 3.3.2: Commit with Descriptive Message**
```bash
git commit -m "feat: Add CloudWatch CPU monitoring for EC2 instances

- Added CloudWatch metric alarm for CPU utilization
- Set threshold to 80% over 2 evaluation periods
- Applied to dev environment EC2 instances"
```

**Commit message format:**
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `security`: Security improvement
- `refactor`: Code refactoring
- `docs`: Documentation
- `test`: Testing
- `chore`: Maintenance

**Step 3.3.3: Push to Remote**
```bash
git push origin feature/add-monitoring-ec2
```

### 3.4 Opening a Pull Request

**Step 3.4.1: Navigate to GitHub Repository**

Go to: `https://github.com/yourusername/agentic-devsecops-aws/pulls`

**Step 3.4.2: Click "New Pull Request"**

**Step 3.4.3: Fill PR Template**

```markdown
## Description
Add CloudWatch CPU monitoring for EC2 instances in dev environment.

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Added CloudWatch metric alarm for CPU utilization
- Configured 80% threshold with 2 evaluation periods
- Applied naming convention: `${environment}-ec2-cpu-alarm`

## Testing Performed
- [x] Terraform validate passed
- [x] Terraform plan reviewed
- [x] TFLint passed
- [x] tfsec security scan passed
- [x] OPA policy validation passed

## Terraform Plan Output
```
Plan: 1 to add, 0 to change, 0 to destroy.
```

## Security Considerations
- No new security groups or open ports
- Uses existing EC2 instance from module
- CloudWatch alarms don't expose sensitive data

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Documentation updated
- [x] No hardcoded secrets
- [x] Required tags added
- [x] Encryption enabled where applicable
```

**Step 3.4.4: Submit Pull Request**

Click "Create pull request"

### 3.5 Automated CI/CD Checks

**Step 3.5.1: Monitor GitHub Actions**

The following workflows will automatically run:

**1. PR Validation** (`.github/workflows/pr-validation.yml`)
- Terraform initialization
- Terraform validation
- Format checking
- Validation script execution
- TFLint
- tfsec security scan

**2. Terraform Plan** (`.github/workflows/terraform-plan.yml`)
- Generate terraform plan
- Upload plan artifact

**3. Security Scan** (`.github/workflows/security-scan.yml`)
- TFLint execution
- tfsec security scanning

**Step 3.5.2: Review Check Results**

Navigate to: `Pull Request → Checks`

Ensure all checks pass:
- ✅ validate
- ✅ terraform
- ✅ security-scan

**Step 3.5.3: If Checks Fail**

View logs:
```
1. Click on failed check
2. Expand failed step
3. Review error messages
4. Fix issues locally
5. Commit and push fixes
6. Checks will re-run automatically
```

Common failures and fixes:

**Terraform Format Issues:**
```bash
terraform fmt -recursive
git add .
git commit -m "fix: Format terraform files"
git push
```

**TFLint Errors:**
```bash
# View specific issues
tflint

# Fix issues based on output
# Example: Remove deprecated syntax, fix module versions
git commit -m "fix: Resolve TFLint issues"
git push
```

**tfsec Security Issues:**
```bash
# View security issues
tfsec . --format=json

# Example fixes:
# - Add encryption
# - Restrict security group rules
# - Enable versioning
# - Add required tags
```

### 3.6 Code Review Process

**Step 3.6.1: Request Review**

Assign reviewers who will check:
- ✅ Infrastructure changes are necessary
- ✅ Security best practices followed
- ✅ No hardcoded credentials
- ✅ Proper tagging strategy
- ✅ Cost implications considered
- ✅ Terraform plan reviewed
- ✅ No unnecessary resource destruction

**Step 3.6.2: Address Review Comments**

```bash
# Make requested changes
git add .
git commit -m "refactor: Address PR review comments"
git push
```

**Step 3.6.3: Obtain Approval**

Minimum 1 approval required (based on branch protection rules)

---

## 4. Security & Compliance

### 4.1 Security Guardrails

**Step 4.1.1: Verify Security Group Rules**

Check that security groups in `terraform/modules/security/main.tf` follow these rules:

❌ **NOT ALLOWED:**
```tf
cidr_blocks = ["0.0.0.0/0"]  # For SSH port 22
```

✅ **ALLOWED:**
```tf
cidr_blocks = ["10.0.0.0/16"]  # Restricted CIDR
cidr_blocks = ["YOUR_OFFICE_IP/32"]  # Specific IP
```

**Step 4.1.2: Verify Required Tags**

All resources must have:
```tf
tags = {
  Environment = "dev"
  Owner       = "team-name"
  CostCenter  = "engineering"
  Project     = "agentic-devsecops"
}
```

**Step 4.1.3: Verify EBS Encryption**

Update `terraform/modules/ec2/main.tf`:

```tf
// filepath: terraform/modules/ec2/main.tf
resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = var.subnet_id
  vpc_security_group_ids = var.security_group_ids

  root_block_device {
    encrypted = true
    volume_type = "gp3"
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"  # IMDSv2
  }

  tags = {
    Name        = "ExampleInstance"
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
  }

  user_data = file("${path.module}/../../workloads/linux/user-data.sh")
}

// ...existing code...
```

**Step 4.1.4: Update OPA Policy**

Edit `policies/opa/policy.rego`:

```rego
// filepath: policies/opa/policy.rego
package terraform.security

import future.keywords.in

# Deny if security group allows 0.0.0.0/0 on port 22
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.from_port == 22
    "0.0.0.0/0" in rule.cidr_blocks
    msg := sprintf("Security group %s allows SSH from 0.0.0.0/0", [resource.address])
}

# Deny if EC2 instance doesn't have required tags
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    required_tags := {"Environment", "Owner", "CostCenter"}
    provided_tags := {tag | resource.change.after.tags[tag]}
    missing := required_tags - provided_tags
    count(missing) > 0
    msg := sprintf("EC2 instance %s missing required tags: %v", [resource.address, missing])
}

# Deny if EBS volumes are not encrypted
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not resource.change.after.root_block_device[0].encrypted
    msg := sprintf("EC2 instance %s has unencrypted root volume", [resource.address])
}

# Deny if IMDSv2 is not enforced
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    resource.change.after.metadata_options[0].http_tokens != "required"
    msg := sprintf("EC2 instance %s does not enforce IMDSv2", [resource.address])
}
```

**Step 4.1.5: Test OPA Policies**

```bash
# Generate plan in JSON format
cd terraform/environments/dev
terraform plan -out=tfplan
terraform show -json tfplan > plan.json

# Test against OPA policy
opa eval --data ../../../policies/opa/policy.rego \
         --input plan.json \
         --format pretty \
         "data.terraform.security.deny"
```

### 4.2 Compliance Checks

**Step 4.2.1: Run Compliance Validation**

```bash
# Navigate to scripts directory
cd scripts

# Run comprehensive validation
./validate.sh
```

**Step 4.2.2: Review Validation Output**

Expected output:
```
✅ Terraform format check passed
✅ Terraform validation passed
✅ TFLint checks passed
✅ tfsec security scan passed
Validation succeeded.
```

**Step 4.2.3: Document Compliance**

Create compliance report:
```bash
# Generate compliance report
cat > compliance-report-$(date +%Y%m%d).md << EOF
# Compliance Report - $(date +%Y-%m-%d)

## Environment: dev

### Security Checks
- [x] No open 0.0.0.0/0 on port 22
- [x] All EBS volumes encrypted
- [x] IMDSv2 enforced on all EC2 instances
- [x] Required tags present on all resources
- [x] Security groups follow least privilege

### Tools Used
- Terraform v1.6.0
- TFLint v0.50.0
- tfsec v1.28.0
- OPA v0.60.0

### Scan Results
\`\`\`
$(tfsec . --format=default)
\`\`\`

### Policy Validation
\`\`\`
$(opa eval --data policies/opa/policy.rego --input terraform/environments/dev/plan.json "data.terraform.security.deny")
\`\`\`
EOF
```

---

## 5. Deployment Process

### 5.1 Manual Approval

**Step 5.1.1: Review PR Approval**

Ensure:
- ✅ All CI checks passed
- ✅ Code review approved
- ✅ Terraform plan reviewed
- ✅ Security scans clean
- ✅ No merge conflicts

**Step 5.1.2: Merge Pull Request**

Click "Merge pull request" → "Confirm merge"

### 5.2 Automated Terraform Apply

**Step 5.2.1: Monitor Terraform Apply Workflow**

The `terraform-apply.yml` workflow will trigger automatically after merge.

**Step 5.2.2: Review Apply Logs**

Navigate to: `Actions → Terraform Apply`

Monitor the apply process:
```
Terraform Init... ✅
Terraform Apply... ⏳
```

**Step 5.2.3: Verify Resources Created**

```bash
# Check AWS resources
aws ec2 describe-instances \
    --filters "Name=tag:Environment,Values=dev" \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' \
    --output table

# Check VPC
aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=dev-vpc" \
    --output table

# Check security groups
aws ec2 describe-security-groups \
    --filters "Name=tag:Environment,Values=dev" \
    --output table
```

**Step 5.2.4: Document Deployment**

```bash
# Create deployment log
cat > deployments/deployment-$(date +%Y%m%d-%H%M%S).md << EOF
# Deployment Log

**Date:** $(date +%Y-%m-%d %H:%M:%S)
**Environment:** dev
**Deployed By:** GitHub Actions
**PR:** #123
**Commit:** $(git rev-parse HEAD)

## Resources Deployed
- VPC: vpc-xxxxx
- EC2 Instance: i-xxxxx
- Security Groups: sg-xxxxx, sg-yyyyy

## Validation
- [x] Resources created successfully
- [x] NGINX accessible
- [x] Security groups configured correctly
- [x] CloudWatch monitoring active

## Rollback Plan
If issues occur:
1. Revert PR merge
2. Run terraform destroy for affected resources
3. Re-apply previous stable state
EOF
```

### 5.3 Post-Deployment Validation

**Step 5.3.1: Verify EC2 Instance**

```bash
# Get instance public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --filters "Name=tag:Environment,Values=dev" "Name=instance-state-name,Values=running" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "Instance IP: $PUBLIC_IP"
```

**Step 5.3.2: Test NGINX Access**

```bash
# Test HTTP connectivity
curl -I http://$PUBLIC_IP

# Expected output:
# HTTP/1.1 200 OK
# Server: nginx
```

**Step 5.3.3: Verify Security Hardening**

```bash
# Connect via SSM (if configured)
aws ssm start-session --target i-xxxxx

# Or use SSH with key
ssh -i your-key.pem ubuntu@$PUBLIC_IP

# Check UFW status
sudo ufw status

# Expected output:
# Status: active
# To                         Action      From
# --                         ------      ----
# Nginx Full                 ALLOW       Anywhere

# Check NGINX status
sudo systemctl status nginx

# Verify IMDSv2
curl -H "X-aws-ec2-metadata-token: invalid" http://169.254.169.254/latest/meta-data/instance-id
# Should return 401 Unauthorized
```

**Step 5.3.4: Verify CloudWatch Monitoring**

```bash
# Check CloudWatch alarms
aws cloudwatch describe-alarms \
    --alarm-name-prefix "dev-" \
    --query 'MetricAlarms[*].[AlarmName,StateValue]' \
    --output table
```

---

## 6. Troubleshooting

### 6.1 Common Terraform Errors

**Error: State Lock Acquisition Failed**

```
Error: Error acquiring the state lock
Error message: ConditionalCheckFailedException
```

**Solution:**
```bash
# List locks
aws dynamodb scan --table-name terraform-lock-table

# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>
```

**Error: Invalid Provider Configuration**

```
Error: Insufficient aws_vpc blocks
```

**Solution:**
```bash
# Check provider configuration
terraform providers

# Re-initialize
rm -rf .terraform
terraform init
```

**Error: Resource Already Exists**

```
Error: A resource with the ID "vpc-xxxxx" already exists
```

**Solution:**
```bash
# Import existing resource
terraform import aws_vpc.main vpc-xxxxx

# Or remove from state if not needed
terraform state rm aws_vpc.main
```

### 6.2 GitHub Actions Failures

**Workflow: terraform-plan.yml fails**

**Check 1: Secrets Configuration**
```
Navigate to: Settings → Secrets → Actions
Verify: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
```

**Check 2: Terraform Syntax**
```bash
terraform validate
terraform fmt -check
```

**Check 3: Backend Access**
```bash
aws s3 ls s3://your-terraform-state-bucket-unique-name/
```

**Workflow: security-scan.yml fails**

**Check tfsec issues:**
```bash
tfsec . --format=json > tfsec-results.json
cat tfsec-results.json | jq '.results[]'
```

**Fix security issues:**
- Add encryption: `encrypted = true`
- Restrict CIDR: Change `0.0.0.0/0` to specific IP
- Add tags: Include Environment, Owner, CostCenter

### 6.3 EC2 Instance Issues

**Issue: Cannot connect to EC2**

**Step 1: Check security group**
```bash
aws ec2 describe-security-groups \
    --group-ids sg-xxxxx \
    --query 'SecurityGroups[*].IpPermissions[]'
```

**Step 2: Verify instance state**
```bash
aws ec2 describe-instances \
    --instance-ids i-xxxxx \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name]'
```

**Step 3: Check system logs**
```bash
aws ec2 get-console-output --instance-id i-xxxxx
```

**Issue: NGINX not responding**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@$PUBLIC_IP

# Check NGINX status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/nginx/error.log

# Restart if needed
sudo systemctl restart nginx
```

**Issue: User data script failed**

```bash
# View cloud-init logs
sudo cat /var/log/cloud-init-output.log

# Re-run user data manually
sudo bash /var/lib/cloud/instance/user-data.txt
```

### 6.4 State Management Issues

**Issue: State file corruption**

```bash
# Download state backup
aws s3 cp s3://your-terraform-state-bucket-unique-name/terraform/state \
          terraform.tfstate.backup

# Restore from backup
aws s3api list-object-versions \
    --bucket your-terraform-state-bucket-unique-name \
    --prefix terraform/state

# Restore specific version
aws s3api get-object \
    --bucket your-terraform-state-bucket-unique-name \
    --key terraform/state \
    --version-id <VERSION_ID> \
    terraform.tfstate
```

**Issue: State drift detected**

```bash
# Refresh state
terraform refresh

# Show differences
terraform plan

# Import resources if needed
terraform import <resource_type>.<name> <resource_id>
```

---

## 7. Maintenance & Operations

### 7.1 Regular Maintenance Tasks

**Weekly Tasks**

**Step 7.1.1: Review Security Scan Results**
```bash
# Run comprehensive security scan
cd terraform/environments/dev
tfsec . --format=json > weekly-scan-$(date +%Y%m%d).json

# Review critical findings
cat weekly-scan-$(date +%Y%m%d).json | jq '.results[] | select(.severity=="CRITICAL")'
```

**Step 7.1.2: Update Dependencies**
```bash
# Check Terraform version
terraform version

# Update providers
terraform init -upgrade

# Test with updated providers
terraform plan
```

**Step 7.1.3: Review CloudWatch Alarms**
```bash
# Check alarm states
aws cloudwatch describe-alarms \
    --state-value ALARM \
    --query 'MetricAlarms[*].[AlarmName,StateValue,StateReason]' \
    --output table
```

**Monthly Tasks**

**Step 7.1.4: Cost Review**
```bash
# Generate cost report
aws ce get-cost-and-usage \
    --time-period Start=$(date -d '1 month ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics "UnblendedCost" \
    --group-by Type=TAG,Key=Environment

# Review untagged resources
aws resourcegroupstaggingapi get-resources \
    --resource-type-filters ec2 \
    --tag-filters Key=Environment
```

**Step 7.1.5: Backup State Files**
```bash
# Create local backup
aws s3 sync s3://your-terraform-state-bucket-unique-name/ \
             ./state-backups/$(date +%Y%m%d)/
```

**Step 7.1.6: Review Access Logs**
```bash
# Check S3 bucket access logs
aws s3 ls s3://your-terraform-state-bucket-unique-name-logs/

# Review EC2 instance access
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=ResourceType,AttributeValue=AWS::EC2::Instance \
    --max-results 50
```

### 7.2 Disaster Recovery

**Step 7.2.1: Create DR Plan Document**

```markdown
# Disaster Recovery Plan

## Scenario 1: Complete Infrastructure Loss

### Recovery Steps:
1. Verify S3 state bucket accessible
2. Clone repository
3. Run terraform init
4. Run terraform apply
5. Verify resources created
6. Restore application data

### RTO: 2 hours
### RPO: 5 minutes (state file updates)

## Scenario 2: State File Corruption

### Recovery Steps:
1. Download state backup from S3 versioning
2. Restore to local terraform.tfstate
3. Upload to S3
4. Run terraform refresh
5. Validate with terraform plan

### RTO: 30 minutes
### RPO: Last state file version

## Scenario 3: Unauthorized Changes

### Recovery Steps:
1. Identify unauthorized changes in CloudTrail
2. Revert to last known good state
3. Run terraform apply to restore
4. Update security policies
5. Rotate credentials

### RTO: 1 hour
### RPO: Last terraform apply
```

**Step 7.2.2: Test DR Procedures Quarterly**

```bash
# Create test environment
cd terraform/environments/dr-test
terraform init
terraform apply

# Verify recovery
./scripts/validate.sh

# Clean up
terraform destroy
```

### 7.3 Scaling Operations

**Step 7.3.1: Add New Environment**

```bash
# Create new environment directory
mkdir -p terraform/environments/qa
cd terraform/environments/qa

# Copy from template
cp ../dev/main.tf .
cp ../dev/variables.tf .
cp ../dev/terraform.tfvars .

# Update environment-specific values
sed -i 's/dev/qa/g' terraform.tfvars
```

**Step 7.3.2: Add New Region**

Update `terraform/versions.tf`:

```tf
// filepath: terraform/versions.tf
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  alias  = "us-west-2"
  region = "us-west-2"
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}
```

### 7.4 Monitoring & Alerting

**Step 7.4.1: Configure SNS for Alerts**

```bash
# Create SNS topic
aws sns create-topic --name terraform-alerts

# Subscribe email
aws sns subscribe \
    --topic-arn arn:aws:sns:us-west-2:ACCOUNT_ID:terraform-alerts \
    --protocol email \
    --notification-endpoint your-email@example.com
```

**Step 7.4.2: Update CloudWatch Alarms**

Add to environment `terraform/environments/dev/main.tf`:

```tf
// filepath: terraform/environments/dev/main.tf
// ...existing code...

resource "aws_sns_topic" "alerts" {
  name = "${var.environment}-infrastructure-alerts"
}

resource "aws_cloudwatch_metric_alarm" "ec2_status_check" {
  alarm_name          = "${var.environment}-ec2-status-check-failed"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = "0"
  alarm_description   = "EC2 instance status check failed"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    InstanceId = module.ec2.instance_id
  }
}

// ...existing code...
```

### 7.5 Documentation Updates

**Step 7.5.1: Update README**

Keep `README.md` current with:
- Architecture changes
- New modules added
- Updated workflows
- New security policies
- Contact information

**Step 7.5.2: Maintain Runbooks**

Create runbooks for common tasks:
- `docs/runbooks/deploy-new-environment.md`
- `docs/runbooks/rollback-deployment.md`
- `docs/runbooks/scale-infrastructure.md`

**Step 7.5.3: Document Lessons Learned**

After incidents or changes:
```markdown
# Incident Report - YYYY-MM-DD

## Issue
Brief description

## Impact
What was affected

## Root Cause
Why it happened

## Resolution
How it was fixed

## Prevention
Steps to prevent recurrence

## Action Items
- [ ] Update policy
- [ ] Add monitoring
- [ ] Document procedure
```

---

## Appendix

### A. Quick Reference Commands

```bash
# Initialize Terraform
terraform init

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Generate plan
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy resources
terraform destroy

# Show state
terraform state list
terraform state show <resource>

# Security scans
tflint
tfsec .
opa test policies/opa/

# AWS CLI
aws sts get-caller-identity
aws s3 ls
aws ec2 describe-instances
```

### B. Environment Variables

```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"

# Terraform Variables
export TF_VAR_environment="dev"
export TF_VAR_instance_type="t2.micro"
```

### C. Contact Information

**Team Contacts:**
- DevOps Lead: devops-lead@example.com
- Security Team: security@example.com
- On-Call: oncall@example.com

**Escalation Path:**
1. Team Lead
2. Engineering Manager
3. Director of Engineering

---

**Document Version:** 1.0  
**Last Updated:** January 15, 2026  
**Next Review:** Quarterly
