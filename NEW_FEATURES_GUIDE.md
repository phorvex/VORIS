# Voris Advanced Features Guide

This guide covers all the advanced features available in Voris AI.

## Table of Contents
1. [Google Maps Integration](#google-maps-integration)
2. [Scheduling & Reminders](#scheduling--reminders)
3. [News Integration](#news-integration)
4. [Email Integration](#email-integration)
5. [Plugin System](#plugin-system)
6. [Configuration](#configuration)

---

## Google Maps Integration

Voris can help you visualize your location and find places using Google Maps.

### View Your Location

Get your current location with coordinates and Google Maps link:

```
where am i
what is my location
show my location on map
```

This will show:
- City and country
- GPS coordinates (latitude/longitude)
- Timezone
- Clickable Google Maps URL

### Search for Places

Find businesses and locations on Google Maps:

```
find starbucks on maps
find pizza near me on maps
search walmart on google maps
locate gas stations in maps
```

Voris generates a Google Maps search URL you can open in your browser.

### Get Directions

Generate navigation links to destinations:

```
directions to Orlando Florida
how do i get to downtown
navigate to the airport
route to 123 Main Street
```

Voris creates a directions URL from your current location to the destination.

---

## Scheduling & Reminders

Voris includes a comprehensive scheduling system for managing reminders, timers, and alarms.

### Setting Reminders

Create reminders using natural language:

```
remind me to call John in 30 minutes
remind me to attend meeting tomorrow at 3pm
set reminder to check email in 2 hours
```

Supported time expressions:
- `in [X] seconds/minutes/hours/days` - Relative time
- `at [time] am/pm` - Specific time today
- `tomorrow at [time]` - Specific time tomorrow
- `tonight` - Tonight at specified time

### Timers

Start countdown timers:

```
set timer for 5 minutes
start timer for 1 hour
timer for 30 seconds
```

### Managing Schedules

View and manage your reminders and timers:

```
list reminders - Show all upcoming reminders
list timers - Show active countdown timers
```

### Technical Details

- Schedules are stored in `~/.voris/schedules.json`
- Background thread checks for due reminders every second
- Timers trigger console notifications when complete
- Future enhancement: System notifications integration

---

## News Integration

Stay informed with integrated news headlines from RSS feeds.

### Getting Headlines

```
news - Get top news headlines
headlines - Same as news
latest news - Get current news stories
tech news - Get technology-specific news
```

### News Sources

Currently integrated sources:
- **BBC News RSS** - Top stories, world news
- **BBC Technology** - Tech industry news
- **BBC Business** - Business and finance news
- **BBC Science** - Science and environment news

### Features

- **No API Key Required** - Uses free RSS feeds
- **Category Filtering** - Get news by category
- **Configurable Limit** - Adjust how many headlines to display
- **Clean Formatting** - Titles, descriptions, and links

### Example Output

```
[You]: tech news
[VORIS]: Fetching technology news...
[VORIS]: Technology headlines from BBC News RSS:
[VORIS]: 1. New AI breakthrough announced by researchers
[VORIS]: 2. Major security flaw discovered in popular app
[VORIS]: 3. Tech giant announces new product lineup
```

---

## Email Integration

Check your email without leaving Voris (IMAP support).

### Setup

First, configure an email account:

**For Gmail:**
1. Enable "Less secure app access" or use App Password
2. Create configuration file at `~/.voris/email_config.json`:

```json
{
  "accounts": [
    {
      "email": "your.email@gmail.com",
      "password": "your-app-password",
      "imap_server": "imap.gmail.com",
      "imap_port": 993,
      "enabled": true
    }
  ]
}
```

**Important:** Use App Passwords for Gmail, not your regular password!

### Using Email Commands

Check for unread emails:
```
check email
any emails?
unread emails
```

View latest emails:
```
latest emails
recent emails
show emails
last emails
```

### Features

- **Multi-Account Support** - Add multiple email accounts
- **Unread Count** - Quick check across all accounts
- **Recent Emails** - See subject lines and senders
- **Secure** - Credentials stored locally
- **IMAP Protocol** - Works with Gmail, Outlook, Yahoo, etc.

### Supported Providers

Any IMAP-enabled email provider:
- **Gmail** - imap.gmail.com:993
- **Outlook/Hotmail** - outlook.office365.com:993
- **Yahoo** - imap.mail.yahoo.com:993
- **Custom** - Your own mail server

---

## Plugin System

Extend Voris with custom functionality using the plugin system.

### What are Plugins?

Plugins are Python modules that add new commands and features to Voris. They're loaded at runtime and have full access to Voris capabilities.

### Creating a Plugin

1. Navigate to the plugins directory:
```bash
cd ~/.voris/plugins/
```

2. Create a new Python file (e.g., `my_plugin.py`):

```python
"""
My Custom Plugin for Voris
"""

PLUGIN_INFO = {
    "name": "My Plugin",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Does something awesome",
    "commands": {
        "hello_world": "Prints a greeting"
    }
}

def hello_world(voris, args):
    """Say hello to the world"""
    name = args.get("name", "World")
    return {
        "success": True,
        "message": f"Hello, {name}! This is a plugin!"
    }
```

3. Plugin will be auto-loaded on next Voris start

### Using Plugins

List loaded plugins:
```
list plugins
```

Execute plugin command:
```
plugin my_plugin hello_world
plugin my_plugin hello_world name=John
```

### Plugin Structure

Every plugin must have:

1. **PLUGIN_INFO dictionary**:
   - `name` - Display name
   - `version` - Version string
   - `author` - Your name
   - `description` - What it does
   - `commands` - Dict of command names and descriptions

2. **Command functions**:
   - Take `voris` and `args` parameters
   - Return dict with `success` and `message`
   - Can access all Voris modules via `voris` object

### Example Plugin Functions

**Access system info:**
```python
def check_system(voris, args):
    sys_info = voris.system.get_system_info()
    return {
        "success": True,
        "message": f"CPU: {sys_info['cpu_percent']}%"
    }
```

**Web search:**
```python
def search(voris, args):
    query = args.get("query", "")
    result = voris.web.search_web(query)
    return result
```

**Custom command:**
```python
def backup_files(voris, args):
    voris.system.execute_command("rsync -av ~/Documents/ ~/Backup/")
    return {
        "success": True,
        "message": "Backup complete"
    }
```

### Plugin Best Practices

- ✅ Return proper success/error dictionaries
- ✅ Document your functions with docstrings
- ✅ Handle errors gracefully
- ✅ Use descriptive command names
- ✅ Keep plugins focused and modular
- ❌ Don't block the main thread
- ❌ Don't modify Voris core files
- ❌ Don't hardcode file paths

### Troubleshooting Plugins

Plugin not loading:
- Check for syntax errors
- Ensure PLUGIN_INFO exists
- Verify file is in `~/.voris/plugins/`

Command not working:
- Check function name matches command name
- Verify function signature (voris, args)
- Return proper dictionary format

---

## Configuration

### Config Files

Voris stores configuration in `~/.voris/`:

```
~/.voris/
├── config.json          # Main configuration
├── memory.json          # Learning and preferences
├── commands.json        # Custom commands
├── schedules.json       # Reminders and timers
├── email_config.json    # Email accounts
└── plugins/             # Plugin directory
    └── example_plugin.py
```

### Main Config (config.json)

```json
{
  "voice_enabled": true,
  "voice_rate": 150,
  "voice_volume": 0.9,
  "wake_word": "voris",
  "always_listening": false,
  "learning_enabled": true,
  "use_voice_output": false
}
```

### Memory (memory.json)

Stores:
- User preferences (name, location, etc.)
- Interaction history
- Learned patterns
- Conversation count

### Advanced Settings

**Voice Settings:**
- `voice_rate`: Speech rate (50-300, default 150)
- `voice_volume`: Volume level (0.0-1.0, default 0.9)
- `wake_word`: Activation word (default "voris")
- `use_voice_output`: Enable TTS (default false)

**Learning:**
- `learning_enabled`: Allow Voris to learn (default true)
- Voris learns your preferences over time
- Remembers your name and patterns

---

## Examples & Use Cases

### Morning Routine
```
news                           # Get headlines
weather                        # Check weather
check email                    # Check inbox
set timer for 30 minutes       # Breakfast timer
remind me to leave in 1 hour   # Commute reminder
```

### Work Session
```
tech news                      # Stay informed
set timer for 25 minutes       # Pomodoro timer
remind me to stretch in 1 hour # Health reminder
battery                        # Check power
```

### Research
```
who is Albert Einstein         # Get information
what is quantum physics        # Learn concepts
search for latest discoveries  # Web search
tell me more                   # Continue reading
```

### System Management
```
status                         # Quick overview
system info                    # Detailed specs
update system                  # Update packages
battery                        # Power status
```

---

## Future Enhancements

Planned features for upcoming versions:

1. **System Notifications**
   - Desktop notifications for reminders
   - Toast notifications for timers
   - Email alerts integration

2. **Smart Home Integration**
   - Control IoT devices
   - Home automation triggers
   - Scene management

3. **Advanced NLP**
   - Machine learning models
   - Sentiment analysis
   - Context retention

4. **Calendar Integration**
   - Google Calendar sync
   - Meeting reminders
   - Event management

5. **Multi-Language Support**
   - Translation capabilities
   - Multiple language interfaces
   - Language learning assistance

6. **Mobile Companion App**
   - Remote Voris control
   - Notifications sync
   - Cloud integration

---

## Troubleshooting

### Common Issues

**Scheduler not triggering:**
- Voris must remain running for reminders
- Background thread needs to be active
- Check `schedules.json` for valid entries

**Email not working:**
- Verify IMAP credentials
- Use App Password for Gmail
- Check firewall/network settings
- Enable IMAP in email provider settings

**Plugins not loading:**
- Check Python syntax
- Verify PLUGIN_INFO exists
- Look for error messages in console
- Ensure plugin file ends in `.py`

**News not updating:**
- Check internet connection
- BBC RSS feeds must be accessible
- Some regions may have blocks

### Getting Help

If you encounter issues:
1. Check console error messages
2. Verify configuration files
3. Review this documentation
4. Check plugin syntax
5. Restart Voris

---

## Contributing

Want to add features? Plugin system makes it easy!

1. Create your plugin
2. Test thoroughly
3. Document your code
4. Share with the community

---

**Happy Voris-ing!** 🚀
