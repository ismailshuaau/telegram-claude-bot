# 🧪 Local Testing Guide

Test the Telegram Claude Code Proxy on your Mac **RIGHT NOW** before deploying to AWS!

---

## ✅ Prerequisites

### 1. Telegram Bot Token

If you don't have one yet:
```bash
# 1. Open Telegram
# 2. Message @BotFather
# 3. Send: /newbot
# 4. Name: Test Dev Bot
# 5. Username: your_test_bot (must end with _bot)
# 6. Save the token!
```

### 2. Your Telegram User ID

**Choose any method:**

**Method 1: Use a Telegram Bot** (Easiest)
```bash
# 1. Open Telegram
# 2. Search for: @userinfobot (or @myidbot, @getidsbot)
# 3. Click "Start"
# 4. Copy your ID (e.g., 123456789)
```

**Method 2: Use Telegram Web** (Quick)
```bash
# 1. Go to: https://web.telegram.org
# 2. Open any chat or "Saved Messages"
# 3. Look at the URL in your browser
# 4. Your ID is in the URL: web.telegram.org/k/#123456789
```

**Method 3: Use Our ID Finder Script** (Convenient)
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
python3 get-my-id.py
# Then message your bot - it shows your ID!
```

### 3. Claude Code CLI

```bash
# Check if installed:
claude-code --version

# If not installed:
npm install -g @anthropic-ai/claude-code

# Login (using your Claude subscription):
claude-code login
# Follow the prompts to authenticate
```

### 4. Python Dependencies

```bash
# Install Telegram bot library:
pip install python-telegram-bot
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Set Environment Variables

```bash
# In your terminal (or add to ~/.zshrc):

export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export ALLOWED_USER_IDS="123456789"  # Your Telegram ID
export PROJECT_DIR="/path/to/your/project"

# Verify:
echo $TELEGRAM_BOT_TOKEN
echo $ALLOWED_USER_IDS
echo $PROJECT_DIR
```

### Step 2: Run the Proxy

```bash
# Navigate to telegram-claude-bot directory:
cd /path/to/your/project/telegram-claude-bot

# Run the proxy:
python3 telegram_proxy.py
```

**You should see:**
```
2025-10-25 10:30:00 - __main__ - INFO - 🚀 Starting Telegram Claude Code Proxy...
2025-10-25 10:30:00 - __main__ - INFO - Project directory: /path/to/your/project
2025-10-25 10:30:00 - __main__ - INFO - Allowed users: [123456789]
2025-10-25 10:30:01 - __main__ - INFO - Starting Claude Code session...
2025-10-25 10:30:02 - __main__ - INFO - ✅ Claude Code session started
2025-10-25 10:30:02 - __main__ - INFO - ✅ Bot starting...
```

### Step 3: Test in Telegram!

**On your phone/Telegram:**

1. **Find your bot:**
   - Search for the bot username you created
   - Or use the link from @BotFather

2. **Start the bot:**
   ```
   /start
   ```

3. **Try chatting:**
   ```
   You: "What files are in this project?"

   Bot: [Lists files from your project directory]

   You: "Explain how the authentication works"

   Bot: [Reads your code and explains]

   You: "What should I work on today?"

   Bot: [Analyzes your project, suggests tasks]
   ```

---

## 🧪 Test Scenarios

### Test 1: General Conversation ✅

```
You: "Hey Claude, how are you?"

Bot: "I'm doing well! I'm connected to your project.
     Ready to help with anything - coding, planning, or just chatting.

     What would you like to work on?"
```

**Expected:** Natural response, NO restrictions

### Test 2: Code Reading ✅

```
You: "What's in the transcription-platform directory?"

Bot: [Reads directory, lists contents]
```

**Expected:** Actual file listing from YOUR project

### Test 3: Code Explanation ✅

```
You: "Explain the billing module"

Bot: [Reads apps/billing/, explains architecture]
```

**Expected:** Detailed explanation using YOUR actual code

### Test 4: Code Editing ✅

```
You: "Add a comment to the top of apps/billing/views.py"

Bot: [Edits file, shows diff]

     "✅ Added comment to apps/billing/views.py"
```

**Expected:** File actually modified on your Mac!

### Test 5: Planning & Discussion ✅

```
You: "Should we use WebSockets or polling for real-time updates?"

Bot: [Discusses pros/cons, gives recommendation based on YOUR stack]
```

**Expected:** Thoughtful discussion, no "I'm just a coding bot" response

