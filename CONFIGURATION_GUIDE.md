# VORIS Configuration - Getting Started

## ✅ What's New

VORIS now includes an **interactive web-based setup interface** that makes configuration easy!

No more editing JSON files or command-line configuration. Just open your browser and follow the guided wizard.

---

## 🚀 Quick Start Guide

### Step 1: Start VORIS
```bash
./start.sh
```

### Step 2: Say or Type "setup"
```
> setup
```

### Step 3: Configure in Your Browser
VORIS will open **http://localhost:5000** automatically, showing you a beautiful setup wizard.

---

## 🎯 What Can You Do Now?

Once you type `setup` in VORIS, you can configure:

### 📧 Email Integration
- Add Gmail, Outlook, Yahoo accounts
- Test connections before saving
- Use IMAP for reading, SMTP for sending
- **Tip:** Use App Passwords for Gmail with 2FA

### 🏠 Smart Home Control
- Auto-discover Roku devices on your network
- Register smart lights and thermostats
- Control devices with voice commands
- **Example:** "turn on roku light"

### 💬 Communication
- Send SMS via Twilio
- Post to Slack channels
- Send Discord notifications
- Translate text to multiple languages

### 💪 Health & Wellness
- Set daily water intake goals
- Track exercise with automatic logging
- Enable reminder system for hydration and posture
- **Example:** "log 16 ounces of water"

### 💰 Finance Management
- Create monthly budgets by category
- Track expenses with voice commands
- Monitor stock watchlist
- Get alerts when approaching budget limits
- **Example:** "add expense $45 for groceries"

### 👨‍💻 Developer Tools
- Configure Git username and email
- Set up Docker host connections
- Save code snippets with tags
- **Example:** "git status in this folder"

### 📊 Habit Tracking
- Create daily or weekly habits
- Automatic streak calculation
- View statistics and progress
- **Example:** "log habit read" or "habit stats"

---

## 📖 Three Ways to Access Setup

### Method 1: Voice/Text Command (Easiest)
Just say or type in VORIS:
```
> setup
```

