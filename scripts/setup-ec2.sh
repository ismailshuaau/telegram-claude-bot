#!/bin/bash
#
# EC2 Setup Script for Telegram Claude Code Bot
# Optimized for m6i.2xlarge (8 vCPU, 32GB RAM)
#
# Usage: curl -fsSL <script-url> | bash
# Or: bash setup-ec2.sh
#

set -e

echo "🚀 Setting up EC2 instance for Telegram Claude Code Bot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    log_warn "Running as root. Some operations will adjust permissions for ubuntu user."
    USER_HOME="/home/ubuntu"
    RUN_USER="ubuntu"
else
    USER_HOME="$HOME"
    RUN_USER="$(whoami)"
fi

# Update system
log_info "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install essential packages
log_info "Installing essential packages..."
sudo apt-get install -y \
    git \
    curl \
    wget \
    vim \
    tmux \
    htop \
    iotop \
    nethogs \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql-client \
    redis-tools \
    ffmpeg \
    jq \
    unzip

# Install Node.js 18 LTS
log_info "Installing Node.js 18..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

node_version=$(node --version)
log_info "Node.js installed: $node_version"

# Install Claude Code CLI
log_info "Installing Claude Code CLI..."
if ! command -v claude-code &> /dev/null; then
    sudo npm install -g @anthropic-ai/claude-code
fi

claude_version=$(claude-code --version 2>&1 || echo "installed")
log_info "Claude Code installed: $claude_version"

# Install AWS CLI v2
log_info "Installing AWS CLI v2..."
if ! command -v aws &> /dev/null; then
    cd /tmp
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    sudo ./aws/install
    rm -rf awscliv2.zip aws
fi

aws_version=$(aws --version)
log_info "AWS CLI installed: $aws_version"

# Configure swap (16GB for 32GB RAM instance)
log_info "Configuring swap space..."
if [ ! -f /swapfile ]; then
    sudo dd if=/dev/zero of=/swapfile bs=1G count=16 status=progress
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    log_info "16GB swap configured"
else
    log_warn "Swap already configured"
fi

# Kernel optimizations
log_info "Applying kernel optimizations..."
sudo tee -a /etc/sysctl.conf > /dev/null <<EOF

# Telegram Claude Bot optimizations
fs.file-max = 2097152
fs.nr_open = 2097152
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 8192
EOF

sudo sysctl -p > /dev/null

# Increase ulimits
log_info "Increasing file descriptor limits..."
sudo tee -a /etc/security/limits.conf > /dev/null <<EOF
$RUN_USER soft nofile 65536
$RUN_USER hard nofile 65536
$RUN_USER soft nproc 32768
$RUN_USER hard nproc 32768
EOF

# Setup Python virtual environment
log_info "Setting up Python environment..."
cd $USER_HOME
if [ ! -d "telegram-claude-bot" ]; then
    mkdir -p telegram-claude-bot
fi

cd telegram-claude-bot

if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi

source venv/bin/activate

# Install Python dependencies
log_info "Installing Python dependencies..."
pip install --upgrade pip

cat > requirements.txt <<EOF
python-telegram-bot[job-queue]==20.7
anthropic==0.18.1
asyncio==3.4.3
aiofiles==23.2.1
python-dotenv==1.0.0
EOF

pip install -r requirements.txt

# Create directory structure
log_info "Creating directory structure..."
mkdir -p logs
mkdir -p config
mkdir -p systemd

# Create .env template
log_info "Creating .env template..."
cat > .env.template <<EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your-bot-token-here
ALLOWED_USER_IDS=123456789,987654321

# Claude API
ANTHROPIC_API_KEY=your-anthropic-key-here

# OpenAI (optional, for Whisper if not using Telegram transcription)
# OPENAI_API_KEY=your-openai-key-here

# Project Paths
PROJECT_ROOT=/home/ubuntu/project
BACKEND_PATH=/home/ubuntu/project/transcription-platform
FRONTEND_PATH=/home/ubuntu/project/expo-voice-analytics-mobile-app

# Bot Settings
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_REQUESTS_PER_MINUTE=10
SESSION_TIMEOUT=3600
LOG_LEVEL=INFO

# Features
ENABLE_NOTIFICATIONS=true
NOTIFY_ON_ERROR=true
NOTIFY_ON_COMPLETION=true
EOF

log_info ".env.template created. Copy to .env and configure!"

# Install Tailscale (optional but recommended for security)
log_info "Installing Tailscale (optional)..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "Tailscale installed. Run 'sudo tailscale up' to connect"
else
    log_warn "Tailscale already installed"
fi

# Configure tmux for mobile coding
log_info "Configuring tmux..."
cat > $USER_HOME/.tmux.conf <<EOF
# Tmux configuration for mobile coding
set -g mouse on
set -g history-limit 100000
set -g prefix C-a
unbind C-b
bind C-a send-prefix
set -g status-position top
set -g status-style bg=colour235,fg=colour136
set -g pane-border-style fg=colour235
set -g pane-active-border-style fg=colour136
set -g display-panes-time 3000

# Quick pane switching
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D
EOF

# Create log directory
sudo mkdir -p /var/log/telegram-claude-bot
sudo chown $RUN_USER:$RUN_USER /var/log/telegram-claude-bot

# Set correct ownership
if [ "$EUID" -eq 0 ]; then
    chown -R ubuntu:ubuntu $USER_HOME/telegram-claude-bot
fi

log_info "✅ EC2 setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next steps:"
echo "1. Clone your project to /home/ubuntu/project"
echo "2. Copy bot files to /home/ubuntu/telegram-claude-bot/"
echo "3. Configure .env with your tokens"
echo "4. Setup systemd service (see systemd/telegram-claude-bot.service)"
echo "5. Start the bot!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To get your Telegram user ID, message @userinfobot"
echo "To get bot token, message @BotFather"
echo ""
