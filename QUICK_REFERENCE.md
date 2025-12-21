# Voris Quick Reference Card

## 🚀 Getting Started

```bash
# Basic mode
python3 voris_advanced.py

# Voice mode
python3 voris_advanced.py --voice

# Run demos
python3 demo_features.py       # Feature showcase
python3 complete_demo.py        # Full interactive demo
```

---

## 📋 Command Quick Reference

### Basic Interaction
| Command | Description |
|---------|-------------|
| `hello`, `hi` | Greet Voris |
| `goodbye`, `exit` | Shutdown |
| `help` | Show help message |
| `my name is [name]` | Tell Voris your name |
| `who are you` | Voris introduction |
| `what can you do` | List capabilities |

### Information & Knowledge
| Command | Description |
|---------|-------------|
| `what time is it` | Current time |
| `what date is it` | Current date |
| `what timezone` | Timezone info |
| `where am i` | Location detection |
| `who is [person]` | Biography/info |
| `what is [topic]` | Explanation |
| `tell me about [topic]` | Detailed info |

### Weather
| Command | Description |
|---------|-------------|
| `weather` | Current local weather |
| `weather in [city]` | Weather for location |
| `weather here` | Uses detected location |

### 🗺️ Google Maps (NEW!)
| Command | Description |
|---------|-------------|
| `show on map` | View location on Maps |
| `find [place] on maps` | Search for place |
| `search [place] on google maps` | Maps search |
| `directions to [place]` | Get directions |
| `navigate to [place]` | Navigation link |

**Examples:**
- `find starbucks on maps`
- `find pizza near me on maps`
- `directions to Orlando Florida`

### Web & Search
| Command | Description |
|---------|-------------|
| `search for [query]` | Web search |
| `look up [topic]` | Find information |
| `tell me more` | Continue previous response |

### System Tasks
| Command | Description |
|---------|-------------|
| `status`, `report` | System status |
| `system info` | Hardware details |
| `battery` | Battery status |
| `update system` | System updates |
| `open [app]` | Launch application |

### ⏰ Scheduling & Reminders (NEW!)
| Command | Description |
|---------|-------------|
| `remind me to [task] in [time]` | Set reminder |
| `remind me to [task] at [time]` | Set timed reminder |
| `set timer for [duration]` | Countdown timer |
| `list reminders` | Show reminders |
| `list timers` | Show active timers |

**Time Examples:**
- `in 5 minutes`
- `in 2 hours`
- `at 3pm`
- `tomorrow at 9am`

### 📰 News & Information (NEW!)
| Command | Description |
|---------|-------------|
| `news`, `headlines` | Top news stories |
| `tech news` | Technology news |
| `latest news` | Current headlines |

### 📧 Email Integration (NEW!)
| Command | Description |
|---------|-------------|
| `check email` | Check unread count |
| `latest emails` | Show recent emails |
| `show emails` | Display inbox |

*Note: Requires configuration in `~/.voris/email_config.json`*

### 🔌 Plugin System (NEW!)
| Command | Description |
|---------|-------------|
| `list plugins` | Show loaded plugins |
| `load plugin [name]` | Load a plugin |
| `plugin [name] [cmd]` | Execute plugin command |

### 🔧 Custom Commands
| Command | Description |
|---------|-------------|
| `when I say [trigger], run [cmd]` | Create command |
| `list commands` | Show custom commands |
| `remove command [trigger]` | Delete command |

### 🧮 Calculations
| Command | Description |
|---------|-------------|
| `what is 25 times 4` | Calculation |
| `calculate [expression]` | Math expression |
| `15 plus 30` | Word operators |

**Supported Operators:**
- Numbers: `+`, `-`, `*`, `/`, `**`, `%`
- Words: `plus`, `minus`, `times`, `divided by`

### 🎙️ Voice Control
| Command | Description |
|---------|-------------|
| `start listening` | Continuous mode |
| `wake word mode` | Use wake word |

---

## 📁 File Locations

```
~/.voris/
├── config.json          # Main settings
├── memory.json          # User preferences
├── commands.json        # Custom commands
├── schedules.json       # Reminders/timers
├── email_config.json    # Email accounts
└── plugins/             # Plugin directory
    └── *.py             # Your plugins
```

