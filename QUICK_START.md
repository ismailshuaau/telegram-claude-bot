# 🚀 Quick Start - Test in 10 Minutes!

Follow these steps to test the Telegram bot on your Mac **right now**.

---

## Step 1: Install Claude Code CLI (5 min)

```bash
# Install globally via npm
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version

# Login with your Claude subscription
claude-code login
```

**Follow the login prompts** - you'll authenticate with your Claude.ai account (Pro/Max subscription).

---

## Step 2: Get Telegram Bot Token (2 min)

### Option A: Use Existing Bot
If you already created a bot, find the token from @BotFather.

### Option B: Create New Bot
1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Name it: `My Dev Bot`
5. Username: `mydevbot_123_bot` (must end with `_bot` and be unique)
6. **Copy the token** (looks like: `1234567890:ABCdef...`)

---

## Step 3: Get Your Telegram User ID (30 seconds)

**Choose any method:**

### Method 1: Use a Telegram Bot (Easiest)
1. Open Telegram
2. Search for `@userinfobot` (or `@myidbot`, `@getidsbot`)
3. Click "Start"
4. **Copy your ID** (e.g., `123456789`)

### Method 2: Use Telegram Web (Quick)
1. Go to https://web.telegram.org
2. Open any chat or "Saved Messages"
3. Look at the URL in your browser
4. **Your ID is in the URL:** `web.telegram.org/k/#123456789`

### Method 3: Use Our ID Finder Script (Convenient)
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
python3 get-my-id.py
# Then message your bot - it shows your ID!
```

---

## Step 4: Set Environment Variables (1 min)

```bash
# In your terminal (or add to ~/.zshrc for persistence):

export TELEGRAM_BOT_TOKEN="1234567890:ABCdef..."  # Your bot token from Step 2
export ALLOWED_USER_IDS="123456789"               # Your user ID from Step 3
export PROJECT_DIR="/path/to/your/project"

# Verify they're set:
echo $TELEGRAM_BOT_TOKEN
echo $ALLOWED_USER_IDS
echo $PROJECT_DIR
```

---

## Step 5: Run the Bot! (1 min)

```bash
# Navigate to the bot directory
cd /path/to/your/project/telegram-claude-bot

# Run the quick start script
./start-local.sh
```

**You should see:**
```
🚀 Starting Telegram Claude Code Proxy (Local Test)
✅ Configuration:
   Bot Token: 1234567890:ABCdef...
   Allowed Users: 123456789
   Project Dir: /path/to/your/project

🤖 Starting bot...
📱 Now open Telegram and message your bot!
```

---

## Step 6: Test in Telegram! 🎉

1. **Open Telegram** on your phone or desktop
2. **Find your bot** (search for the name you gave it)
3. **Send:** `/start`
4. **Try these messages:**

```
You: What files are in this project?
Bot: [Lists your actual project files]

You: Explain how the authentication works
Bot: [Reads your code and explains]

You: Hey Claude, how should I implement notifications?
Bot: [Discusses options based on your stack]
```

---

## 🎯 What to Expect

**✅ Working Correctly:**
- Bot responds to your messages
- Reads actual files from your project
- Can discuss architecture, code, and planning
- Conversation feels natural (like our chat here!)
- No restrictions on topics

**❌ Common Issues:**

### "Unauthorized"
→ Your Telegram ID is wrong. Message @userinfobot again.

### "claude-code not found"
→ Not installed or not in PATH:
```bash
npm install -g @anthropic-ai/claude-code
export PATH="$PATH:$(npm root -g)/../bin"
```

### "Not authenticated"
→ Not logged in:
```bash
claude-code login
```

### No response from bot
→ Check terminal logs for errors

---

## 🧪 Test Checklist

Test these scenarios to verify everything works:

- [ ] Bot responds to `/start`
- [ ] Bot lists files from your project
- [ ] Bot explains a piece of your code
- [ ] Bot can chat naturally (not just coding)
- [ ] Conversation context carries across messages
- [ ] Long responses split into multiple messages
- [ ] Bot can make code changes (try: "Add a comment to README.md")

---

## 🛑 Stop the Bot

```bash
# In the terminal where the bot is running:
Ctrl+C
```

---

## 🎨 Example Conversation

```
You: Hey Claude! What's in this project?

Bot: Let me check the project structure for you...

     [Reads files]

     This is your project. Let me check the structure...

     Backend (Django):
     - 11 apps with 67 models
     - REST API with 60+ endpoints
     - Celery for background tasks
     - WebSocket support with Channels

     Frontend (React Native):
     - 70+ components
     - 40+ screens
     - Cross-platform (iOS/Android)

     What would you like to explore?

You: Show me the billing implementation

Bot: [Reads apps/billing/, explains in detail]

You: Can we add a feature to export invoices?

Bot: Absolutely! Let me think about the best approach...

     [Discusses options, then implements if you approve]
```

---

## 🚀 Next Steps

Once this works locally:

1. **Use it for real work!** Fix bugs, add features from your phone
2. **Deploy to AWS EC2** for 24/7 access (separate guide)
3. **Code from anywhere** via Telegram

---

## 💡 Pro Tips

**Tip 1:** Keep the terminal visible to watch what Claude is doing

**Tip 2:** Test with real tasks - "Fix that bug in the billing module"

**Tip 3:** Use voice messages in Telegram - they auto-transcribe!

**Tip 4:** Add to ~/.zshrc so env vars persist:
```bash
echo 'export TELEGRAM_BOT_TOKEN="your-token"' >> ~/.zshrc
echo 'export ALLOWED_USER_IDS="your-id"' >> ~/.zshrc
echo 'export PROJECT_DIR="/your/project/path"' >> ~/.zshrc
```

---

## 📚 Full Documentation

- **LOCAL_TEST.md** - Detailed testing guide with troubleshooting
- **README-SIMPLE.md** - Complete documentation
- **COMPARISON.md** - Simple vs Complex version comparison

---

## ✅ Ready to Start!

```bash
# Set your 3 environment variables:
export TELEGRAM_BOT_TOKEN="..."
export ALLOWED_USER_IDS="..."
export PROJECT_DIR="..."

# Run it:
cd telegram-claude-bot
./start-local.sh

# Then open Telegram and chat!
```

**This is Claude Code in your pocket! 🚀📱**
