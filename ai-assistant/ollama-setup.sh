#!/bin/bash
# Ollama Local AI Setup Script for Agentic DevSecOps
# This script installs and configures Ollama with LLaMA 3.1 for FREE local AI

set -e

echo "=================================="
echo "Ollama AI Assistant Setup"
echo "FREE Local AI for DevSecOps"
echo "=================================="

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Windows;;
    MINGW*)     MACHINE=Windows;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected OS: ${MACHINE}"

# Install Ollama
install_ollama() {
    echo "Installing Ollama..."
    
    if [ "$MACHINE" == "Linux" ]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [ "$MACHINE" == "Mac" ]; then
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install ollama
    elif [ "$MACHINE" == "Windows" ]; then
        echo "For Windows, please download from: https://ollama.ai/download"
        echo "Or use WSL2 for Linux installation"
        exit 1
    fi
    
    echo "✅ Ollama installed successfully!"
}

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    install_ollama
else
    echo "✅ Ollama already installed"
    ollama --version
fi

# Start Ollama service
echo "Starting Ollama service..."
if [ "$MACHINE" == "Mac" ]; then
    brew services start ollama || ollama serve &
elif [ "$MACHINE" == "Linux" ]; then
    # Check if systemd service exists
    if systemctl is-active --quiet ollama; then
        echo "✅ Ollama service already running"
    else
        echo "Starting Ollama in background..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
fi

# Pull recommended models
echo ""
echo "Downloading AI models (this may take a few minutes)..."
echo "Models to install:"
echo "  1. llama3.1:8b - Best for code review and analysis (4.7GB)"
echo "  2. codellama:7b - Optimized for code generation (3.8GB)"
echo "  3. mistral:7b - Fast and efficient (4.1GB)"
echo ""

read -p "Which model would you like to install? (1/2/3 or 'all'): " MODEL_CHOICE

case $MODEL_CHOICE in
    1)
        echo "Pulling LLaMA 3.1:8b..."
        ollama pull llama3.1:8b
        DEFAULT_MODEL="llama3.1:8b"
        ;;
    2)
        echo "Pulling CodeLLaMA:7b..."
        ollama pull codellama:7b
        DEFAULT_MODEL="codellama:7b"
        ;;
    3)
        echo "Pulling Mistral:7b..."
        ollama pull mistral:7b
        DEFAULT_MODEL="mistral:7b"
        ;;
    all)
        echo "Pulling all models..."
        ollama pull llama3.1:8b
        ollama pull codellama:7b
        ollama pull mistral:7b
        DEFAULT_MODEL="llama3.1:8b"
        ;;
    *)
        echo "Invalid choice. Defaulting to LLaMA 3.1:8b"
        ollama pull llama3.1:8b
        DEFAULT_MODEL="llama3.1:8b"
        ;;
esac

echo "✅ Model(s) installed successfully!"

# Create configuration file
echo ""
echo "Creating configuration..."
cat > ../config/ai-config.yaml << EOF
# AI Assistant Configuration
ai:
  provider: ollama
  endpoint: http://localhost:11434
  model: ${DEFAULT_MODEL}
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
  enabled: false  # Set to true to enable automatic fixes
  require_approval: true

# Notification Settings
notifications:
  discord_webhook: ""  # Optional: Add your Discord webhook
  slack_webhook: ""    # Optional: Add your Slack webhook
EOF

echo "✅ Configuration created at config/ai-config.yaml"

# Test the setup
echo ""
echo "Testing Ollama setup..."
RESPONSE=$(ollama run ${DEFAULT_MODEL} "Hello, respond with 'AI is ready' if you can read this." --verbose=false 2>/dev/null || echo "Test failed")

if [[ $RESPONSE == *"AI is ready"* ]] || [[ $RESPONSE == *"ready"* ]]; then
    echo "✅ AI model is working correctly!"
else
    echo "⚠️ Warning: AI response may not be optimal. Response: $RESPONSE"
fi

# Create quick test script
cat > test-ai.sh << 'EOF'
#!/bin/bash
# Quick test script for Ollama AI

echo "Testing AI code review..."
ollama run llama3.1:8b "Review this Terraform code and identify security issues:

resource \"aws_security_group\" \"example\" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = \"tcp\"
    cidr_blocks = [\"0.0.0.0/0\"]
  }
}

Provide a brief security analysis."
EOF

chmod +x test-ai.sh

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Run './test-ai.sh' to test AI code review"
echo "  2. Configure webhooks in config/ai-config.yaml (optional)"
echo "  3. Run 'python pr-reviewer.py' to start AI PR reviews"
echo ""
echo "Model installed: ${DEFAULT_MODEL}"
echo "Ollama endpoint: http://localhost:11434"
echo ""
echo "Useful commands:"
echo "  - List models: ollama list"
echo "  - Run model: ollama run ${DEFAULT_MODEL}"
echo "  - Stop service: killall ollama"
echo ""
echo "For more models, visit: https://ollama.ai/library"
echo "=================================="
