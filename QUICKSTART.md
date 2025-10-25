# 🚀 Quick Start Guide

Get your Telegram Claude Code Bot running in 15 minutes!

## Step 1: Create Telegram Bot (2 minutes)

1. Open Telegram
2. Message @BotFather
3. Send: `/newbot`
4. Name: `My Dev Bot`
5. Username: `my_dev_bot` (must end with `_bot`)
6. **Save the token!** `1234567890:ABCdef...`

## Step 2: Get Your Telegram ID (1 minute)

1. Message @userinfobot
2. **Save your ID!** `123456789`

## Step 3: Choose Authentication Method (2 minutes)

**Pick ONE option:**

### Option A: Claude Subscription (Recommended if you have it)

1. Have Claude Pro/Max subscription? Use this!
2. **No key needed** - you'll login on EC2
3. Fixed cost: $20-60/month

### Option B: Anthropic API (Recommended for most users)

1. Go to https://console.anthropic.com/
2. Create API key
3. **Save the key!** `sk-ant-api03-xxxxx`
4. Pay-per-use: ~$0.06/session

**See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed comparison**

## Step 4: Launch EC2 (5 minutes)

```bash
# Set your variables
export KEY_NAME="your-ssh-key"
export SECURITY_GROUP="sg-xxxxx"
export SUBNET="subnet-xxxxx"

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type m6i.2xlarge \
  --key-name $KEY_NAME \
  --security-group-ids $SECURITY_GROUP \
  --subnet-id $SUBNET \
  --block-device-mappings '[{
    "DeviceName": "/dev/sda1",
    "Ebs": {"VolumeSize": 100, "VolumeType": "gp3"}
  }]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=telegram-bot}]'

# Note the instance ID from output
export INSTANCE_ID="i-xxxxx"

# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Note the public IP from output
export ELASTIC_IP="xx.xx.xx.xx"

# Associate IP with instance
aws ec2 associate-address \
  --instance-id $INSTANCE_ID \
  --public-ip $ELASTIC_IP

# Wait for instance to be ready
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
```

## Step 5: Setup Instance (3 minutes)

```bash
# SSH into instance
ssh ubuntu@$ELASTIC_IP

# Clone this repo
git clone https://github.com/YOUR_ORG/chefvision-analytics-platform.git
cd chefvision-analytics-platform/telegram-claude-bot

# Run setup
bash scripts/setup-ec2.sh

# Clone your main project
cd ~
git clone https://github.com/YOUR_ORG/chefvision-analytics-platform.git project
cd project
git submodule update --init --recursive
```

## Step 6: Configure Bot (2 minutes)

```bash
cd ~/telegram-claude-bot

# Create .env
cp .env.template .env

# Edit .env
nano .env
```

**Minimal configuration needed:**

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...  # From Step 1
ALLOWED_USER_IDS=123456789               # From Step 2

# Authentication - Use ONE of these:
# Option A: Auto-detect (recommended)
AUTH_METHOD=auto

# Option B: If using API, set your key:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Option C: If using CLI, login separately (see Step 6.5)
```

Save and exit (Ctrl+X, Y, Enter)

## Step 6.5: Setup Authentication (1-2 minutes)

**If using Claude CLI (Option A from Step 3):**

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Login
claude-code login
# Follow prompts to authenticate
```

**If using API (Option B from Step 3):**

```bash
# Nothing to do - your API key is already in .env
```

## Step 7: Start Bot (1 minute)

```bash
# Copy bot files if not already there
cp -r ~/chefvision-analytics-platform/telegram-claude-bot/* ~/telegram-claude-bot/

# Install dependencies
cd ~/telegram-claude-bot
source venv/bin/activate
pip install -r requirements.txt

# Install systemd service
sudo cp systemd/telegram-claude-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-claude-bot
sudo systemctl start telegram-claude-bot

# Check status
sudo systemctl status telegram-claude-bot
```

## Step 8: Test! (1 minute)

1. Open Telegram
2. Search for your bot (the username from Step 1)
3. Click "Start" or send `/start`
4. Send a message: "What's the project status?"

**You should get a response!** 🎉

---

## Troubleshooting

### Bot doesn't respond?

```bash
# Check logs
sudo journalctl -u telegram-claude-bot -n 50

# Common issues:
# 1. Wrong token → Check .env
# 2. Wrong user ID → Message @userinfobot again
# 3. Service not running → sudo systemctl start telegram-claude-bot
```

### "Unauthorized" message?

Your Telegram ID is not in the allowed list:

```bash
# Get your ID from the bot's error message
# Add it to .env
nano ~/telegram-claude-bot/.env

# Add your ID to ALLOWED_USER_IDS
# Restart bot
sudo systemctl restart telegram-claude-bot
```

### Service fails to start?

```bash
# Check configuration
cd ~/telegram-claude-bot
source venv/bin/activate
python -c "from config import config; config.validate()"

# If validation fails, fix .env and restart
```

---

## Next Steps

Now that your bot is running:

1. **Try voice messages** - Send a voice note!
2. **Switch contexts** - `/context frontend`
3. **Check status** - `/status`
4. **Read full docs** - See [README.md](README.md)

---

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help |
| `/status` | Project status |
| `/context backend` | Switch to backend |
| `/context frontend` | Switch to frontend |

**Or just chat naturally:**
- "Fix the authentication bug"
- "Run tests"
- "Show me recent commits"
- "What's broken?"

---

**Total time:** ~15 minutes
**Cost:** ~$26/month (or $15/month with Spot instances)

🎉 **Happy coding!**
