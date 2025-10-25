#!/bin/bash
#
# EC2 Setup Script for Telegram Claude Code Bot
# Run this on a fresh Ubuntu 24.04 EC2 instance
#

set -e  # Exit on error

echo "========================================"
echo "🚀 EC2 Setup for Telegram Claude Bot"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if running on Ubuntu
if [ ! -f /etc/os-release ]; then
    print_error "Cannot detect OS. This script is for Ubuntu 24.04"
    exit 1
fi

. /etc/os-release
if [ "$ID" != "ubuntu" ]; then
    print_error "This script is for Ubuntu only. Detected: $ID"
    exit 1
fi

print_status "Detected Ubuntu $VERSION"

# Update system
print_info "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_status "System updated"

# Install Node.js 20.x
print_info "Installing Node.js 20.x..."
if command -v node &> /dev/null; then
    print_info "Node.js already installed: $(node --version)"
else
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
    print_status "Node.js installed: $(node --version)"
fi

# Verify npm
if command -v npm &> /dev/null; then
    print_status "npm installed: $(npm --version)"
else
    print_error "npm not found after Node.js installation"
    exit 1
fi

# Install Python 3.12 (should be pre-installed on Ubuntu 24.04)
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python3 installed: $PYTHON_VERSION"
else
    print_error "Python3 not found"
    exit 1
fi

# Install pip
print_info "Installing pip..."
sudo apt install -y python3-pip python3-venv
print_status "pip installed"

# Install Git
print_info "Installing Git..."
if command -v git &> /dev/null; then
    print_info "Git already installed: $(git --version)"
else
    sudo apt install -y git
    print_status "Git installed: $(git --version)"
fi

# Install useful tools
print_info "Installing useful tools..."
sudo apt install -y htop tmux curl wget unzip
print_status "Tools installed (htop, tmux, curl, wget, unzip)"

# Install Claude Code CLI
print_info "Installing Claude Code CLI..."
if command -v claude &> /dev/null; then
    print_info "Claude Code already installed: $(claude --version)"
elif command -v claude-code &> /dev/null; then
    print_info "Claude Code already installed: $(claude-code --version)"
else
    sudo npm install -g @anthropic-ai/claude-code
    if command -v claude &> /dev/null; then
        print_status "Claude Code installed: $(claude --version)"
    elif command -v claude-code &> /dev/null; then
        print_status "Claude Code installed: $(claude-code --version)"
    else
        print_error "Claude Code installation failed"
        exit 1
    fi
fi

# Create projects directory
print_info "Creating projects directory..."
mkdir -p ~/projects
print_status "Created ~/projects"

echo ""
echo "========================================"
echo "✅ EC2 Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Login to Claude Code:"
echo "   claude login"
echo ""
echo "2. Set up GitHub SSH access:"
echo "   ssh-keygen -t ed25519 -C \"your-email@example.com\""
echo "   cat ~/.ssh/id_ed25519.pub"
echo "   # Add the public key to GitHub: https://github.com/settings/keys"
echo ""
echo "3. Clone your projects:"
echo "   cd ~/projects"
echo "   git clone git@github.com:YOUR_ORG/YOUR_PROJECT.git"
echo "   git clone git@github.com:ismailshuaau/telegram-claude-bot.git"
echo ""
echo "4. Deploy the bot:"
echo "   cd ~/projects/telegram-claude-bot"
echo "   pip3 install python-telegram-bot"
echo "   # Configure .env file"
echo "   # Set up systemd service"
echo ""
echo "5. (Optional) Install Tailscale:"
echo "   curl -fsSL https://tailscale.com/install.sh | sh"
echo "   sudo tailscale up"
echo ""
echo "📚 See AWS_DEPLOYMENT.md for full deployment guide"
echo ""
