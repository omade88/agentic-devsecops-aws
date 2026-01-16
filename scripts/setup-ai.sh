#!/bin/bash
# Complete Setup Script for Agentic AI DevSecOps
# Installs all dependencies and configures the environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "Agentic AI DevSecOps Setup"
echo "FREE Infrastructure Automation with AI"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install on different OSes
install_package() {
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y "$1"
    elif command_exists yum; then
        sudo yum install -y "$1"
    elif command_exists brew; then
        brew install "$1"
    else
        echo "⚠️  Unable to install $1. Please install manually."
    fi
}

echo "Step 1: Checking prerequisites..."
echo ""

# Check Python
if ! command_exists python3; then
    echo "Installing Python 3..."
    install_package python3
fi
echo "✅ Python 3: $(python3 --version)"

# Check pip
if ! command_exists pip3; then
    echo "Installing pip..."
    if command_exists apt-get; then
        sudo apt-get install -y python3-pip
    else
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
fi
echo "✅ pip: $(pip3 --version)"

# Check AWS CLI
if ! command_exists aws; then
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
fi
echo "✅ AWS CLI: $(aws --version)"

# Check Terraform
if ! command_exists terraform; then
    echo "Installing Terraform..."
    wget -q https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
    unzip terraform_1.6.0_linux_amd64.zip
    sudo mv terraform /usr/local/bin/
    rm terraform_1.6.0_linux_amd64.zip
fi
echo "✅ Terraform: $(terraform --version | head -1)"

# Check Git
if ! command_exists git; then
    echo "Installing Git..."
    install_package git
fi
echo "✅ Git: $(git --version)"

echo ""
echo "Step 2: Installing security scanning tools..."
echo ""

# Install TFLint
if ! command_exists tflint; then
    echo "Installing TFLint..."
    curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
fi
echo "✅ TFLint installed"

# Install tfsec
if ! command_exists tfsec; then
    echo "Installing tfsec..."
    curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
fi
echo "✅ tfsec installed"

# Install OPA
if ! command_exists opa; then
    echo "Installing OPA..."
    curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
    chmod 755 opa
    sudo mv opa /usr/local/bin/
fi
echo "✅ OPA: $(opa version)"

# Install Checkov
if ! command_exists checkov; then
    echo "Installing Checkov..."
    pip3 install checkov
fi
echo "✅ Checkov installed"

echo ""
echo "Step 3: Installing Python dependencies..."
echo ""

# Install AI assistant dependencies
if [ -d "$PROJECT_ROOT/ai-assistant" ]; then
    echo "Installing AI assistant dependencies..."
    pip3 install -r "$PROJECT_ROOT/ai-assistant/requirements.txt"
fi

# Install ChatOps dependencies
if [ -d "$PROJECT_ROOT/chatops" ]; then
    echo "Installing ChatOps dependencies..."
    pip3 install -r "$PROJECT_ROOT/chatops/requirements.txt"
fi

echo "✅ Python dependencies installed"

echo ""
echo "Step 4: Setting up Ollama (Local AI)..."
echo ""

if command_exists ollama; then
    echo "✅ Ollama already installed"
else
    read -p "Install Ollama for local AI? (y/n): " install_ollama
    if [ "$install_ollama" = "y" ]; then
        cd "$PROJECT_ROOT/ai-assistant"
        bash ollama-setup.sh
    else
        echo "⏭️  Skipping Ollama installation"
    fi
fi

echo ""
echo "Step 5: Configuring AWS credentials..."
echo ""

if [ ! -f ~/.aws/credentials ]; then
    echo "AWS credentials not found. Let's configure them:"
    aws configure
else
    echo "✅ AWS credentials already configured"
    aws sts get-caller-identity > /dev/null 2>&1 && echo "✅ AWS credentials are valid" || echo "⚠️  AWS credentials may be invalid"
fi

echo ""
echo "Step 6: Setting up pre-commit hooks..."
echo ""

if ! command_exists pre-commit; then
    pip3 install pre-commit
fi

cd "$PROJECT_ROOT"
if [ ! -f .pre-commit-config.yaml ]; then
    cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint

  - repo: https://github.com/aquasecurity/tfsec
    rev: v1.28.1
    hooks:
      - id: tfsec
EOF
fi

pre-commit install
echo "✅ Pre-commit hooks installed"

echo ""
echo "Step 7: Creating configuration files..."
echo ""

# Create config directory
mkdir -p "$PROJECT_ROOT/config"

# Create AI config if it doesn't exist
if [ ! -f "$PROJECT_ROOT/config/ai-config.yaml" ]; then
    cat > "$PROJECT_ROOT/config/ai-config.yaml" << 'EOF'
# AI Assistant Configuration
ai:
  provider: ollama
  endpoint: http://localhost:11434
  model: llama3.1:8b
  temperature: 0.2
  max_tokens: 2000

# PR Review Settings
pr_review:
  enabled: true
  focus_areas:
    - security
    - best_practices
    - cost_optimization
    - compliance

# Auto-fix Settings
auto_fix:
  enabled: false
  require_approval: true

# Notification Settings
notifications:
  discord_webhook: ""
  slack_webhook: ""
EOF
fi

echo "✅ Configuration files created"

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure notifications (optional):"
echo "   - Edit config/ai-config.yaml"
echo "   - Add Discord/Slack webhook URLs"
echo ""
echo "2. Set up GitHub repository:"
echo "   - Push code to GitHub"
echo "   - Add secrets: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION"
echo "   - Enable branch protection on main branch"
echo ""
echo "3. Test the AI assistant:"
echo "   cd ai-assistant"
echo "   python3 pr-reviewer.py"
echo ""
echo "4. Deploy Lambda functions:"
echo "   cd terraform/environments/dev"
echo "   terraform init"
echo "   terraform plan"
echo "   terraform apply"
echo ""
echo "5. Generate policies with AI:"
echo "   cd ai-assistant"
echo "   python3 policy-generator.py --interactive"
echo ""
echo "Documentation:"
echo "  - Setup guide: docs/AI-SETUP-GUIDE.md"
echo "  - SOP: step_by_step.md"
echo "  - README: README.md"
echo ""
echo "========================================"
