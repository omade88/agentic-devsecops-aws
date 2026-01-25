# Security Policy

## Sensitive Data Protection

This repository contains infrastructure-as-code for AWS deployments. **NEVER commit sensitive information** such as:

### ❌ DO NOT COMMIT:
- AWS Access Keys or Secret Keys
- Email addresses
- S3 bucket names (if they contain sensitive identifiers)
- DynamoDB table names (if they contain sensitive identifiers)
- Slack/Discord webhook URLs
- GitHub Personal Access Tokens
- SSH private keys
- SSL/TLS certificates
- IP addresses (unless they're example IPs like `203.0.113.0/24`)
- Any credentials or secrets

### ✅ How to Handle Sensitive Data:

1. **Use `.env` files (gitignored)**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env with your actual values
   # .env is in .gitignore and will NOT be committed
   ```

2. **Use GitHub Secrets for CI/CD**
   - Repository Settings → Secrets and variables → Actions
   - Add: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc.
   - Never hardcode in workflow files

3. **Use Terraform Variables**
   - Create `terraform.tfvars` with your values
   - `terraform.tfvars` is gitignored
   - Use `terraform.tfvars.example` for templates

4. **Use AWS Systems Manager Parameter Store**
   - Store secrets in AWS SSM Parameter Store
   - Reference them in Terraform using data sources
   - Never hardcode in `.tf` files

### 🔒 Before Pushing to GitHub:

```bash
# Check for sensitive data
git diff

# Review what will be committed
git status

# Use git-secrets to scan
git secrets --scan

# Check for hardcoded credentials
grep -r "aws_access_key" .
grep -r "secret" . --include="*.tf" --include="*.tfvars"
```

### 📋 Example IPs in This Repo

The following are **TEST-NET IPs** (RFC 5737) and are safe to commit:
- `203.0.113.0/24` - TEST-NET-3
- `198.51.100.0/24` - TEST-NET-2
- `192.0.2.0/24` - TEST-NET-1

Replace these with your actual IPs in your local `terraform.tfvars`.

### 🚨 If You Accidentally Commit Secrets:

1. **Immediately rotate the credentials** (delete and create new ones)
2. **Remove from Git history:**
   ```bash
   # Use BFG Repo-Cleaner or git filter-branch
   bfg --replace-text passwords.txt
   git push --force
   ```
3. **Report to security@github.com** if it's a serious leak

### 📧 Reporting Security Issues

If you discover a security vulnerability, please email:
- **DO NOT** create a public GitHub issue
- Email: [Create a security advisory](https://github.com/<your-username>/agentic-devsecops-aws/security/advisories/new)
- We will respond within 48 hours

### ✅ Safe to Commit:

- Terraform modules (`.tf` files without secrets)
- Example configurations (`.example` files)
- Documentation
- Scripts (without hardcoded credentials)
- Lambda function code (without API keys)
- GitHub Actions workflows (using `${{ secrets.* }}` references)

### 🔐 Best Practices:

1. **Use environment variables** for all sensitive data
2. **Enable branch protection** on main/production branches
3. **Require pull request reviews** before merging
4. **Enable GitHub secret scanning** (free for public repos)
5. **Use AWS IAM roles** instead of access keys when possible
6. **Rotate credentials regularly** (every 90 days minimum)
7. **Use least-privilege access** for all IAM policies
8. **Enable MFA** on AWS root account
9. **Review AWS CloudTrail logs** for suspicious activity
10. **Keep dependencies updated** (run `dependabot` or `renovate`)

---

**Remember**: Once credentials are pushed to GitHub, assume they are compromised, even if you delete the commit. Always rotate immediately!
