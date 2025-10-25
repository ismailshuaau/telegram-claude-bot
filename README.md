# Telegram Claude Code Proxy

**True Claude Code via Telegram - Full capabilities, zero restrictions!**

A **pure proxy** that connects Telegram to Claude Code CLI. Code from anywhere, anytime - it's like having Claude Code in your pocket!

---

## 🎯 What This Does

**Telegram = Remote interface to Claude Code CLI**

```
You type in Telegram
    ↓
Forwards to Claude Code CLI on your machine
    ↓
Claude reads/writes files, runs commands, analyzes code
    ↓
Response sent back to Telegram
    ↓
You receive it on your phone
```

**NO restrictions, NO special logic, NO limitations!**

Just like chatting with Claude Code directly, but via Telegram instead of a desktop app.

---

## ✨ Features

✅ **Full Claude Code capabilities**
- Everything Claude Code can do, you can do via Telegram
- Read files, write code, edit files, run commands
- Natural conversation about ANYTHING
- Code explanations, planning, debugging, implementation

✅ **Simple & Clean**
- One Python file (350 lines)
- 3 environment variables
- No complex configuration

✅ **Uses Your Claude Subscription**
- No API costs
- Included in your Pro/Max subscription
- Fixed monthly cost

✅ **Works Anywhere**
- Code from your phone
- Send voice messages
- Get instant responses
- Persistent sessions

---

## 🚀 Quick Start

### Prerequisites

1. **Telegram Bot Token** (from @BotFather)
2. **Your Telegram User ID** (see methods below)
3. **Claude Code CLI** (with your subscription)
   ```bash
   npm install -g @anthropic-ai/claude-code
   claude-code login
   ```

#### How to Get Your Telegram User ID

**Method 1: Use a Telegram Bot** (Easiest)
```
1. Open Telegram
2. Search for: @userinfobot (or @myidbot, @getidsbot)
3. Click "Start"
4. Bot shows your User ID
```

**Method 2: Use Telegram Web** (Quick)
```
1. Go to: https://web.telegram.org
2. Open any chat or "Saved Messages"
3. Look at the URL in your browser
4. Your ID is in the URL: web.telegram.org/k/#123456789
```

**Method 3: Use Our ID Finder Script** (Convenient)
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
python3 get-my-id.py
# Then message your bot - it shows your ID!
```

### Local Testing (Test on Mac First!)

```bash
# 1. Set environment variables
export TELEGRAM_BOT_TOKEN="1234567890:ABCdef..."
export ALLOWED_USER_IDS="123456789"
export PROJECT_DIR="/Users/you/your-project"

# 2. Install dependency
pip3 install python-telegram-bot

# 3. Run the bot
python3 telegram_proxy.py

# Or use the quick start script:
./start-local.sh
```

**See [LOCAL_TEST.md](LOCAL_TEST.md) for detailed testing guide!**

---

## 📱 Usage Examples

### General Conversation

```
You: "Hey Claude, how are you?"
Bot: "I'm doing well! Connected to your project.
     What would you like to work on today?"

You: "Explain how webhooks work"
Bot: [Full explanation of webhooks]

You: "Now show me how they're implemented in our code"
Bot: [Reads your code, explains YOUR implementation]
```

### Code Reading

```
You: "What's in the billing module?"
Bot: [Lists directory contents]

     apps/billing/
     ├── __init__.py
     ├── models.py
     ├── views.py
     ├── serializers.py
     └── tests/

You: "Explain the models.py file"
Bot: [Reads file, explains each model with code snippets]
```

### Code Editing

```
You: "Add logging to all payment-related functions"
Bot: "I'll add logging to the payment functions. Let me review
     what we have first..."

     [Reads code]

     "Found 5 payment functions:
     - process_payment()
     - validate_card()
     - handle_refund()
     - update_subscription()
     - cancel_subscription()

     Adding logging to each..."

     [Edits files]

     "Done! Added logging to all 5 functions.
     Files modified:
     - apps/billing/views.py
     - apps/billing/services.py

     Want me to show you the changes?"
```

### Planning & Discussion

```
You: "Should we use WebSockets or polling for real-time notifications?"
Bot: "Great question! Let's consider both options for your stack...

     WebSockets (via Django Channels):
     Pros:
     - True real-time, bidirectional
     - You already have Redis (needed for Channels)
     - Works well with Celery

     Cons:
     - More complex infrastructure
     - Requires WebSocket support on mobile

     Polling:
     Pros:
     - Simple to implement
     - Works everywhere
     - Easy to debug

     Cons:
     - Not truly real-time
     - More server load
     - Battery drain on mobile

     Given your React Native app and existing Redis setup,
     I'd recommend WebSockets via Django Channels.

     Want me to show you an implementation?"
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN="1234567890:ABCdef..."  # From @BotFather

# Recommended
ALLOWED_USER_IDS="123456789,987654321"     # Comma-separated Telegram IDs

