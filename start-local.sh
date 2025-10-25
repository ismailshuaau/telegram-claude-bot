#!/bin/bash
#
# Quick start script for local testing
# Run this to test the Telegram bot on your Mac
#

set -e

echo "🚀 Starting Telegram Claude Code Proxy (Local Test)"
echo ""

# Check for bot token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set!"
    echo ""
    echo "Get your token:"
    echo "1. Message @BotFather in Telegram"
    echo "2. Send: /newbot"
    echo "3. Follow prompts"
    echo "4. Copy the token"
    echo ""
    echo "Then run:"
    echo "  export TELEGRAM_BOT_TOKEN='your-token-here'"
    echo "  $0"
    exit 1
fi

# Check for user ID
if [ -z "$ALLOWED_USER_IDS" ]; then
    echo "⚠️  ALLOWED_USER_IDS not set!"
    echo ""
    echo "Get your Telegram ID:"
    echo "1. Message @userinfobot in Telegram"
    echo "2. Note your ID"
    echo ""
    echo "Then run:"
    echo "  export ALLOWED_USER_IDS='your-id-here'"
    echo "  $0"
    echo ""
    read -p "Continue anyway? Bot will accept anyone! (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set default project dir if not set
if [ -z "$PROJECT_DIR" ]; then
    export PROJECT_DIR="$(pwd)"
    echo "📁 PROJECT_DIR not set, using current directory:"
    echo "   $PROJECT_DIR"
    echo ""
fi

# Check if claude-code or claude is installed
CLAUDE_CMD=""
if command -v claude-code &> /dev/null; then
    CLAUDE_CMD="claude-code"
elif command -v claude &> /dev/null; then
    # Check if it's actually Claude Code
    if claude --version 2>&1 | grep -q "Claude Code"; then
        CLAUDE_CMD="claude"
    fi
fi

if [ -z "$CLAUDE_CMD" ]; then
    echo "❌ Claude Code not found!"
    echo ""
    echo "Install with:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "Then login with:"
    echo "  claude-code login  (or: claude login)"
    exit 1
fi

echo "✅ Found Claude Code: $CLAUDE_CMD"
echo ""

# Check if logged in to Claude
if ! $CLAUDE_CMD --version &> /dev/null; then
    echo "⚠️  Claude Code CLI might not be authenticated"
    echo ""
    echo "Login with:"
    echo "  $CLAUDE_CMD login"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if python-telegram-bot is installed
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "📦 Installing python-telegram-bot..."
    pip3 install python-telegram-bot
    echo ""
fi

echo "✅ Configuration:"
echo "   Bot Token: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "   Allowed Users: ${ALLOWED_USER_IDS:-Anyone (⚠️ not recommended)}"
echo "   Project Dir: $PROJECT_DIR"
echo ""

echo "🤖 Starting bot..."
echo ""
echo "📱 Now open Telegram and message your bot!"
echo "   Send /start to begin"
echo ""
echo "Press Ctrl+C to stop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the bot
python3 telegram_proxy.py
