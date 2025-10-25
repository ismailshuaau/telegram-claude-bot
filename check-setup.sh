#!/bin/bash
#
# Setup verification script
# Checks if everything is ready for testing the Telegram bot
#

echo "🔍 Checking setup for Telegram Claude Code Proxy..."
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Claude Code CLI
echo "1️⃣ Checking Claude Code CLI..."
if command -v claude-code &> /dev/null; then
    VERSION=$(claude-code --version 2>&1 || echo "unknown")
    echo "   ✅ claude-code is installed: $VERSION"
elif command -v claude &> /dev/null; then
    VERSION=$(claude --version 2>&1 || echo "unknown")
    # Check if it's actually Claude Code (not just the old claude cli)
    if echo "$VERSION" | grep -q "Claude Code"; then
        echo "   ✅ claude is installed (Claude Code): $VERSION"
    else
        echo "   ⚠️  claude command found, but not Claude Code: $VERSION"
        echo "      Install Claude Code with: npm install -g @anthropic-ai/claude-code"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ❌ Claude Code NOT installed"
    echo "      Install with: npm install -g @anthropic-ai/claude-code"
    echo "      Then login: claude-code login (or: claude login)"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 2: Python and dependencies
echo "2️⃣ Checking Python and dependencies..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Python installed: $PYTHON_VERSION"

    # Check python-telegram-bot
    if python3 -c "import telegram" 2>/dev/null; then
        echo "   ✅ python-telegram-bot installed"
    else
        echo "   ❌ python-telegram-bot NOT installed"
        echo "      Install with: pip3 install python-telegram-bot"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ❌ Python 3 NOT installed"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 3: Telegram Bot Token
echo "3️⃣ Checking TELEGRAM_BOT_TOKEN..."
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "   ✅ TELEGRAM_BOT_TOKEN is set: ${TELEGRAM_BOT_TOKEN:0:20}..."
else
    echo "   ❌ TELEGRAM_BOT_TOKEN NOT set"
    echo "      Get token from @BotFather in Telegram"
    echo "      Set with: export TELEGRAM_BOT_TOKEN='your-token'"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Allowed User IDs
echo "4️⃣ Checking ALLOWED_USER_IDS..."
if [ -n "$ALLOWED_USER_IDS" ]; then
    echo "   ✅ ALLOWED_USER_IDS is set: $ALLOWED_USER_IDS"
else
    echo "   ⚠️  ALLOWED_USER_IDS NOT set (bot will accept anyone!)"
    echo "      Get your ID from @userinfobot in Telegram"
    echo "      Set with: export ALLOWED_USER_IDS='your-id'"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check 5: Project Directory
echo "5️⃣ Checking PROJECT_DIR..."
if [ -n "$PROJECT_DIR" ]; then
    if [ -d "$PROJECT_DIR" ]; then
        echo "   ✅ PROJECT_DIR is set and exists: $PROJECT_DIR"
    else
        echo "   ⚠️  PROJECT_DIR is set but directory doesn't exist: $PROJECT_DIR"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "   ℹ️  PROJECT_DIR NOT set (will use current directory)"
    echo "      Set with: export PROJECT_DIR='/path/to/your/project'"
fi
echo ""

# Check 6: Bot script
echo "6️⃣ Checking telegram_proxy.py..."
if [ -f "telegram_proxy.py" ]; then
    echo "   ✅ telegram_proxy.py found"
else
    echo "   ❌ telegram_proxy.py NOT found"
    echo "      Are you in the correct directory?"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo "🎉 All checks passed! You're ready to start the bot!"
        echo ""
        echo "Run: ./start-local.sh"
    else
        echo "⚠️  Setup complete with $WARNINGS warning(s)"
        echo "   You can start the bot, but review warnings above"
        echo ""
        echo "Run: ./start-local.sh"
    fi
else
    echo "❌ Setup incomplete: $ERRORS error(s), $WARNINGS warning(s)"
    echo "   Fix the errors above before starting the bot"
    echo ""
    echo "Quick fixes:"
    echo ""
    echo "# Install Claude Code CLI:"
    echo "npm install -g @anthropic-ai/claude-code"
    echo "claude-code login"
    echo ""
    echo "# Install Python dependencies:"
    echo "pip3 install python-telegram-bot"
    echo ""
    echo "# Set environment variables:"
    echo "export TELEGRAM_BOT_TOKEN='your-bot-token'"
    echo "export ALLOWED_USER_IDS='your-telegram-id'"
    echo "export PROJECT_DIR='/path/to/your/project'"
    echo ""
    echo "Then run: ./check-setup.sh again"
fi

echo ""