# Optional
PROJECT_DIR="/path/to/project"             # Defaults to current directory
```

### File Structure

```
telegram-claude-bot/
├── telegram_proxy.py           # The bot (this is all you need!)
├── requirements-simple.txt     # Just python-telegram-bot
├── check-setup.sh             # Setup verification
├── get-my-id.py              # Get your Telegram ID
├── start-local.sh            # Quick start script
├── README.md                 # This file
├── QUICK_START.md            # 10-minute setup guide
├── LOCAL_TEST.md             # Detailed testing guide
└── START_HERE.md             # Getting started overview
```

---

## 🧪 Testing Locally

**Before deploying to AWS, test on your Mac!**

1. **Follow [LOCAL_TEST.md](LOCAL_TEST.md)**
2. **Run ./start-local.sh**
3. **Chat with your bot in Telegram**
4. **Verify it works like Claude Code**
5. **Then deploy to AWS if you want 24/7 access**

---

## 🚀 Deploy to AWS (Optional)

Once local testing works, deploy to EC2 for 24/7 access:

```bash
# On EC2:
1. Install Claude Code CLI
2. Login: claude-code login
3. Set environment variables
4. Run: python3 telegram_proxy.py

# Or use systemd for auto-restart
# See DEPLOY_TO_AWS.md (coming soon!)
```

---

## 💬 Real Conversation Example

```
You: "I'm thinking about refactoring the authentication system"

Bot: "That's a good idea! What's prompting this refactor?"

You: "The User model is doing too much - auth, permissions, profile"

Bot: "I see the problem. Let me look at your current implementation..."

     [Reads apps/authentication/models.py]

     "You're absolutely right. The User model has:
     - Authentication logic (login, password reset)
     - Authorization (permissions, roles)
     - Profile data (name, email, avatar)
     - Team membership
     - Billing info

     That's way too many responsibilities. I'd suggest:

     1. Keep User for auth only
     2. Create UserProfile for profile data
     3. Create separate Permission model
     4. Move team to existing Team model
     5. Move billing to existing Subscription model

     This follows single responsibility principle.
     Want me to create a refactoring plan?"

You: "Yes, show me the plan"

Bot: [Creates detailed refactoring plan with steps]

You: "Looks good, start with splitting out the profile"

Bot: [Creates migration, new model, updates references]

     "Done! Created:
     - UserProfile model
     - Migration to move data
     - Updated all references
     - Tests still pass

     Next step: permissions?"
```

**This is a REAL conversation you can have!**

---

## ❓ FAQ

### Q: Is this safe?

**A:** It's as safe as Claude Code on your desktop:
- Only authorized Telegram users can access (ALLOWED_USER_IDS)
- Claude Code runs with your user permissions
- Same access as running Claude Code locally
- Review changes before committing to git

### Q: Will my code be sent to Anthropic?

**A:** Same as Claude Code:
- Yes, code is sent to Claude API for analysis
- Covered by Anthropic's privacy policy
- No different than using Claude Code desktop app

### Q: Can I use this for multiple projects?

**A:** Yes!
- Change PROJECT_DIR environment variable
- Or tell Claude to change directory in conversation
- "Claude, let's work on my other project at /path/to/other"

### Q: Does this work with voice messages?

**A:** Yes! Use Telegram's voice-to-text feature:
- Hold the mic button 🎤
- Swipe up ⬆️ (this converts voice to text)
- Release and send
- Bot receives it as text message and responds normally

### Q: Can multiple people use the same bot?

**A:** Current version: One shared session
- Everyone shares same conversation
- Not ideal for teams (consider separate bots per user)
- For multi-user with separate sessions, you'd need to modify the code

### Q: What if Claude Code crashes?

**A:** Bot auto-restarts the session
- Error message sent to Telegram
- Next message starts fresh session
- Conversation history lost (session-based only)

---

## 🐛 Troubleshooting

### Bot doesn't respond

```bash
# Check logs in terminal where bot is running
# Should see: "User 123456789: message..."

# Common issues:
1. Wrong Telegram ID → Message @userinfobot again
2. Claude Code not logged in → claude-code login
3. Bot token wrong → Check @BotFather
```

### "No response received"

```bash
# Claude Code session crashed
# Restart bot: Ctrl+C then ./start-local.sh
```

### Timeout errors

```bash
# Claude is taking too long (>5 min)
# Normal for complex tasks
# Increase timeout in telegram_proxy.py line ~106
```

---

## 💡 Tips

**Tip 1: Keep it running**
- Use tmux/screen on server
- Or systemd service for auto-restart
- Bot maintains persistent session

**Tip 2: Use for real work**
- Don't just test, actually use it!
- Fix real bugs from your phone
- Add real features on the go
- True mobile development

**Tip 3: Voice messages**
- Faster than typing on phone
- Hold mic button and swipe up to convert to text
- Just speak naturally

**Tip 4: Long conversations**
- Context carries across messages
- Refer to previous responses
- Natural back-and-forth

---

## 🎉 That's It!

**One file. Three environment variables. Full Claude Code via Telegram.**

```bash
# Test locally right now:
./start-local.sh

# Then chat with Claude in Telegram!
```

**Questions? Check [QUICK_START.md](QUICK_START.md) or [LOCAL_TEST.md](LOCAL_TEST.md)**

---

**Happy vibe coding! 🚀📱🤖**
