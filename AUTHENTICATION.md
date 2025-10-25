# Authentication Methods Guide

The Telegram Claude Bot supports **TWO authentication methods**. Choose the one that works best for you!

---

## 🎯 Quick Comparison

| Factor | Claude Subscription (CLI) | Anthropic API |
|--------|---------------------------|---------------|
| **Cost Structure** | Fixed monthly ($20-60/mo) | Pay-per-use (~$0.06/session) |
| **Best For** | Heavy users, personal dev | Light users, production |
| **Setup** | Login once | API key in .env |
| **Billing** | Subscription includes usage | Billed to API account |
| **Requirements** | Claude Pro/Max/Team/Enterprise | Anthropic Console account |

---

## Option 1: Claude Subscription (CLI Method) ⭐

**Use this if:** You already have a Claude Pro, Max, Team, or Enterprise subscription

### What You Need

- Claude subscription ($20/mo for Pro, $60/mo for Max)
- Claude Code CLI installed on your EC2 instance

### Setup Steps

#### Step 1: Get Claude Subscription

1. Go to https://claude.ai/
2. Subscribe to Pro ($20/month) or Max ($60/month)
3. Or use your Team/Enterprise account

#### Step 2: Install Claude Code CLI on EC2

```bash
# SSH into your EC2 instance
ssh ubuntu@your-ec2-ip

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version
```

#### Step 3: Login to Claude

```bash
# Start login process
claude-code login

# This will:
# 1. Open a browser (or give you a URL to visit)
# 2. Ask you to login to Claude
# 3. Authorize the CLI
# 4. Save your credentials
```

**Note:** On a headless server (EC2), you may need to:

```bash
# Get the login URL
claude-code login

# Copy the URL it gives you
# Open it on your local machine
# Complete authentication
# The EC2 instance will automatically detect success
```

#### Step 4: Configure Bot

```bash
cd ~/telegram-claude-bot
cp .env.template .env
nano .env
```

Set:

```bash
# Use CLI authentication
AUTH_METHOD=cli

# No API key needed!
# Leave ANTHROPIC_API_KEY commented out
```

#### Step 5: Start Bot

```bash
sudo systemctl start telegram-claude-bot
```

### Benefits

✅ **Fixed cost** - Included in your subscription
✅ **No usage limits** - Use as much as you want
✅ **Same account** - Use your personal Claude account
✅ **Simpler billing** - One monthly charge

### Limitations

⚠️ Requires active subscription ($20-60/month)
⚠️ CLI must stay logged in on EC2
⚠️ If subscription expires, bot stops working

---

## Option 2: Anthropic API (API Key Method) 💳

**Use this if:** You want pay-per-use billing or don't have a Claude subscription

### What You Need

- Anthropic Console account (free to create)
- Credit card for API billing

### Setup Steps

#### Step 1: Create Anthropic Account

1. Go to https://console.anthropic.com/
2. Sign up (or login)
3. Add payment method

#### Step 2: Create API Key

