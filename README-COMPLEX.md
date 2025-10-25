# Telegram Claude Code Bot 🤖

**Vibe Coding Interface via Telegram**

Code from anywhere - your phone, tablet, or any device with Telegram. This bot provides a natural language interface to Claude Code, allowing you to write code, fix bugs, run tests, and manage your project through simple chat messages or voice notes.

---

## 🚨 WHICH VERSION DO YOU WANT?

This repository contains **TWO implementations**. Choose based on your needs:

### 🌟 Simple Version (Recommended for Getting Started)

**Pure proxy to Claude Code CLI - Test locally in 10 minutes!**

📄 **Documentation:** [START_HERE.md](START_HERE.md) or [QUICK_START.md](QUICK_START.md)

**Best for:**
- ✅ Personal use (you're the only user)
- ✅ Full Claude Code capabilities via Telegram
- ✅ Natural conversations (not just coding)
- ✅ Testing locally on your Mac first
- ✅ Using your Claude subscription (Pro/Max)
- ✅ Simplicity (1 file, 3 env vars)

**What you get:**
- Chat with Claude Code exactly like our current conversation
- No restrictions, no system prompts
- Read/write files, run commands, discuss architecture
- Voice message support (Telegram auto-transcribes)

**Start here:** `./check-setup.sh` then `./start-local.sh`

### 🏗️ Complex Version (This README)

**Production-ready bot with multi-user support and safety features**

📄 **Documentation:** This README (below)

**Best for:**
- ✅ Multiple users with separate sessions
- ✅ Production deployment on AWS EC2
- ✅ Context switching (backend/frontend)
- ✅ Rate limiting and secret sanitization
- ✅ Structured responses with buttons
- ✅ Both API and CLI authentication

**What you get:**
- Specialized coding assistant
- Per-user session management
- Safety features (rate limiting, secret redaction)
- Git integration with buttons
- Parallel agent execution

---

**Not sure?** Read [COMPARISON.md](COMPARISON.md) to compare both versions.

**Want to test locally first?** Use the Simple Version - see [START_HERE.md](START_HERE.md)

---

# Complex Version Documentation (Below)

## ✨ Features

- 🎤 **Voice Coding** - Send voice messages (Telegram auto-transcribes)
- 💬 **Natural Language** - Just chat naturally about what you want to do
- 🔄 **Parallel Sessions** - Multiple coding contexts (backend, frontend, root)
- 🧪 **Automated Testing** - Run tests and see results instantly
- 📝 **File Diffs** - Review changes before committing
- 🔒 **Secure** - User authentication, rate limiting, secret sanitization
- 📱 **Mobile-First** - Optimized for coding on your phone
- 🔔 **Notifications** - Get notified when long tasks complete
- 🚀 **Git Integration** - Commit, push, pull from chat

## 🏗️ Architecture

```
Telegram App (Your Phone)
    ↓
Telegram Bot API
    ↓
EC2 Instance (m6i.2xlarge)
    ├── Telegram Bot Server (Python)
    ├── Claude Code Bridge
    ├── Claude API
    └── Your Codebase
```

## 📋 Prerequisites

### 1. Telegram Bot Token

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name: `My Dev Bot`
4. Choose a username: `mydevbot_bot` (must end in `_bot`)
5. Save the token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Your Telegram User ID

**Choose any method:**

**Method 1: Use a Telegram Bot** (Easiest)
1. Open Telegram
2. Search for [@userinfobot](https://t.me/userinfobot) (or @myidbot, @getidsbot)
3. Click "Start"
4. Copy your ID: `123456789`

**Method 2: Use Telegram Web** (Quick)
1. Go to https://web.telegram.org
2. Open any chat or "Saved Messages"
3. Look at the URL in your browser
4. Your ID is in the URL: `web.telegram.org/k/#123456789`

**Method 3: Use Our ID Finder Script** (Convenient)
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
python3 get-my-id.py
# Then message your bot - it shows your ID!
```

### 3. Claude Authentication - Choose ONE:

**Option A: Claude Subscription (CLI)**
- For users with Claude Pro/Max/Team/Enterprise
- Fixed monthly cost ($20-60/mo)
- Setup: Login via `claude-code login`
- Best for: Heavy users, personal development

**Option B: Anthropic API (Pay-per-use)**
- Pay only for what you use (~$0.06/session)
- No subscription needed
- Get API key from [Anthropic Console](https://console.anthropic.com/)
- Best for: Light users, production deployments

**See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed guide on both methods.**

### 4. EC2 Instance

**Recommended:** `m6i.2xlarge` (8 vCPU, 32GB RAM)

See [EC2 Setup Guide](#-ec2-instance-setup) below.

## 🚀 Quick Start

### Step 1: Launch EC2 Instance

```bash
# From your local machine
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type m6i.2xlarge \
  --key-name your-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --block-device-mappings '[{
    "DeviceName": "/dev/sda1",
    "Ebs": {
      "VolumeSize": 100,
      "VolumeType": "gp3",
      "Iops": 16000,
      "Throughput": 1000
    }
  }]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=telegram-claude-bot}]'

# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Associate with instance
aws ec2 associate-address \
  --instance-id i-xxxxx \
  --public-ip xx.xx.xx.xx
```

### Step 2: Run Setup Script

```bash
# SSH into EC2
ssh ubuntu@your-ec2-ip

# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_ORG/YOUR_PROJECT/main/telegram-claude-bot/scripts/setup-ec2.sh | bash

# Or if you have the repo cloned:
cd ~/your-project/telegram-claude-bot/scripts
bash setup-ec2.sh
```

### Step 3: Clone Your Project

```bash
# Clone the main project
cd ~
git clone https://github.com/YOUR_ORG/YOUR_PROJECT.git project

# Initialize submodules (if any)
cd project
git submodule update --init --recursive
```

### Step 4: Deploy Bot Code

```bash
# From your local machine
cd telegram-claude-bot

# Set EC2 host
export EC2_HOST="ubuntu@your-ec2-ip"

# Deploy
bash scripts/deploy.sh
```

### Step 5: Configure Environment

```bash
# On EC2 instance
cd ~/telegram-claude-bot

# Create .env from template
cp .env.template .env

# Edit .env
nano .env
```

Add your configuration:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=123456789,987654321  # Your Telegram user IDs

# Authentication - Choose ONE method:
# Option A: Use 'cli' if you have Claude subscription
# Option B: Use 'api' if you have Anthropic API key
# Option C: Use 'auto' to auto-detect (recommended)
AUTH_METHOD=auto

# If using API method, set your key:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# If using CLI method, no key needed (login separately with: claude-code login)

# Project Paths (adjust if needed)
PROJECT_ROOT=/home/ubuntu/project
BACKEND_PATH=/home/ubuntu/project/transcription-platform
FRONTEND_PATH=/home/ubuntu/project/expo-voice-analytics-mobile-app

# Bot Settings
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_REQUESTS_PER_MINUTE=10
SESSION_TIMEOUT=3600
LOG_LEVEL=INFO
```

### Step 5.5: Setup Authentication

**If using CLI method (Claude subscription):**

```bash
# Install Claude Code CLI (if not already installed)
npm install -g @anthropic-ai/claude-code

# Login to Claude
claude-code login
# Follow the prompts to authenticate with your Claude account

# Verify
claude-code --version
```

**If using API method:**

```bash
# Just ensure your API key is in .env
cat ~/telegram-claude-bot/.env | grep ANTHROPIC_API_KEY
# Should show: ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

**See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed setup guides.**

### Step 6: Start the Bot

```bash
# Install systemd service
sudo cp systemd/telegram-claude-bot.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable telegram-claude-bot
sudo systemctl start telegram-claude-bot

# Check status
sudo systemctl status telegram-claude-bot

# View logs
sudo journalctl -u telegram-claude-bot -f
```

### Step 7: Test the Bot

1. Open Telegram
2. Search for your bot: `@mydevbot_bot`
3. Send `/start`
4. Try a command: "What's the project status?"

## 📱 Usage Examples

### Text Commands

```
You: Fix the billing API authentication bug

Bot: 🔍 Analyzing billing authentication...
     Found issue in apps/billing/views.py:142

     ✅ Fixed webhook signature verification
     ✅ Updated tests
     ✅ All 47 tests passing

     📝 Modified 2 files:
       • apps/billing/views.py
       • apps/billing/tests/test_webhooks.py
```

### Voice Messages

```
You: 🎤 [Voice] "Add a new endpoint for team usage metrics"

Bot: 🎤 You said: Add a new endpoint for team usage metrics

     Processing...

     📋 Plan:
     1. Create TeamUsageMetrics model
     2. Add API endpoint
     3. Write tests

     Proceed? [Yes] [Modify]
```

### Quick Status Check

```
You: /status

Bot: 📊 Project Status

     Context: backend

     Git Status:
     ✅ Working tree clean

     Services:
     ✅ Django: Running
     ✅ Celery: Running
     ❌ Redis: Stopped

     [🧪 Run Tests] [🔨 Build]
```

### Context Switching

```
You: /context frontend

Bot: ✅ Switched to frontend context
     Working directory: /home/ubuntu/project/expo-voice-analytics-mobile-app
```

## 🛠️ Management

### Using the Management Script

```bash
# On EC2 instance
cd ~/telegram-claude-bot

# Make script executable
chmod +x scripts/manage.sh

# View available commands
./scripts/manage.sh

# Common operations
./scripts/manage.sh start      # Start bot
./scripts/manage.sh stop       # Stop bot
./scripts/manage.sh restart    # Restart bot
./scripts/manage.sh status     # Check status
./scripts/manage.sh logs       # Follow logs
./scripts/manage.sh test       # Test configuration
```

### Viewing Logs

```bash
# Real-time logs
sudo journalctl -u telegram-claude-bot -f

# Last 100 lines
sudo journalctl -u telegram-claude-bot -n 100

# Today's logs
sudo journalctl -u telegram-claude-bot --since today