VORIS will:
1. Explain what you can configure
2. Give you the URL (http://localhost:5000)
3. Automatically open your browser

### Method 2: Setup Script
Run from terminal:
```bash
./setup_voris.sh
```

### Method 3: Manual
```bash
source venv/bin/activate
python3 web_setup.py
```
Then open http://localhost:5000 in any browser.

---

## 🎨 The Setup Interface

The web interface includes:

✨ **Modern Design**
- Dark theme with blue/purple accents
- Responsive layout (works on phone too!)
- Smooth animations and transitions

🔍 **Device Discovery**
- Automatically scans your network for Roku devices
- Finds smart lights and thermostats
- Click "Discover Devices" and wait ~30 seconds

🧪 **Live Testing**
- Test email credentials before saving
- Verify device connections
- Test Slack/Discord webhooks
- Instant feedback on what works

📋 **Guided Wizard**
- Progress bar shows completion
- Section-by-section configuration
- Help text for each field
- Review summary before saving

💾 **Automatic Saving**
- Configurations save to `~/.voris/web_config.json`
- Backup your config file anytime
- Import/export settings (coming soon)

---

## 💡 Common Setup Tasks

### Setting Up Gmail
1. Go to: https://myaccount.google.com/apppasswords
2. Generate a new App Password
3. In VORIS setup:
   - IMAP Server: `imap.gmail.com`
   - IMAP Port: `993`
   - Username: your full email address
   - Password: **use the App Password** (not your regular password!)
   - SMTP Server: `smtp.gmail.com`
   - SMTP Port: `587`
4. Click "Test Email Connection"
5. If successful, continue to next section

### Finding Your Roku Device
1. On your Roku:
   - Go to Settings → Network → About
   - Note the IP address (e.g., 192.168.1.100)
2. In VORIS setup:
   - Click "Discover Devices" (may take 30-60 seconds)
   - Or add manually:
     * Name: "Living Room Roku"
     * Type: roku
     * IP: 192.168.1.100
     * Port: 8060
3. Click "Test Device" to verify

### Setting Up Twilio SMS
1. Sign up at: https://www.twilio.com
2. Get your Account SID and Auth Token from console
3. Get a Twilio phone number
4. In VORIS Communication setup:
   - Enter Account SID
   - Enter Auth Token
   - Enter phone number (with country code: +15551234567)
5. Test with: "send sms test message to +1234567890"

---

## 🎯 After Setup - Try These Commands

Once configured, test your new capabilities:

### Email
```
> check my email
> latest emails
> how many unread emails?
```

### Smart Home
```
> turn on roku light
> roku play
> roku pause
> roku home
```

### Health
```
> log 16 ounces of water
> log 30 minutes of exercise
> health summary
> start health reminders
```

### Finance
```
> add expense $20 for lunch
> add expense $45 for groceries
> budget status
> what's my food budget?
> stock price AAPL
```

### Habits
```
> add habit read daily
> log habit read
> habit stats
> show my habits
```

### Developer Tools
```
> git status
> list docker containers
> docker start mycontainer
```

---

## 🐛 Troubleshooting

### "Setup" Command Not Recognized

**Problem:** VORIS says "I didn't quite catch that" when you type setup.

**Solution:**
- Make sure you're running the latest voris_advanced.py
- Try: "configure" instead of "setup"
- Restart VORIS: Ctrl+C then ./start.sh again

### Can't Access http://localhost:5000

**Problem:** Browser shows "Connection refused" or can't reach page.

**Solutions:**
1. Check if server is running:
   ```bash
   ps aux | grep web_setup
   ```
2. Try http://127.0.0.1:5000 instead
3. Restart setup server:
   ```bash
   ./setup_voris.sh
   ```
4. Check firewall isn't blocking port 5000

### Email Test Fails

**Problem:** "Login failed" or "Connection timeout"

**Solutions:**
1. For Gmail with 2FA, you MUST use App Password
2. Check server address is exactly right:
   - Gmail: `imap.gmail.com` (not just `gmail.com`)
3. Verify port numbers:
   - IMAP: 993
   - SMTP: 587
4. Some email providers block IMAP by default - enable in settings

### Device Not Discovered

**Problem:** "Discover Devices" doesn't find your Roku or lights.

**Solutions:**
1. Ensure device is powered on and connected to WiFi
2. Check device is on same network as computer
3. Try manual entry with IP from router
4. Some networks block device discovery (guest networks, VPNs)
5. Wait full 60 seconds for scan to complete

### Configuration Not Saving

**Problem:** Settings disappear after restart.

**Solutions:**
1. Check ~/.voris/ directory exists:
   ```bash
   ls -la ~/.voris/
   ```
2. Verify web_config.json created:
   ```bash
   cat ~/.voris/web_config.json
   ```
3. Check file permissions:
   ```bash
   chmod 644 ~/.voris/web_config.json
   ```
4. Look for error messages in terminal when clicking "Save"

---

## 📚 More Resources

- **Full Setup Guide:** [WEB_SETUP_GUIDE.md](WEB_SETUP_GUIDE.md)
- **Quick Reference:** [SETUP_QUICKSTART.md](SETUP_QUICKSTART.md)
- **Command List:** [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)
- **Extended Features:** [EXTENDED_CAPABILITIES_SUMMARY.md](EXTENDED_CAPABILITIES_SUMMARY.md)
- **Main Documentation:** [README.md](README.md)

---

## 🎉 You're All Set!

Once you've configured VORIS through the web setup:

1. **Stop the setup server** (Ctrl+C in terminal)
2. **Start VORIS normally** (`./start.sh`)
3. **Start using your new features!**

Example session:
```
> setup                          # Configure everything
> check my email                 # Read your inbox
> turn on roku light             # Control smart home
> log habit read                 # Track habits
> add expense $10 for coffee     # Track spending
> log 12 ounces of water         # Health tracking
> budget status                  # Check finances
```

**Welcome to the enhanced VORIS experience!** 🚀

Have questions? Just ask VORIS:
```
> help setup
> how do I use roku commands?
> show me email commands
```