### Test 6: Multi-Turn Conversation ✅

```
You: "I'm thinking about refactoring the auth system"

Bot: "That's a good idea! What's prompting this?"

You: "The code is getting messy with too many responsibilities"

Bot: "I see. Let me look at the current implementation..."
     [Reads code]
     "You're right - the User model is doing authentication,
      authorization, AND profile management.

      I'd suggest..."
```

**Expected:** Continuous conversation with context

---

## 🐛 Troubleshooting

### Bot doesn't respond

**Check logs in terminal:**
```
# You should see:
User 123456789: What files are in this project?...
```

**If you see "Unauthorized":**
```bash
# Your Telegram ID is wrong
# Message @userinfobot again to get correct ID
export ALLOWED_USER_IDS="correct-id-here"
# Restart bot
```

### "claude-code not found"

```bash
# Install Claude Code CLI:
npm install -g @anthropic-ai/claude-code

# Verify:
which claude-code

# If still not found, check PATH:
export PATH="$PATH:$(npm root -g)/../bin"
```

### "Not authenticated"

```bash
# Login to Claude:
claude-code login

# Follow prompts to authenticate
```

### Response timeout

```bash
# Claude Code is taking too long
# Increase timeout in telegram_proxy.py:
# Line ~106: timeout = 300  # Change to 600 (10 minutes)
```

### "No response received"

```bash
# Claude Code session might have crashed
# Check logs in terminal
# Restart the bot: Ctrl+C then python telegram_proxy.py
```

---

## ✅ What to Test

### Must Test (Critical)

- [ ] /start command works
- [ ] Can send and receive messages
- [ ] Bot reads actual files from your project
- [ ] Bot can edit files (check file actually changes!)
- [ ] Conversation continues across messages
- [ ] No "I'm just a coding bot" restrictions

### Should Test (Important)

- [ ] Long messages (>4096 chars) split correctly
- [ ] Code blocks render properly
- [ ] Multiple concurrent messages
- [ ] Bot recovers from errors

### Nice to Test (Optional)

- [ ] Voice messages (Telegram's transcription)
- [ ] Multiple users (add another ID to ALLOWED_USER_IDS)
- [ ] Different project directories

---

## 📊 Performance Check

**Expected response times:**
- Simple queries: 2-5 seconds
- Code reading: 5-10 seconds
- Code editing: 10-30 seconds
- Complex analysis: 30-120 seconds

**If slower:**
- Your Mac is doing all the work
- Claude Code CLI takes time to read/analyze
- Normal for complex tasks

---

## 🎯 Success Criteria

**You'll know it's working when:**

✅ You can have a natural conversation
✅ Bot reads YOUR actual project files
✅ Bot can make real code changes
✅ No "I'm just a coding assistant" limitations
✅ Context carries across messages
✅ It feels like chatting with Claude Code (this!) via Telegram

---

## 🔄 Stopping the Bot

```bash
# In terminal where bot is running:
Ctrl+C

# You'll see:
Shutting down...
Claude Code session stopped
```

---

## 📝 Quick Reference

### Start Bot
```bash
cd telegram-claude-bot
python telegram_proxy.py
```

### Stop Bot
```bash
Ctrl+C
```

### Check Logs
```bash
# Logs appear in terminal in real-time
# Look for:
# - User messages
# - Claude responses
# - Errors
```

### Change Project Directory
```bash
export PROJECT_DIR="/path/to/different/project"
python telegram_proxy.py
```

---

## 🚀 Next Steps After Testing

Once local testing works:

1. **Deploy to EC2** (see DEPLOY_TO_AWS.md)
2. **Run 24/7** as a systemd service
3. **Code from anywhere** via Telegram!

---

## 💡 Tips

**Tip 1: Keep terminal visible**
- See what Claude is doing in real-time
- Useful for debugging
- Watch file operations happen

**Tip 2: Test with your actual work**
- Ask about real bugs you're facing
- Request actual features you need
- Use it for real development

**Tip 3: Test the limits**
- Ask non-coding questions
- Have long conversations
- Test complex tasks
- See if it feels like Claude Code (it should!)

---

## 🎉 Ready to Test!

```bash
# 1. Set env vars
export TELEGRAM_BOT_TOKEN="your-token"
export ALLOWED_USER_IDS="your-id"
export PROJECT_DIR="/path/to/project"

# 2. Run bot
python telegram_proxy.py

# 3. Open Telegram and chat!
```

**Have fun! This is Claude Code in your pocket!** 🚀📱