---

## 🔧 Configuration

### Voice Settings (config.json)
```json
{
  "voice_rate": 150,        // Speech rate (50-300)
  "voice_volume": 0.9,      // Volume (0.0-1.0)
  "wake_word": "voris",     // Activation word
  "use_voice_output": false // Enable TTS
}
```

### Email Setup (email_config.json)
```json
{
  "accounts": [{
    "email": "you@example.com",
    "password": "app-password",
    "imap_server": "imap.gmail.com",
    "imap_port": 993
  }]
}
```

---

## 🎨 Example Sessions

### Morning Routine
```
> hello
> my name is John
> weather
> news
> check email
> remind me to leave in 30 minutes
```

### Work Session
```
> set timer for 25 minutes
> tech news
> who is Elon Musk
> remind me to stretch in 1 hour
> battery
```

### Research
```
> what is quantum computing
> tell me more
> search for latest AI research
> who is Alan Turing
```

---

## 🔌 Creating a Plugin

**1. Create file:** `~/.voris/plugins/my_plugin.py`

```python
"""My Custom Plugin"""

PLUGIN_INFO = {
    "name": "My Plugin",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Does cool stuff",
    "commands": {
        "hello": "Says hello"
    }
}

def hello(voris, args):
    return {
        "success": True,
        "message": "Hello from my plugin!"
    }
```

**2. Restart Voris** (plugins auto-load)

**3. Use it:**
```
> list plugins
> plugin my_plugin hello
```

---

## 🐛 Troubleshooting

### Voice Issues
```bash
# Test microphone
python3 -m speech_recognition

# Reinstall PyAudio
pip install --upgrade pyaudio
```

### Module Not Found
```bash
# Install dependencies
pip install -r requirements.txt

# Or use system packages
sudo apt install python3-psutil python3-pyttsx3
```

### News Not Loading
- Check internet connection
- Try different category: `tech news`
- BBC RSS may be blocked in some regions

### Email Not Working
- Verify IMAP credentials
- Use App Password for Gmail
- Check `~/.voris/email_config.json` format

---

## 📚 Documentation Files

- **README.md** - Main documentation
- **NEW_FEATURES_GUIDE.md** - New features tutorial
- **ADVANCED_FEATURES.md** - Advanced usage
- **UPDATE_SUMMARY.md** - Change log
- **QUICK_REFERENCE.md** - This file

---

## 💡 Tips & Tricks

### Productivity
- Set multiple reminders for tasks
- Use timers for Pomodoro technique
- Check news while timer runs
- Create custom commands for frequent tasks

### Research
- Ask questions naturally
- Use "tell me more" for detailed answers
- Search web for latest information
- Combine weather + news for daily briefing

### Customization
- Create plugins for specialized tasks
- Set custom commands for workflows
- Adjust voice settings to preference
- Build your own command shortcuts

---

## 🎯 Keyboard Shortcuts

### In Text Mode
- `Ctrl+C` - Exit Voris
- `Ctrl+D` - EOF (same as goodbye)
- Enter empty line - Skip command

### In Voice Mode
- Say wake word ("Voris") + command
- Press `Ctrl+C` to stop listening

---

## 🚀 Next Steps

1. **Try Basic Features**
   - Run `python3 voris_advanced.py`
   - Try: `hello`, `weather`, `news`

2. **Explore Scheduling**
   - `set timer for 5 minutes`
   - `remind me to test in 1 hour`

3. **Create Custom Command**
   - `when I say check disk, run df -h`
   - `list commands`

4. **Build Your First Plugin**
   - Copy example from NEW_FEATURES_GUIDE.md
   - Place in `~/.voris/plugins/`
   - Restart and test

5. **Customize Your Experience**
   - Edit `~/.voris/config.json`
   - Create frequently-used commands
   - Set up email integration

---

**Need More Help?**
- Read NEW_FEATURES_GUIDE.md for tutorials
- Check ADVANCED_FEATURES.md for deep dives
- Review UPDATE_SUMMARY.md for latest changes

**Happy Voris-ing!** 🎉
