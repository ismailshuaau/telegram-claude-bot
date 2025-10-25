# 🚀 START HERE - Telegram Claude Code Proxy

Welcome! This is your **Telegram interface to Claude Code CLI** - code from anywhere via your phone!

---

## 🎯 What You Have

**✅ Already Set Up:**
- `telegram_proxy.py` - The bot (pure proxy to Claude Code)
- `python-telegram-bot` - Installed and ready
- Documentation and guides

**❌ Still Need:**
1. **Claude Code CLI** - Install and login
2. **Telegram Bot Token** - Get from @BotFather
3. **Your Telegram User ID** - Get from @userinfobot

---

## ⚡ Quick Start (Choose One)

### Option 1: Follow Quick Start Guide (Recommended)

```bash
# Open the quick start guide:
cat QUICK_START.md

# Or open in your editor:
open QUICK_START.md
```

**This walks you through the complete setup in 10 minutes.**

### Option 2: Check What You Need

```bash
# Run the setup checker:
./check-setup.sh

# It will tell you exactly what's missing
```

---

## 📋 Minimum Steps to Test

### 1. Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
claude-code login  # Login with your Claude subscription
```

### 2. Get Telegram Bot Token

1. Open Telegram
2. Message `@BotFather`
3. Send `/newbot` and follow prompts
4. Save the token

### 3. Get Your Telegram User ID

**Choose any method:**

**Method 1: Use a Telegram Bot** (Easiest)
1. Open Telegram
2. Search for `@userinfobot` (or `@myidbot`, `@getidsbot`)
3. Click "Start"
4. Copy your ID (e.g., 123456789)

**Method 2: Use Telegram Web** (Quick)
1. Go to https://web.telegram.org
2. Open any chat or "Saved Messages"
3. Look at the URL - your ID is in it: `web.telegram.org/k/#123456789`

**Method 3: Use Our ID Finder Script** (Convenient)
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
python3 get-my-id.py
# Then message your bot - it shows your ID!
```

### 4. Set Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your-token-from-botfather"
export ALLOWED_USER_IDS="your-id-from-userinfobot"
export PROJECT_DIR="/path/to/your/project"
```

### 5. Start the Bot!

```bash
./start-local.sh
```

### 6. Test in Telegram

Open Telegram, find your bot, send `/start` and start chatting!

---

## 📚 Full Documentation

| File | What It's For |
|------|---------------|
| **QUICK_START.md** | ⭐ Complete setup guide (start here!) |
| **check-setup.sh** | ⭐ Verify your setup is ready |
| **start-local.sh** | ⭐ Start the bot after setup |
| **LOCAL_TEST.md** | Detailed testing guide |
| **README-SIMPLE.md** | Full documentation |
| **COMPARISON.md** | Simple vs Complex version |
| **requirements-simple.txt** | Python dependencies |
| **telegram_proxy.py** | The bot code |

---

## 🎨 What This Does

```
You type in Telegram
    ↓
Forwards to Claude Code CLI on your Mac
    ↓
Claude reads/writes files, runs commands, analyzes code
    ↓
Response sent back to Telegram
    ↓
You receive it on your phone
```

**Just like chatting with Claude Code directly, but via Telegram!**

---

## ✅ Current Status

Run `./check-setup.sh` to see what you need:

```bash
./check-setup.sh
```

**Current needs:**
- [ ] Install Claude Code CLI
- [ ] Get Telegram bot token
- [ ] Get your Telegram user ID
- [x] Python installed ✅
- [x] python-telegram-bot installed ✅
- [x] Bot code ready ✅

---

## 🆘 Need Help?

### "Where do I start?"
→ Read **QUICK_START.md** (10 minute guide)

### "Is everything ready?"
→ Run `./check-setup.sh`

### "How do I install Claude Code?"
→ `npm install -g @anthropic-ai/claude-code`

### "How do I get a bot token?"
→ Message `@BotFather` in Telegram, send `/newbot`

### "How do I get my user ID?"
→ Message `@userinfobot` in Telegram

### "Is this safe?"
→ Yes! Only authorized users (your Telegram ID) can access it

### "Will this cost money?"
→ No API costs - uses your existing Claude subscription

---

## 🎯 Recommended Path

```bash
# 1. Check current status
./check-setup.sh

# 2. Install what's missing (follow the output)
npm install -g @anthropic-ai/claude-code
claude-code login

# 3. Get Telegram credentials
# - Message @BotFather for bot token
# - Message @userinfobot for your ID

# 4. Set environment variables
export TELEGRAM_BOT_TOKEN="..."
export ALLOWED_USER_IDS="..."
export PROJECT_DIR="..."

# 5. Verify setup
./check-setup.sh

# 6. Start the bot!
./start-local.sh

# 7. Open Telegram and chat!
```

---

## 🚀 Next Steps After Testing

Once local testing works:

1. **Use it for real work** - Fix bugs, add features from your phone
2. **Deploy to AWS EC2** - For 24/7 access (guide coming)
3. **Code from anywhere** - Beach, train, anywhere with Telegram!

---

## 💡 What You Can Do

Once running, you can:

✅ Chat naturally about anything
✅ Read files from your project
✅ Edit code
✅ Run commands
✅ Discuss architecture
✅ Fix bugs
✅ Plan features
✅ EVERYTHING Claude Code can do!

**No restrictions, no limitations - full Claude Code via Telegram!**

---

## 🎉 Ready?

```bash
# Start here:
cat QUICK_START.md

# Or jump right in:
./check-setup.sh
```

**This is Claude Code in your pocket! 🚀📱🤖**
