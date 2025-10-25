#!/bin/bash
#
# Deployment script for Telegram Claude Bot
# Deploys bot to EC2 instance
#

set -e

# Configuration
EC2_HOST="${EC2_HOST:-ubuntu@your-ec2-instance}"
REMOTE_DIR="/home/ubuntu/telegram-claude-bot"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 Deploying Telegram Claude Bot to $EC2_HOST..."

# Check if SSH connection works
if ! ssh -o ConnectTimeout=5 $EC2_HOST "echo 'Connection OK'" > /dev/null 2>&1; then
    echo "❌ Cannot connect to $EC2_HOST"
    echo "Set EC2_HOST environment variable or update this script"
    exit 1
fi

# Copy bot files
echo "📦 Copying bot files..."
rsync -avz --exclude='venv' --exclude='__pycache__' --exclude='.env' --exclude='*.pyc' \
    "$LOCAL_DIR/" "$EC2_HOST:$REMOTE_DIR/"

# Copy systemd service
echo "⚙️  Installing systemd service..."
ssh $EC2_HOST "sudo cp $REMOTE_DIR/systemd/telegram-claude-bot.service /etc/systemd/system/"

# Install Python dependencies
echo "📚 Installing Python dependencies..."
ssh $EC2_HOST "cd $REMOTE_DIR && source venv/bin/activate && pip install -r requirements.txt"

# Reload systemd
echo "🔄 Reloading systemd..."
ssh $EC2_HOST "sudo systemctl daemon-reload"

# Restart service
echo "♻️  Restarting bot service..."
ssh $EC2_HOST "sudo systemctl restart telegram-claude-bot"

# Check status
echo "📊 Checking service status..."
ssh $EC2_HOST "sudo systemctl status telegram-claude-bot --no-pager"

echo "✅ Deployment complete!"
echo ""
echo "Useful commands:"
echo "  ssh $EC2_HOST 'sudo journalctl -u telegram-claude-bot -f'  # View logs"
echo "  ssh $EC2_HOST 'sudo systemctl status telegram-claude-bot'   # Check status"
echo "  ssh $EC2_HOST 'sudo systemctl stop telegram-claude-bot'     # Stop bot"
echo "  ssh $EC2_HOST 'sudo systemctl start telegram-claude-bot'    # Start bot"
