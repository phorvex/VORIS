# VORIS Web Setup Guide

## 🚀 Quick Start

The interactive web-based setup interface makes configuring VORIS simple and intuitive.

### Starting the Setup Interface

**Option 1: Using the launcher script (Recommended)**
```bash
./setup_voris.sh
```

**Option 2: Manual start**
```bash
source venv/bin/activate
python3 web_setup.py
```

### Accessing the Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

Or if that doesn't work:
```
http://127.0.0.1:5000
```

---

## 📋 Setup Wizard Sections

The setup wizard guides you through 8 configuration sections:

### 1. 📧 Email Setup
Configure email access for reading and sending emails through VORIS.

**What to Enter:**
- **IMAP Server**: Your email provider's IMAP server (e.g., `imap.gmail.com`)
- **IMAP Port**: Usually `993` for SSL
- **Username**: Your full email address
- **Password**: Your email password or app-specific password
- **SMTP Server**: For sending emails (e.g., `smtp.gmail.com`)
- **SMTP Port**: Usually `587` or `465`

**Gmail Users:**
- Enable "Less secure app access" or use an [App Password](https://support.google.com/accounts/answer/185833)
- IMAP: `imap.gmail.com:993`
- SMTP: `smtp.gmail.com:587`

**Test Button**: Click "Test Email Connection" to verify your credentials

---

### 2. 🏠 Smart Home Devices
Register and configure smart home devices like Roku, lights, and thermostats.

**Adding a Device:**
1. Click "Discover Devices" to scan your network (scans `192.168.x.x` range)
2. Or manually enter:
   - **Device Name**: Friendly name (e.g., "Living Room Roku")
   - **Device Type**: roku, light, thermostat, etc.
   - **IP Address**: Device's local network IP
   - **Port**: Device's port (8060 for Roku, 80 for most lights)

**Finding Device IPs:**
- Check your router's DHCP client list
- Use network scanner apps
- Roku: Settings → Network → About

**Supported Devices:**
- Roku streaming devices and TVs
- Smart lights (Philips Hue, LIFX, etc.)
- Smart thermostats
- Generic smart home devices with HTTP APIs

---

### 3. 💬 Communication Services
Set up SMS, Slack, and Discord integrations.

**Twilio (SMS):**
- Account SID: From [Twilio Console](https://console.twilio.com)
- Auth Token: From Twilio Console
- Phone Number: Your Twilio phone number (with country code, e.g., +15551234567)

**Slack:**
- Webhook URL: Create at [Slack API](https://api.slack.com/messaging/webhooks)
- Example: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`

**Discord:**
- Webhook URL: Server Settings → Integrations → Webhooks → New Webhook
- Example: `https://discord.com/api/webhooks/YOUR_WEBHOOK`

---

### 4. 💪 Health & Wellness
Set personal health goals and reminders.

**Configuration Options:**
- **Daily Water Goal**: Ounces per day (e.g., 64)
- **Daily Exercise Goal**: Minutes per day (e.g., 30)
- **Reminder Interval**: How often to remind you (minutes, e.g., 60)
- **Work Session Length**: Pomodoro-style work sessions (minutes, e.g., 25)
- **Break Length**: Break duration (minutes, e.g., 5)

**Commands After Setup:**
- "log 16 ounces of water"
- "log 30 minutes of exercise"
- "start focus mode"
- "how is my screen time today?"

---

### 5. 💰 Finance
Configure budget tracking and stock watchlist.

**Budget Categories:**
- **Category Name**: food, entertainment, utilities, transportation, etc.
- **Monthly Limit**: Maximum amount to spend per month
- **Alert Threshold**: Get notified at X% of budget (e.g., 80)

**Stock Watchlist:**
- Enter stock symbols separated by commas (e.g., AAPL, GOOGL, TSLA)

**Commands After Setup:**
- "add expense $45 for groceries"
- "what's my food budget status?"
- "check stock prices"

---

### 6. 👨‍💻 Developer Tools
Configure Git and Docker settings for development commands.

**Git Configuration:**
- **Username**: Your Git username for commits
- **Email**: Your Git email
- **Default Branch**: Usually `main` or `master`

**Docker Configuration:**
- **Docker Host**: Usually `unix:///var/run/docker.sock` (local)
- Leave default unless using remote Docker

**Commands After Setup:**
- "git commit these changes"
- "list running containers"
- "create git branch feature-auth"

---

### 7. 📊 Habit Tracking
Create habits you want to track daily or weekly.

**Adding a Habit:**
- **Habit Name**: What you want to track (e.g., "Read", "Meditate", "Exercise")
- **Frequency**: daily or weekly
- **Target Count**: How many times per period (e.g., 1 per day, 3 per week)

**Examples:**
- Name: "Read", Frequency: daily, Target: 1
- Name: "Gym", Frequency: weekly, Target: 3
- Name: "Meditate", Frequency: daily, Target: 2

**Commands After Setup:**
- "log habit read"
- "show my habits"
- "habit stats for this week"

---

### 8. ✅ Summary & Save
Review all your configurations before saving.

- Shows all configured settings
- Click **"Save Configuration"** to persist settings
- Configuration saved to `~/.voris/web_config.json`

---

## 🔧 Device Discovery

The **"Discover Devices"** button scans your local network for common smart home devices:

**What It Scans:**
- IP Range: 192.168.1.1 - 192.168.1.254 (and other common ranges)
- Ports:
  - 8060 (Roku devices)
  - 80 (HTTP-based smart devices)
  - 443 (HTTPS devices)

**Note**: Discovery takes 30-60 seconds. Be patient!

**If Discovery Doesn't Find Your Device:**
1. Check device is powered on and connected to WiFi
2. Find IP address manually from router or device settings
3. Add device manually using "Add Device" form

---

## 🧪 Testing Connections

Each section has **Test** buttons to verify configurations:

**Email Test:**
- Attempts IMAP login with provided credentials
- Shows success/error message
- **Important**: Test before saving!

**Device Test:**
- Sends HTTP request to device
- Verifies device responds
- Shows device status

**Webhook Test:**
- Sends test message to Slack/Discord
- Confirms webhook is working

---

## 💾 Configuration Files

All settings are saved to:
```
~/.voris/web_config.json
```

**Manual Editing:**
You can edit this file directly if needed. Format:
```json
{
  "email": {
    "imap_server": "imap.gmail.com",
    "imap_port": 993,
    "username": "you@gmail.com",
    "password": "your_password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  },
  "devices": [
    {
      "name": "Living Room Roku",
      "type": "roku",
      "ip": "192.168.1.100",
      "port": 8060
    }
  ],
  "habits": [
    {
      "name": "Read",
      "frequency": "daily",
      "target": 1
    }
  ]
}
```

**Backup Your Config:**
```bash
cp ~/.voris/web_config.json ~/.voris/web_config.backup.json
```

---

## 🎯 After Setup

Once configuration is complete:

1. **Stop the web server**: Press `Ctrl+C` in the terminal
2. **Start VORIS**: Run `./start.sh`
3. **Test your configurations**:
   ```
   "check my email"
   "turn on roku light"
   "log habit read"
   "add expense $20 for lunch"
   "what's my water intake today?"
   ```

---

## 🐛 Troubleshooting

### Web Interface Won't Load

**Problem**: Browser shows "Connection refused" or "Can't reach page"

**Solutions:**
1. Check server is running (you should see Flask output in terminal)
2. Try `http://127.0.0.1:5000` instead of `localhost`
3. Check firewall isn't blocking port 5000
4. Make sure no other service is using port 5000

### Email Test Fails

**Problem**: "Login failed" or "Connection timeout"

**Solutions:**
1. **Gmail**: Use App Password, not regular password
2. **2FA**: If you have 2-factor auth, you MUST use app-specific password
3. Check server address is correct (imap.gmail.com, not gmail.com)
4. Verify port (993 for IMAP, 587 for SMTP)
5. Some providers block IMAP by default - enable in settings

### Device Not Discovered

**Problem**: "Discover Devices" doesn't find your Roku/lights

**Solutions:**
1. Make sure device is on same WiFi network as computer
2. Check device is powered on
3. Try manual entry with IP address from router
4. Some networks block device discovery (guest networks, VPNs)
5. Check device documentation for API/control port

### Flask Not Installed Error

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
source venv/bin/activate
pip install flask
```

### Configuration Not Persisting

**Problem**: Settings disappear after restart

**Solutions:**
1. Check `~/.voris/` directory exists
2. Verify web_config.json was created: `ls -la ~/.voris/`
3. Check file permissions: `chmod 644 ~/.voris/web_config.json`
4. Look for errors in terminal when clicking "Save Configuration"

---

## 🔒 Security Notes

**Important Security Considerations:**

1. **Passwords in Config**:
   - Your passwords are stored in plain text in web_config.json
   - Keep this file secure: `chmod 600 ~/.voris/web_config.json`
   - Never commit this file to git

2. **Local Network Only**:
   - This setup server should only run on localhost
   - Don't expose it to the internet
   - Don't change binding from 127.0.0.1 to 0.0.0.0

3. **API Keys**:
   - Treat Twilio, Slack, Discord tokens as passwords
   - Don't share your web_config.json file

4. **Email Security**:
   - Use app-specific passwords when possible
   - Don't use your main email password
   - Consider creating a dedicated email for VORIS

---

## 📱 Mobile Access (Optional)

To access setup from phone on same network:

1. Find computer's local IP:
   ```bash
   hostname -I
   ```

2. Edit `web_setup.py` line 554:
   ```python
   # Change from:
   app.run(debug=True, host='127.0.0.1', port=5000)
   
   # To:
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. Access from phone: `http://YOUR_COMPUTER_IP:5000`

**⚠️ Warning**: Only do this on trusted private networks!

---

## 🎉 You're All Set!

The web setup interface makes VORIS configuration easy. Configure once, then enjoy voice-controlled smart home, email, habits, budgets, and more!

Need help? Check the main README.md or command references in COMMAND_REFERENCE.md.

**Happy configuring! 🚀**
