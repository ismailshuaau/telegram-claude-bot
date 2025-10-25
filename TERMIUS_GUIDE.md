# 📱 Termius Setup Guide for Android

Complete guide to connect to your AWS EC2 instance from your Android phone using Termius.

---

## 📥 Step 1: Install Termius

1. Open **Google Play Store**
2. Search for **"Termius"**
3. Install **Termius - SSH client** (by Termius Corporation)
4. Open the app

---

## 🔑 Step 2: Import SSH Key

### Option A: From Email/Cloud Storage

1. **Save the .pem file to your Android:**
   - Email yourself the `aws-vietnam-claude-bot.pem` file
   - Or upload to Google Drive/Dropbox
   - Download to your Android device

2. **In Termius app:**
   - Tap the menu (≡) → **Keychain**
   - Tap **Keys** tab
   - Tap the **+** button
   - Tap **Import from file**
   - Navigate to Downloads folder
   - Select `aws-vietnam-claude-bot.pem`
   - **Label:** `AWS Vietnam`
   - Tap **Save**

### Option B: Copy-Paste Key Content

1. **On your Mac, display the key:**
   ```bash
   cat ~/.ssh/aws-vietnam-claude-bot.pem
   ```

2. **Copy the entire output** (including BEGIN and END lines)

3. **In Termius app:**
   - Tap menu (≡) → **Keychain**
   - Tap **Keys** tab
   - Tap the **+** button
   - Tap **Create key**
   - **Label:** `AWS Vietnam`
   - **Paste** the key content
   - Tap **Save**

---

## 🖥️ Step 3: Add EC2 Host

1. **In Termius app, tap the menu (≡) → Hosts**

2. **Tap the + button**

3. **Configure the host:**

   **Alias:** `AWS Claude Bot (Singapore)`
   
   **Hostname:** `YOUR_ELASTIC_IP_HERE`
   - Replace with the Elastic IP from AWS Console
   - Example: `13.229.45.123`
   
   **Port:** `22`
   
   **Username:** `ubuntu`
   
   **Key:** Select `AWS Vietnam` (the key you imported)
   
   **Group:** Leave blank or create "AWS" group

4. **Tap Save**

---

## 🚀 Step 4: Connect!

1. **In Termius, tap on your host:**
   - `AWS Claude Bot (Singapore)`

2. **First connection prompt:**
   - "The authenticity of host can't be established..."
   - Tap **Connect**
   - Tap **Yes** to add to known hosts

3. **You should see:**
   ```
   Welcome to Ubuntu 24.04 LTS
   ubuntu@ip-xxx-xxx-xxx-xxx:~$
   ```

4. **You're in!** 🎉

---

## 🧪 Step 5: Test Commands

Try these commands to verify everything works:

```bash
# Check system info
uname -a

# Check Node.js
node --version

# Check Python
python3 --version

# Check Claude Code
claude --version

# List files
ls -la

# Check bot status (after deployment)
sudo systemctl status telegram-claude-bot
```

---

## 🔐 Step 6: Add Tailscale Host (Optional - Recommended)

After setting up Tailscale on EC2:

1. **Install Tailscale on Android:**
   - Open Play Store
   - Search "Tailscale"
   - Install Tailscale
   - Login with same account as EC2

2. **Get Tailscale IP from EC2:**
   ```bash
   tailscale ip -4
   # Example output: 100.98.234.56
   ```

3. **In Termius, add new host:**
   
   **Alias:** `AWS Claude Bot (Tailscale)`
   
   **Hostname:** `100.x.x.x` (your Tailscale IP)
   
   **Port:** `22`
   
   **Username:** `ubuntu`
   
   **Key:** `AWS Vietnam`

4. **Save and connect!**

**Benefits of Tailscale:**
- ✅ Works from any WiFi/mobile network
- ✅ No public internet exposure
- ✅ Auto-reconnects when switching networks
- ✅ Secure even on public WiFi

---

## 💡 Termius Tips & Tricks

### 1. Quick Terminal

- **Swipe from left** to open hosts menu
- **Long press** on host to copy IP
- **Double tap** terminal to zoom

### 2. Multiple Sessions

- Tap **+** in top bar to open new tab
- Swipe between tabs
- Keep multiple sessions open

### 3. SSH Snippets

