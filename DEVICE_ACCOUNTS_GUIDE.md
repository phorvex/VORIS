# VORIS Device Account Integration Guide

## 🔐 Overview

VORIS now supports integration with major device accounts and platforms, allowing seamless authentication and control across multiple ecosystems.

**Supported Platforms:**
- 🔍 **Google** - Google Assistant, Calendar, Gmail, Drive
- 🗣️ **Amazon Alexa** - Alexa Skills, Smart Home
- 🪟 **Microsoft** - Cortana, OneDrive, Outlook, Office 365
- 🍎 **Apple HomeKit** - Siri, Home app, HomeKit devices
- ⚙️ **IFTTT** - Cross-platform automations
- 💠 **SmartThings** - Samsung smart home platform

---

## 🚀 Quick Start

### Access Account Setup

1. **Start VORIS Setup:**
   ```bash
   ./setup_voris.sh
   ```
   Or in VORIS: `> setup`

2. **Navigate to Accounts Section:**
   - Open http://localhost:5000
   - Click "🔐 Accounts" tab

3. **Connect Your Accounts:**
   - Fill in credentials for each platform
   - Click "Connect" to save
   - Use "Test" button to verify

---

## 📋 Platform-Specific Setup

### 🔍 Google Account

**What You Get:**
- Google Assistant integration
- Gmail access for email commands
- Google Calendar for scheduling
- Drive access for file management

**Setup Steps:**

1. **Get OAuth Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create a new project or select existing
   - Enable APIs:
     * Google Assistant API
     * Gmail API
     * Google Calendar API
     * Google Drive API
   - Create OAuth 2.0 Client ID
   - Download credentials

2. **Configure in VORIS:**
   - **Client ID**: Your OAuth 2.0 client ID
   - **Client Secret**: Your OAuth 2.0 client secret
   - **Refresh Token** (optional): For persistent auth

3. **Commands After Setup:**
   ```
   > send email via gmail
   > check my google calendar
   > save this to google drive
   > hey google, turn on the lights
   ```

**Scopes Needed:**
```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/drive.file
https://www.googleapis.com/auth/assistant-sdk-prototype
```

---

### 🗣️ Amazon Alexa Account

**What You Get:**
- Alexa Skills integration
- Smart home device control
- Voice command forwarding
- Alexa routines

**Setup Steps:**

1. **Create Alexa Skill:**
   - Go to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
   - Create new skill (Custom, Python/Node.js)
   - Note your Skill ID

2. **Get Security Profile:**
   - Go to Security Profiles
   - Create new or use existing
   - Note Client ID and Client Secret
   - Add redirect URI: `http://localhost:5000/auth/alexa/callback`

3. **Configure in VORIS:**
   - **Client ID**: From Security Profile
   - **Client Secret**: From Security Profile
   - **Access Token** (optional): After OAuth flow

4. **Commands After Setup:**
   ```
   > alexa, play music
   > tell alexa to turn off bedroom lights
   > check alexa shopping list
   > create alexa routine
   ```

---

### 🪟 Microsoft Account

**What You Get:**
- Cortana integration
- Outlook email access
- OneDrive file storage
- Office 365 integration

**Setup Steps:**

1. **Register App in Azure:**
   - Go to [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps)
   - Click "New registration"
   - Name: "VORIS Integration"
   - Supported account types: Single tenant or multitenant
   - Redirect URI: `http://localhost:5000/auth/microsoft/callback`

2. **Get Credentials:**
   - Application (client) ID
   - Directory (tenant) ID
   - Create new client secret in "Certificates & secrets"
   - Note the secret VALUE (not ID)

3. **API Permissions:**
   - Add permissions:
     * Microsoft Graph → Mail.Read
     * Microsoft Graph → Calendars.ReadWrite
     * Microsoft Graph → Files.ReadWrite.All
   - Grant admin consent

4. **Configure in VORIS:**
   - **Client ID**: Application (client) ID
   - **Client Secret**: Client secret value
   - **Tenant ID**: Directory (tenant) ID

5. **Commands After Setup:**
   ```
   > check my outlook
   > save to onedrive
   > create teams meeting
   > hey cortana, what's the weather?
   ```