1. In console, go to "API Keys"
2. Click "Create Key"
3. Name it: `telegram-bot`
4. Copy the key: `sk-ant-api03-xxxxxxxxxxxxx`
5. **Save it!** (You can't see it again)

#### Step 3: Configure Bot

```bash
cd ~/telegram-claude-bot
cp .env.template .env
nano .env
```

Set:

```bash
# Use API authentication
AUTH_METHOD=api

# Set your API key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

#### Step 4: Start Bot

```bash
sudo systemctl start telegram-claude-bot
```

### Benefits

✅ **Pay only for what you use** - No subscription needed
✅ **Scales automatically** - Handle any usage level
✅ **Multiple bots** - Use same key for multiple instances
✅ **Better for production** - Designed for programmatic use

### Limitations

⚠️ Variable costs (but usually cheap: ~$0.06/session)
⚠️ Requires API key management
⚠️ Need to monitor usage

### Cost Examples

**Real usage estimates:**

```
Typical coding session:
- Read 10,000 tokens (code + context): $0.03
- Generate 2,000 tokens (code + response): $0.03
- Total per session: ~$0.06

Monthly costs:
- 10 sessions/month: $0.60
- 50 sessions/month: $3.00
- 100 sessions/month: $6.00
- 200 sessions/month: $12.00
```

**When API becomes more expensive than subscription:**
- If you do 350+ sessions/month, subscription is cheaper
- That's ~12 sessions per day

---

## Option 3: Auto-Detect (Recommended) 🤖

**Use this if:** You want the bot to automatically choose the best method

### How It Works

```bash
# In .env
AUTH_METHOD=auto
```

The bot will:
1. Check if Claude Code CLI is installed and logged in
2. If yes → Use CLI
3. If no → Check for ANTHROPIC_API_KEY
4. If yes → Use API
5. If neither → Show error

### Benefits

✅ **Flexible** - Works with either method
✅ **Fallback** - Tries both if one fails
✅ **Automatic** - No manual configuration

### Setup

```bash
# In .env
AUTH_METHOD=auto

# Then either:
# A) Login to Claude CLI (if you have subscription)
claude-code login

# B) Or set API key (if you prefer API)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Or both! Bot will prefer CLI, fallback to API
```

---

## 🔄 Switching Between Methods

You can switch anytime!

### From CLI to API

```bash
nano ~/.telegram-claude-bot/.env

# Change:
AUTH_METHOD=cli
# to:
AUTH_METHOD=api
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Restart:
sudo systemctl restart telegram-claude-bot
```

### From API to CLI

```bash
# Login to Claude
claude-code login

# Update config
nano ~/.telegram-claude-bot/.env

# Change:
AUTH_METHOD=api
# to:
AUTH_METHOD=cli

# Restart
sudo systemctl restart telegram-claude-bot
```

---

## 🧪 Testing Your Setup

```bash
# Test configuration
cd ~/telegram-claude-bot
source venv/bin/activate
python -c "from config import config; config.validate()"

# Should show:
# ✅ Using Claude Code CLI authentication
# or:
# ✅ Using Anthropic API authentication

# Check logs when starting bot:
sudo journalctl -u telegram-claude-bot -f

# Look for:
# "Using auth method: cli"
# or:
# "Using auth method: api"
```

---

## 🐛 Troubleshooting

### CLI Method Issues

**"Claude CLI not available"**

```bash
# Install CLI
npm install -g @anthropic-ai/claude-code

# Login
claude-code login

# Verify
claude-code --version
```

**"Not authenticated"**

```bash
# Re-login
claude-code logout
claude-code login
```

**"CLI command not found"**

```bash
# Check PATH
which claude-code

# If not found, add to PATH:
export PATH="$PATH:$(npm root -g)/../bin"
```

### API Method Issues

**"ANTHROPIC_API_KEY not set"**

```bash
# Check .env
cat ~/telegram-claude-bot/.env | grep ANTHROPIC

# Should see:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

**"Invalid API key"**

```bash
# Get new key from:
# https://console.anthropic.com/settings/keys

# Update .env
nano ~/telegram-claude-bot/.env

# Restart bot
sudo systemctl restart telegram-claude-bot
```

**"API quota exceeded"**

- Check your billing: https://console.anthropic.com/settings/billing
- Add more credits
- Or switch to CLI method if you have subscription

---

## 💡 Recommendations

### For Personal Development

**Use CLI method** if you:
- Already have Claude Pro/Max subscription
- Use Claude a lot personally
- Want predictable costs

### For Production/Team Use

**Use API method** if you:
- Need to scale to multiple users
- Want usage-based billing
- Share bot across team
- Don't have Claude subscription

### For Testing

**Use 'auto' mode** with both configured:
- Best reliability (automatic fallback)
- Test both methods
- Seamless switching

---

## 📊 Cost Comparison Examples

### Scenario 1: Light User (10 sessions/month)

| Method | Monthly Cost |
|--------|--------------|
| **CLI** (requires Pro) | $20 |
| **API** (pay per use) | $0.60 ⭐ **Best** |

**Recommendation:** API

### Scenario 2: Medium User (50 sessions/month)

| Method | Monthly Cost |
|--------|--------------|
| **CLI** (requires Pro) | $20 |
| **API** (pay per use) | $3 ⭐ **Best** |

**Recommendation:** API (or CLI if you already have subscription for other use)

### Scenario 3: Heavy User (400 sessions/month)

| Method | Monthly Cost |
|--------|--------------|
| **CLI** (requires Pro) | $20 ⭐ **Best** |
| **API** (pay per use) | $24 |

**Recommendation:** CLI with Claude Pro subscription

### Scenario 4: Very Heavy User (1000+ sessions/month)

| Method | Monthly Cost |
|--------|--------------|
| **CLI** (requires Max) | $60 ⭐ **Best** |
| **API** (pay per use) | $60+ |

**Recommendation:** CLI with Claude Max subscription

---

**Summary:** Most users should start with **API method** for flexibility. Switch to CLI if you exceed ~350 sessions/month or already have a Claude subscription.

---

**Need help?** Check bot logs: `sudo journalctl -u telegram-claude-bot -f`
