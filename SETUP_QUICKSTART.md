# VORIS Setup Quick Start

## 🚀 Three Ways to Setup VORIS

### 1. Voice/Text Command (Easiest!)
Just say or type in VORIS:
```
> setup
```

VORIS will automatically:
- Explain what you can configure
- Give you the web interface URL
- Try to open your browser

---

### 2. Run Setup Script
```bash
./setup_voris.sh
```

---

### 3. Manual Start
```bash
source venv/bin/activate
python3 web_setup.py
```
Then open: **http://localhost:5000**

---

## 💡 What You Can Configure

- **📧 Email** - IMAP/SMTP for Gmail, Outlook, etc.
- **🏠 Smart Home** - Roku, lights, thermostats
- **💬 Communication** - Twilio SMS, Slack, Discord
- **💪 Health** - Water goals, exercise tracking
- **💰 Finance** - Budgets, expense tracking, stocks
- **👨‍💻 Developer** - Git, Docker settings
- **📊 Habits** - Daily/weekly habit tracking
- **🎵 Media** - Music preferences, favorites

---

## 🔑 Common Setup Tasks

### Setup Email (Gmail)
1. Go to: https://myaccount.google.com/apppasswords
2. Generate an App Password
3. In VORIS setup, use:
   - Server: `imap.gmail.com`
   - Port: `993`
   - Username: your email
   - Password: the app password (not your regular password!)

### Setup Roku Device
1. Find your Roku IP address:
   - Roku Settings → Network → About
2. In VORIS setup:
   - Click "Discover Devices" or
   - Add manually: Name, Type=roku, IP=192.168.x.x, Port=8060

### Setup Slack Notifications
1. Go to: https://api.slack.com/messaging/webhooks
2. Create a webhook for your workspace/channel
3. Copy the webhook URL
4. Paste in VORIS Communication setup

---

## 🆘 Troubleshooting

**Can't access http://localhost:5000?**
- Check the web server is running: `ps aux | grep web_setup`
- Try http://127.0.0.1:5000 instead
- Restart: `./setup_voris.sh`

**Browser doesn't open automatically?**
- Just open http://localhost:5000 manually
- Works on any modern browser (Chrome, Firefox, Edge, Safari)

**Configuration not saving?**
- Check ~/.voris/ directory exists
- Verify permissions: `ls -la ~/.voris/`
- Look for web_config.json after saving

---

## 📝 After Setup

Once configured, try these commands in VORIS:

```
> check my email
> turn on roku light
> log habit read
> add expense $20 for lunch
> what's my water intake today?
> budget status
> translate hello to spanish
```

---

## 📖 More Help

- Full guide: `WEB_SETUP_GUIDE.md`
- Commands: `COMMAND_REFERENCE.md`
- Features: `EXTENDED_CAPABILITIES_SUMMARY.md`
- Main docs: `README.md`

**Need help? Just ask VORIS:**
```
> help setup
> how do I configure email?
> show me roku commands
```