---

### 🍎 Apple HomeKit Account

**What You Get:**
- HomeKit device control
- Siri integration
- Home app synchronization
- Automation triggers

**Setup Steps:**

1. **Find Home ID:**
   - Open Home app on iOS/macOS
   - Go to Home Settings
   - Note your Home ID (under "Home" → "i" icon)

2. **Get Setup Code:**
   - For each HomeKit device:
   - Settings → Accessories
   - Select device → Note setup code

3. **Configure in VORIS:**
   - **Home ID**: From Home app
   - **Setup Code**: 8-digit code from device

4. **Commands After Setup:**
   ```
   > turn on living room lights
   > set thermostat to 72 degrees
   > lock the front door
   > activate good morning scene
   ```

**Note:** HomeKit integration requires iOS device on same network initially.

---

### ⚙️ IFTTT Account

**What You Get:**
- Cross-platform automations
- 700+ service integrations
- Custom webhooks
- Trigger/action chains

**Setup Steps:**

1. **Get Webhook Key:**
   - Go to [IFTTT Webhooks](https://ifttt.com/maker_webhooks)
   - Click "Documentation"
   - Copy your unique webhook key (after `/use/`)

2. **Configure in VORIS:**
   - **Webhook Key**: Your unique key

3. **Create Applets:**
   - Go to [IFTTT Create](https://ifttt.com/create)
   - IF: Webhooks → Receive web request
   - Event name: `voris_command`
   - THEN: Choose action (lights, notifications, etc.)

4. **Commands After Setup:**
   ```
   > trigger ifttt event lights_on
   > activate ifttt applet morning_routine
   > send ifttt notification
   ```

**Example Webhook URL:**
```
https://maker.ifttt.com/trigger/voris_command/with/key/YOUR_KEY
```

---

### 💠 SmartThings Account

**What You Get:**
- Samsung SmartThings hub control
- Device management
- Automation rules
- Scene activation

**Setup Steps:**

1. **Generate Access Token:**
   - Go to [SmartThings Tokens](https://account.smartthings.com/tokens)
   - Click "Generate new token"
   - Name: "VORIS Integration"
   - Scopes:
     * `r:devices:*` (Read devices)
     * `x:devices:*` (Execute devices)
     * `r:scenes:*` (Read scenes)
   - Copy token immediately (shown once only!)

2. **Configure in VORIS:**
   - **Personal Access Token**: Your generated token

3. **Commands After Setup:**
   ```
   > list smartthings devices
   > turn on kitchen lights via smartthings
   > activate movie time scene
   > set smartthings thermostat to 70
   ```

---

## 🔒 Security Best Practices

### Credential Storage
- All credentials encrypted at rest in `~/.voris/accounts/device_accounts.json`
- File permissions set to 600 (owner read/write only)
- Never commit config files to version control

### Access Control
- Use OAuth 2.0 flows when available (Google, Microsoft, Alexa)
- Rotate tokens regularly
- Revoke access when not needed
- Use minimal required scopes

### Network Security
- Setup server runs on localhost only (127.0.0.1)
- Not exposed to internet
- Use HTTPS for OAuth redirects in production

---

## 🧪 Testing Connections

### Test Button
Each platform has a "Test" button that verifies:
- Credentials are valid
- API endpoints are reachable
- Required scopes are granted
- Account is active

### Manual Testing
```bash
# Test Google
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://www.googleapis.com/oauth2/v1/userinfo

# Test Alexa
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.amazonalexa.com/v1/users/~current/profile

# Test Microsoft
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://graph.microsoft.com/v1.0/me

# Test SmartThings
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.smartthings.com/v1/devices
```

---

## 💡 Use Cases

### Smart Home Unified Control
```
> turn on all lights
```
VORIS checks: HomeKit → SmartThings → Alexa → Google Home
Turns on lights across all platforms

### Cross-Platform Notifications
```
> notify me everywhere
```
Sends to: Alexa devices, Google Assistant, Apple devices, IFTTT webhooks

### Calendar Synchronization
```
> add meeting to all calendars
```
Adds to: Google Calendar, Outlook, Apple Calendar

### Voice Assistant Relay
```
> ask google about the weather, then tell alexa
```
Gets info from Google Assistant, forwards to Alexa

---

## 🐛 Troubleshooting

### Google Connection Issues

**Problem:** "Invalid client" error

**Solutions:**
1. Check Client ID is correct (ends in `.apps.googleusercontent.com`)
2. Verify redirect URI matches: `http://localhost:5000/auth/google/callback`
3. Enable required APIs in Google Cloud Console
4. Wait 5 minutes after creating credentials

**Problem:** "Scope not granted"

**Solutions:**
1. Re-authorize with correct scopes
2. Check API is enabled in console
3. Clear browser cookies and retry

### Alexa Connection Issues

**Problem:** "Skill not found"

**Solutions:**
1. Verify Skill is published or in development
2. Check Skill ID is correct
3. Ensure skill is enabled in Alexa app
4. Check skill endpoint is accessible

### Microsoft Connection Issues

**Problem:** "AADSTS error codes"

**Solutions:**
- `AADSTS50020`: Check username/password
- `AADSTS650052`: Add app to access package
- `AADSTS65001`: Check consent permissions
- `AADSTS700016`: Check Client ID format

### HomeKit Connection Issues

**Problem:** "Accessory not found"

**Solutions:**
1. Ensure iOS device on same network
2. Reset HomeKit accessory
3. Re-pair device in Home app
4. Check setup code is 8 digits

### IFTTT Connection Issues

**Problem:** "Invalid webhook key"

**Solutions:**
1. Copy full key from IFTTT documentation page
2. Check for extra spaces
3. Regenerate key if necessary
4. Test with curl first

### SmartThings Connection Issues

**Problem:** "Unauthorized"

**Solutions:**
1. Generate new token with correct scopes
2. Check token hasn't expired
3. Verify account has devices
4. Test token with curl

---

## 📚 API Integration Examples

### Using Google Calendar
```python
from voris_google import GoogleAccount

google = GoogleAccount()
events = google.get_calendar_events(days=7)
google.create_event("Meeting", "2026-01-03 14:00")
```

### Using Alexa Skills
```python
from voris_alexa import AlexaAccount

alexa = AlexaAccount()
alexa.send_directive("TurnOnRequest", {"deviceId": "light123"})
alexa.trigger_routine("Good Morning")
```

### Using SmartThings
```python
from voris_smartthings import SmartThingsAccount

st = SmartThingsAccount()
devices = st.get_devices()
st.control_device("switch123", "on")
st.activate_scene("movie_time")
```

---

## 🎯 Next Steps

After connecting accounts:

1. **Test Basic Commands:**
   ```
   > list my google devices
   > check alexa status
   > show smartthings devices
   ```

2. **Create Cross-Platform Routines:**
   ```
   > create routine: when I say good morning, turn on google lights, start alexa music, and open microsoft outlook
   ```

3. **Set Up Automations:**
   ```
   > when I leave home, tell google and alexa to turn off all devices
   ```

4. **Configure Voice Forwarding:**
   ```
   > forward all voris commands to google assistant
   ```

---

## 🆘 Getting Help

**Web Setup:** http://localhost:5000
**Documentation:** See WEB_SETUP_GUIDE.md
**Support:** Ask VORIS: `> help accounts`

**Platform Documentation:**
- Google: https://developers.google.com/assistant
- Alexa: https://developer.amazon.com/docs/alexa
- Microsoft: https://docs.microsoft.com/graph
- Apple: https://developer.apple.com/homekit
- IFTTT: https://ifttt.com/docs
- SmartThings: https://developer.smartthings.com

---

## ✅ Configuration Checklist

- [ ] Google account connected and tested
- [ ] Alexa account connected and tested
- [ ] Microsoft account connected and tested
- [ ] HomeKit devices paired (if applicable)
- [ ] IFTTT webhook configured (if applicable)
- [ ] SmartThings token generated (if applicable)
- [ ] All test buttons show green checkmarks
- [ ] Basic commands tested for each platform
- [ ] Credentials backed up securely
- [ ] OAuth tokens saved

**Ready to use multi-platform device integration! 🎉**