Create shortcuts for common commands:

1. Menu (≡) → **Snippets**
2. Tap **+**
3. Add useful commands:
   ```
   Name: Check Bot Status
   Command: sudo systemctl status telegram-claude-bot
   
   Name: Bot Logs
   Command: sudo journalctl -u telegram-claude-bot -f
   
   Name: Restart Bot
   Command: sudo systemctl restart telegram-claude-bot
   ```

### 4. Port Forwarding

Forward ports from EC2 to your phone:

1. Edit host
2. Tap **Forwarding**
3. Add rule:
   - **Type:** Local
   - **Source:** 8080
   - **Destination:** localhost:8000
   - Now access http://localhost:8080 on phone!

### 5. SFTP File Transfer

1. Connect to host
2. Tap menu (⋮) → **SFTP**
3. Browse files
4. Download/upload files easily

---

## 🐛 Troubleshooting

### Can't connect - "Connection refused"

1. **Check if EC2 instance is running:**
   - Go to AWS Console → EC2 → Instances
   - Status should be "Running"

2. **Verify Elastic IP:**
   - Elastic IPs → Check associated instance
   - Make sure IP matches what you entered in Termius

3. **Check Security Group:**
   - EC2 → Security Groups
   - Should allow SSH (port 22) from your IP

### "Permission denied (publickey)"

1. **Wrong key selected:**
   - Edit host in Termius
   - Verify correct key is selected

2. **Key format issue:**
   - Re-import the .pem file
   - Make sure entire key was copied

### "Host key verification failed"

1. **Host key changed:**
   - Termius → Settings → Known Hosts
   - Remove the old entry for your IP
   - Try connecting again

### Connection timeout from Vietnam

1. **Check internet connection:**
   - Try opening a website
   - Switch between WiFi and mobile data

2. **AWS region issue:**
   - Singapore (ap-southeast-1) should be fast
   - Latency: 50-100ms is normal

3. **Firewall blocking SSH:**
   - Some networks block port 22
   - Solution: Use Tailscale (works on any network!)

---

## 🌐 Using on Different Networks

### On Mobile Data (4G/5G)
- ✅ Works great
- Usually no restrictions
- May use ~50MB/hour for active coding

### On Public WiFi (Coffee shops, airports)
- ⚠️ Some block SSH (port 22)
- **Solution:** Use Tailscale!
- Tailscale works on any network

### On Hotel/Office WiFi
- ⚠️ Often blocks SSH
- **Solution:** Use Tailscale!

---

## 📊 Data Usage Estimates

```
Light usage (chat with bot):        ~10MB/hour
Medium usage (coding via Termius):  ~50MB/hour
Heavy usage (file transfers):       ~200MB/hour
```

**Recommendation:** Use WiFi when possible to save mobile data.

---

## 🔋 Battery Usage

Termius is quite battery-efficient:

- **Background connection:** ~1-2% per hour
- **Active typing:** ~3-5% per hour
- **Tip:** Close unused tabs to save battery

---

## ⌨️ External Keyboard Support

Termius works great with Bluetooth keyboards!

**Useful shortcuts:**
- `Ctrl + C` - Interrupt
- `Ctrl + D` - Exit
- `Ctrl + Z` - Suspend
- `Tab` - Auto-complete
- `Arrow keys` - Navigate
- `Ctrl + R` - Search command history

---

## ✅ Quick Reference Card

```
┌─────────────────────────────────────┐
│  Termius Quick Reference            │
├─────────────────────────────────────┤
│  Connect:       Tap host            │
│  New tab:       Tap +               │
│  Menu:          Swipe from left     │
│  SFTP:          Menu → SFTP         │
│  Snippets:      Menu → Snippets     │
│  Disconnect:    Tap X or Back       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Useful Commands on EC2             │
├─────────────────────────────────────┤
│  Bot status:    systemctl status... │
│  Bot logs:      journalctl -u...    │
│  Restart bot:   systemctl restart...│
│  Update code:   git pull            │
│  System info:   htop                │
└─────────────────────────────────────┘
```

---

## 🎯 Next Steps

Once connected via Termius:
1. Follow [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for full setup
2. Deploy the Telegram bot
3. Start coding from your phone!

---

**Happy mobile coding!** 🚀📱