# Errors only
sudo journalctl -u telegram-claude-bot -p err
```

### Updating the Bot

```bash
# Method 1: From local machine
cd telegram-claude-bot
bash scripts/deploy.sh

# Method 2: On EC2 instance
cd ~/telegram-claude-bot
./scripts/manage.sh update
```

## 🔒 Security

### Authentication

Only users in `ALLOWED_USER_IDS` can use the bot:

```bash
# In .env
ALLOWED_USER_IDS=123456789,987654321
```

### Rate Limiting

Default: 10 requests per minute per user

```bash
# In .env
MAX_REQUESTS_PER_MINUTE=10
```

### Secret Sanitization

The bot automatically redacts:
- API keys (Stripe, OpenAI, Anthropic, GitHub)
- Passwords and tokens
- Database connection strings
- AWS credentials

### Network Security

**Option 1: Security Group (Basic)**

```bash
# Allow SSH only from your IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32
```

**Option 2: Tailscale (Recommended)**

```bash
# On EC2
sudo tailscale up

# On your phone
# Install Tailscale app
# Connect to same account
# SSH via Tailscale IP (100.x.x.x)
```

## 🎯 Advanced Features

### Parallel Agent Execution

```
You: Work on 3 things in parallel:
     1. Fix TypeScript errors in mobile app
     2. Update Django API docs
     3. Run full test suite

Bot: 🤖 Launching 3 parallel agents...

     [Agent 1] Fixing TypeScript errors...
     [Agent 2] Updating API documentation...
     [Agent 3] Running tests...

     [Updates as agents complete...]
```

### Git Operations

```
You: Commit these changes with message "Fix billing webhook"

Bot: ✅ Changes committed

     Commit: a1b2c3d
     Message: Fix billing webhook
     Files: 3

     [Push to Remote] [View Diff]
```

### CI/CD Integration

```
You: Deploy to staging

Bot: 🚀 Starting deployment...

     ✅ Tests passed
     ✅ Docker image built
     ✅ Deployed to ECS
     ✅ Health checks passing

     Staging: https://staging.yourproject.com
```

## 💰 Cost Breakdown

### EC2 Instance (m6i.2xlarge)

**Usage:** 40 hours/month

- **On-Demand:** $0.384/hour = $15.36/month
- **Spot Instance:** ~$0.115/hour = $4.60/month (70% savings!)

### Storage

- **100GB gp3 (high IOPS):** ~$10/month

### Elastic IP

- **While running:** $0
- **While stopped:** $3.60/month

### Telegram & Claude

- **Telegram Bot API:** FREE
- **Claude API:** Your existing costs
- **Network transfer:** ~$1-2/month

**Total: $26-28/month (on-demand) or $15-17/month (spot)**

## 🐛 Troubleshooting

### Bot Not Responding

```bash
# Check if service is running
sudo systemctl status telegram-claude-bot

# Check logs for errors
sudo journalctl -u telegram-claude-bot -n 100

# Test configuration
cd ~/telegram-claude-bot
source venv/bin/activate
python -c "from config import config; config.validate()"
```

### "Unauthorized" Error

1. Get your Telegram ID from @userinfobot
2. Add it to `.env`:
   ```bash
   ALLOWED_USER_IDS=YOUR_ID,OTHER_IDS
   ```
3. Restart bot:
   ```bash
   sudo systemctl restart telegram-claude-bot
   ```

### Voice Messages Not Working

Telegram's automatic transcription requires:
1. User has voice-to-text enabled in settings
2. Voice message is in a supported language
3. Good audio quality

**Alternative:** Just send text messages instead

### Claude Code Timeouts

Increase timeout in `.env`:

```bash
CLAUDE_TIMEOUT=600  # 10 minutes
```

## 📚 File Structure

```
telegram-claude-bot/
├── bot.py                  # Main bot implementation
├── config.py               # Configuration management
├── auth.py                 # Authentication & security
├── claude_code_bridge.py   # Claude Code integration
├── requirements.txt        # Python dependencies
├── .env.template          # Environment template
├── .env                   # Your configuration (create this)
├── scripts/
│   ├── setup-ec2.sh       # EC2 setup automation
│   ├── deploy.sh          # Deployment script
│   └── manage.sh          # Management utilities
├── systemd/
│   └── telegram-claude-bot.service  # Systemd service
└── logs/                  # Bot logs
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

See main project license.

## 🆘 Support

- **Telegram Bot Issues:** Check logs with `sudo journalctl -u telegram-claude-bot -f`
- **Claude Code Issues:** See [Claude Code docs](https://docs.claude.com/claude-code)
- **EC2 Issues:** Check AWS CloudWatch logs

## 🎉 Tips for Best Experience

1. **Use voice messages** - Faster than typing on phone
2. **Switch contexts** - Use `/context` to work on different parts
3. **Review before commit** - Always check diffs before approving
4. **Use Tailscale** - More secure than exposing SSH
5. **Enable notifications** - Get alerted when tasks complete
6. **Start small** - Try simple requests first to understand how it works

---

**Happy Vibe Coding!** 🚀📱🤖
