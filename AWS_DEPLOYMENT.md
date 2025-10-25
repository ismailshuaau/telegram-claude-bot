# 🚀 AWS Deployment Guide - Singapore Region

Complete guide to deploy the Telegram Claude Code bot to AWS EC2 in Singapore (ap-southeast-1) for 24/7 access from Vietnam.

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ AWS Account
- ✅ AWS CLI installed on your Mac (or use AWS Console)
- ✅ Your Telegram bot token
- ✅ Your Telegram user ID
- ✅ Claude Code subscription (Pro/Max)
- ✅ GitHub account with SSH access to your projects
- ✅ Termius app on Android

---

## 💰 Expected Costs

```
t3a.xlarge spot (ap-southeast-1):  ~$42/month
100GB gp3 storage:                 ~$10/month
Data transfer:                      ~$2/month
────────────────────────────────────────────
Total:                             ~$54/month
```

---

## 🎯 Step 1: Launch EC2 Instance (10 minutes)

### Option A: AWS Console (Recommended for First Time)

1. **Go to EC2 Dashboard:**
   - https://ap-southeast-1.console.aws.amazon.com/ec2/

2. **Click "Launch Instance"**

3. **Configure Instance:**

   **Name:** `telegram-claude-bot`

   **Application and OS Images:**
   - **Quick Start:** Ubuntu
   - **Ubuntu Server 24.04 LTS (HVM), SSD Volume Type**
   - **Architecture:** 64-bit (x86)

   **Instance type:**
   - Click "Compare instance types"
   - Search for `t3a.xlarge`
   - Select: `t3a.xlarge` (4 vCPU, 16 GiB)

   **Key pair (login):**
   - Click "Create new key pair"
   - **Name:** `aws-vietnam-claude-bot`
   - **Key pair type:** ED25519
   - **Private key format:** .pem
   - **Download and SAVE the .pem file!** (You'll need it for Termius)

   **Network settings:**
   - ✅ Allow SSH traffic from: My IP (it will auto-detect your Vietnam IP)
   - ✅ Allow HTTPS traffic from the internet
   - ✅ Allow HTTP traffic from the internet

   **Configure storage:**
   - **Size:** 100 GiB
   - **Volume type:** gp3
   - **IOPS:** 3000
   - **Throughput:** 125 MB/s
   - ✅ Delete on termination

   **Advanced details:**
   - **Purchasing option:** ✅ Request Spot Instances
   - This gives you 70% discount!

4. **Review and Launch:**
   - Click "Launch instance"
   - Wait 2-3 minutes for instance to start

5. **Allocate Elastic IP:**
   - Go to "Elastic IPs" in EC2 sidebar
   - Click "Allocate Elastic IP address"
   - Click "Allocate"
   - Select the new IP → Actions → Associate Elastic IP address
   - Choose your instance → Associate
   - **Copy the Elastic IP** - you'll need it!

### Option B: AWS CLI (For Advanced Users)

```bash
# Launch instance
aws ec2 run-instances \
  --region ap-southeast-1 \
  --image-id ami-0c802847a7dd848c0 \
  --instance-type t3a.xlarge \
  --key-name aws-vietnam-claude-bot \
  --instance-market-options MarketType=spot \
  --block-device-mappings '[{
    "DeviceName": "/dev/sda1",
    "Ebs": {
      "VolumeSize": 100,
      "VolumeType": "gp3",
      "Iops": 3000,
      "Throughput": 125,
      "DeleteOnTermination": true
    }
  }]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=telegram-claude-bot}]'

# Allocate and associate Elastic IP
INSTANCE_ID=$(aws ec2 describe-instances \
  --region ap-southeast-1 \
  --filters "Name=tag:Name,Values=telegram-claude-bot" \
  --query 'Reservations[0].Instances[0].InstanceId' \
  --output text)

ALLOCATION_ID=$(aws ec2 allocate-address \
  --region ap-southeast-1 \
  --domain vpc \
  --query 'AllocationId' \
  --output text)

aws ec2 associate-address \
  --region ap-southeast-1 \
  --instance-id $INSTANCE_ID \
  --allocation-id $ALLOCATION_ID

# Get Elastic IP
aws ec2 describe-addresses \
  --region ap-southeast-1 \
  --allocation-ids $ALLOCATION_ID \
  --query 'Addresses[0].PublicIp' \
  --output text
```

---

## 🔌 Step 2: Connect from Termius (5 minutes)

### On Your Mac:

1. **Save the SSH key:**
   ```bash
   mv ~/Downloads/aws-vietnam-claude-bot.pem ~/.ssh/
   chmod 400 ~/.ssh/aws-vietnam-claude-bot.pem
   ```

2. **Test connection:**
   ```bash
   ssh -i ~/.ssh/aws-vietnam-claude-bot.pem ubuntu@YOUR_ELASTIC_IP
   ```

3. **Transfer key to Android:**
   - Option A: Email yourself the .pem file
   - Option B: Use cloud storage (Google Drive, Dropbox)
   - Option C: Use Termius sync feature

### On Your Android:

See detailed guide: [TERMIUS_GUIDE.md](TERMIUS_GUIDE.md)

**Quick steps:**
1. Install Termius from Play Store
2. Import the .pem key file
3. Add host with Elastic IP
4. Connect!

---

## 🛠️ Step 3: Initial Setup on EC2 (20 minutes)

### Connect via Termius and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verify Node.js
node --version  # Should show v20.x.x
npm --version

# Install Python 3.12 (should be pre-installed on Ubuntu 24.04)
python3 --version  # Should show 3.12.x

# Install pip
sudo apt install -y python3-pip python3-venv

# Install Git
sudo apt install -y git

# Install useful tools
sudo apt install -y htop tmux curl wget

# Install Claude Code CLI
sudo npm install -g @anthropic-ai/claude-code

# Verify Claude Code
claude --version  # Should show Claude Code version
```

---

## 🔑 Step 4: Login to Claude Code (5 minutes)

```bash
# Login to Claude
claude login

# Follow the prompts:
# 1. Opens a URL (copy to your phone browser)
# 2. Login with your Claude account
# 3. Authorize the device
# 4. Return to terminal

# Verify login
claude --version
```

---

## 📦 Step 5: Set Up GitHub Access (5 minutes)

```bash
# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "your-email@example.com"
# Press Enter for default location
# Press Enter for no passphrase (or set one)

# Display public key
cat ~/.ssh/id_ed25519.pub

# Copy the output and add to GitHub:
# 1. Go to https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Title: "AWS EC2 Singapore"
# 4. Paste the public key
# 5. Click "Add SSH key"

# Test connection
ssh -T git@github.com
# Should see: "Hi YourUsername! You've successfully authenticated..."
```

---

## 📥 Step 6: Clone Projects (5 minutes)

```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone your main project (ChefVision)
git clone git@github.com:Chef-Vision-AI/chefvision-analytics-platform.git
cd chefvision-analytics-platform
git submodule update --init --recursive

# Clone telegram bot
cd ~/projects
git clone git@github.com:ismailshuaau/telegram-claude-bot.git
```

---

## 🤖 Step 7: Deploy Telegram Bot (10 minutes)

```bash
cd ~/projects/telegram-claude-bot

# Install Python dependencies
pip3 install python-telegram-bot

# Create environment file
nano .env
```

**Add to .env file:**
```bash
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ALLOWED_USER_IDS=YOUR_TELEGRAM_ID_HERE
PROJECT_DIR=/home/ubuntu/projects/chefvision-analytics-platform
```

**Save and exit:** Ctrl+O, Enter, Ctrl+X

**Test the bot manually:**
```bash
python3 telegram_proxy.py
```

**Test from Telegram:**
- Open Telegram on your phone
- Message your bot: `/start`
- Try: "What files are in this project?"

**If working, press Ctrl+C to stop**

---

## ⚙️ Step 8: Install as systemd Service (10 minutes)

```bash
# Create systemd service file
sudo nano /etc/systemd/system/telegram-claude-bot.service
```

**Copy the entire service file from:** [telegram-claude-bot.service](telegram-claude-bot.service)

Or use this content:
```ini
[Unit]
Description=Telegram Claude Code Proxy Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/projects/telegram-claude-bot
Environment="TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE"
Environment="ALLOWED_USER_IDS=YOUR_TELEGRAM_ID_HERE"
Environment="PROJECT_DIR=/home/ubuntu/projects/chefvision-analytics-platform"
ExecStart=/usr/bin/python3 /home/ubuntu/projects/telegram-claude-bot/telegram_proxy.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Replace YOUR_BOT_TOKEN_HERE and YOUR_TELEGRAM_ID_HERE with actual values!**

**Enable and start service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable telegram-claude-bot

# Start service
sudo systemctl start telegram-claude-bot

# Check status
sudo systemctl status telegram-claude-bot

# View logs
sudo journalctl -u telegram-claude-bot -f
```

**Test from Telegram - bot should respond instantly!**

---

## 🔐 Step 9: Install Tailscale (Optional but Recommended) (10 minutes)

Tailscale provides secure access without exposing SSH to the internet.

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale
sudo tailscale up

# Copy the auth URL and open in browser
# Login with Google/GitHub/Email
# Authorize the device

# Get your Tailscale IP
tailscale ip -4
# Should show something like: 100.x.x.x

# Copy this IP for Termius!
```

**On Android:**
1. Install Tailscale from Play Store
2. Login with same account
3. See your EC2 in device list
4. In Termius, add new host with IP: 100.x.x.x

**Lock down AWS Security Group:**
```bash
# Go to EC2 Console → Security Groups
# Find your instance's security group
# Remove SSH rule (port 22) from 0.0.0.0/0
# Now only accessible via Tailscale!
```

---

## 🎯 Step 10: Verify Everything Works

### Test Bot from Telegram:
```
You: /start
Bot: [Welcome message]

You: What files are in this project?
Bot: [Lists your project files]

You: Explain the Django settings
Bot: [Reads and explains settings.py]
```

### Check Service Status:
```bash
# Via Termius:
sudo systemctl status telegram-claude-bot

# Should show: active (running)
```

### Check Logs:
```bash
sudo journalctl -u telegram-claude-bot -f
```

---

## 🔄 Maintenance & Management

### Restart Bot:
```bash
sudo systemctl restart telegram-claude-bot
```

### Update Bot Code:
```bash
cd ~/projects/telegram-claude-bot
git pull origin main
sudo systemctl restart telegram-claude-bot
```

### View Logs:
```bash
# Live logs
sudo journalctl -u telegram-claude-bot -f

# Last 100 lines
sudo journalctl -u telegram-claude-bot -n 100

# Today's logs
sudo journalctl -u telegram-claude-bot --since today
```

### Stop Bot:
```bash
sudo systemctl stop telegram-claude-bot
```

### Disable Auto-Start:
```bash
sudo systemctl disable telegram-claude-bot
```

---

## 🐛 Troubleshooting

### Bot not responding:
```bash
# Check if service is running
sudo systemctl status telegram-claude-bot

# Check logs for errors
sudo journalctl -u telegram-claude-bot -n 50

# Test manually
cd ~/projects/telegram-claude-bot
python3 telegram_proxy.py
```

### "Claude Code not found":
```bash
# Reinstall Claude Code
sudo npm install -g @anthropic-ai/claude-code

# Login again
claude login
```

### "Unauthorized" from Telegram:
```bash
# Verify your Telegram ID
# Message @userinfobot in Telegram

# Update .env file
nano ~/projects/telegram-claude-bot/.env

# Restart service
sudo systemctl restart telegram-claude-bot
```

### Slow response times:
```bash
# Check system resources
htop

# If memory is full, consider upgrading instance
# Or reducing other running services
```

---

## 💡 Tips

1. **Use tmux for persistent sessions:**
   ```bash
   tmux new -s coding
   # Your session persists even if Termius disconnects
   # Reconnect with: tmux attach -t coding
   ```

2. **Set up aliases in ~/.bashrc:**
   ```bash
   alias bot-status='sudo systemctl status telegram-claude-bot'
   alias bot-logs='sudo journalctl -u telegram-claude-bot -f'
   alias bot-restart='sudo systemctl restart telegram-claude-bot'
   ```

3. **Monitor costs:**
   - Set up AWS billing alerts
   - Spot instances can be interrupted (rare for t3a)
   - If interrupted, instance auto-restarts

4. **Backup important data:**
   ```bash
   # Backup your project
   cd ~/projects
   tar -czf backup.tar.gz chefvision-analytics-platform/
   ```

---

## ✅ Success Checklist

- [ ] EC2 instance running in ap-southeast-1
- [ ] Elastic IP allocated and associated
- [ ] Can connect via Termius from Android
- [ ] Node.js and Python installed
- [ ] Claude Code CLI installed and logged in
- [ ] GitHub SSH access configured
- [ ] Projects cloned
- [ ] Telegram bot working manually
- [ ] systemd service running
- [ ] Bot responds on Telegram
- [ ] (Optional) Tailscale installed and configured

---

**🎉 Congratulations! Your bot is now running 24/7 on AWS!**

Code from anywhere - phone, tablet, laptop - via Telegram!
