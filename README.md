# VORIS - Voice Operated Responsive Intelligence System

A custom AI assistant that combines the sophistication of JARVIS with the informative nature of Gideon from The Flash.

## Features

### Current Capabilities

**Core Features:**
- ✅ Natural language command processing
- ✅ Text-to-speech (TTS) with customizable voice
- ✅ Speech recognition for voice commands
- ✅ Wake word detection ("Voris") and continuous listening
- ✅ System monitoring and information
- ✅ Battery status checking
- ✅ Task automation (file operations, app launching, system updates)
- ✅ Personalized responses with character traits
- ✅ Memory and learning system (remembers your name and preferences)
- ✅ Context-aware greetings and responses

**Web & Information:**
- ✅ Web searching and information retrieval (DuckDuckGo, Wikipedia)
- ✅ Real-time weather information (any location, no API key needed)
- ✅ General knowledge Q&A (people, places, concepts, history)
- ✅ Location and timezone detection (automatic IP-based detection)
- ✅ Mathematical calculations (supports numbers and word operators)
- ✅ Multi-step response continuation (ask for more information)
- ✅ **News headlines and updates** (BBC RSS feeds - tech, business, science)

**Productivity:**
- ✅ **Scheduling and reminders** (natural language time expressions)
- ✅ **Countdown timers** (seconds, minutes, hours)
- ✅ **Email integration** (IMAP support for Gmail, Outlook, Yahoo, etc.)
- ✅ **Custom command creation** (create your own voice shortcuts)

**Extensibility:**
- ✅ **Plugin system** (load custom Python modules for new functionality)
- ✅ **Auto-loading plugins** (plugins load automatically on startup)
- ✅ **Plugin marketplace ready** (share and install community plugins)
- ✅ **Ollama LLM Integration** (optional local AI for enhanced understanding)

**NEW: AI Enhancement (Optional)**
- 🤖 **Ollama LLM support** - Use local LLMs (Llama, Mistral, etc.) for:
  - Better conversational understanding
  - Intelligent handling of complex questions
  - Natural follow-up and corrections
  - Context-aware responses
  - See [OLLAMA_INTEGRATION.md](OLLAMA_INTEGRATION.md) for setup

### Planned Features
- 🔄 Advanced NLP with machine learning models
- 🔄 Smart home integration (IoT device control)
- 🔄 Desktop notifications for reminders and alerts
- 🔄 Calendar sync (Google Calendar, Outlook)
- 🔄 Multi-language support and translation
- 🔄 Mobile app companion

## Installation

### 1. Clone or Download
```bash
cd /path/to/VORIS
```

### 2. Install Dependencies

**Option A: Quick Start (Recommended)**
```bash
./start.sh
```

**Option B: Manual Installation**

If on Kali Linux or system with externally-managed Python:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or install system packages:
```bash
sudo apt install python3-psutil python3-pyttsx3 python3-speechrecognition python3-pyaudio
```

**Option C: Standard pip**
```bash
pip install -r requirements.txt
# or
pip install --user -r requirements.txt
```

### 3. System-Specific Setup

#### Linux (Ubuntu/Debian)
```bash
# For audio support
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### macOS
```bash
# Install portaudio via Homebrew
brew install portaudio
```

#### Windows
PyAudio installation may require additional steps. You can download pre-built wheels from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

## Usage

### Basic Mode (Text Input)
```bash
python voris_ai.py
```

### With Voice Commands
Voice capabilities are automatically enabled if dependencies are installed.

## Available Commands

### Basic Interaction
- "Hello" / "Hi" - Greet Voris
- "Status" / "Report" - Get system status
- "Help" - Show available commands
- "Exit" / "Goodbye" - Shutdown Voris

### System Information
- "System info" - Get hardware specifications
- "Time" - Current time
- "Date" - Current date

### Task Automation
- "Open [application]" - Launch an application
- "Search for [query]" - Search for files
- "Create folder [name]" - Create a directory
- "List directory" - Show directory contents

### More Coming Soon!
Voris is constantly being improved with new capabilities.

## Configuration

Voris stores configuration in `~/.voris/config.json`. You can customize:

```json
{
    "voice_enabled": true,
    "voice_rate": 150,
    "voice_volume": 0.9,
    "wake_word": "voris",
    "always_listening": false,
    "learning_enabled": true
}
```

## Personality

Voris combines:
- **JARVIS traits**: Sophisticated, helpful, anticipates needs
- **Gideon traits**: Informative, formal, mission-oriented

You can adjust personality traits in the code:
```python
personality = {
    "sophistication": 0.9,
    "formality": 0.8,
    "warmth": 0.6,
    "humor": 0.3,
    "verbosity": 0.7,
    "proactivity": 0.8
}
```

## Project Structure

```
VORIS/
├── voris_ai.py              # Basic entry point
├── voris_advanced.py        # Full-featured version (recommended)
├── start.sh                 # Installation script
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── ADVANCED_FEATURES.md     # Detailed feature guide
├── NEW_FEATURES_GUIDE.md    # Guide for new features (scheduling, news, email, plugins)
└── modules/
    ├── __init__.py
    ├── voice_module.py      # Voice I/O and wake word detection
    ├── nlp_module.py        # Natural language processing
    ├── system_tasks.py      # System operations
    ├── personality.py       # Character traits (JARVIS + Gideon)
    ├── web_module.py        # Web search, weather, location, Q&A
    ├── custom_commands.py   # User-defined commands
    ├── scheduler.py         # Reminders and timers
    ├── news_module.py       # News headlines (RSS feeds)
    ├── email_module.py      # Email checking (IMAP)
    └── plugin_system.py     # Plugin loader

Configuration Files (auto-created in ~/.voris/):
~/.voris/
├── config.json              # Main configuration
├── memory.json              # User preferences and learning
├── commands.json            # Custom commands
├── schedules.json           # Reminders and timers
├── email_config.json        # Email account settings
└── plugins/                 # User plugins directory
    └── example_plugin.py    # Example plugin template
```

## Extending Voris

### Using the Plugin System (Recommended)

The easiest way to extend Voris is with plugins! No need to modify core files.

1. **Create a plugin file** in `~/.voris/plugins/my_plugin.py`:

```python
"""My Custom Plugin"""

PLUGIN_INFO = {
    "name": "My Plugin",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Does something cool",
    "commands": {
        "greet": "Greets the user"
    }
}

def greet(voris, args):
    name = args.get("name", "friend")
    return {
        "success": True,
        "message": f"Hello {name}!"
    }
```

2. **Plugin auto-loads** on Voris startup
3. **Use it**: `plugin my_plugin greet name=John`

See [NEW_FEATURES_GUIDE.md](NEW_FEATURES_GUIDE.md) for detailed plugin documentation.

### Adding Core Commands (Advanced)

For permanent core features, edit `modules/nlp_module.py` to add new intents:

```python
"your_intent": {
    "patterns": ["keyword1", "keyword2"],
    "action": "your_action"
}
```

Then implement the action handler in `voris_advanced.py`.

### Custom Modules

Create new modules in the `modules/` directory:

```python
class YourModule:
    def __init__(self):
        pass
    
    def your_function(self):
        return "result"
```

## Troubleshooting

### Voice Not Working
- Ensure microphone permissions are granted
- Install/reinstall PyAudio: `pip install --upgrade pyaudio`
- Check audio devices: Run `python -m speech_recognition` to test

### Command Not Recognized
- Speak clearly and at normal pace
- Reduce background noise
- Check internet connection (Google Speech Recognition requires it)

### Import Errors
- Run: `pip install -r requirements.txt --upgrade`
- Ensure you're using Python 3.7+

## Contributing

Want to improve Voris? Feel free to:
1. Add new features
2. Improve NLP capabilities
3. Enhance personality responses
4. Fix bugs
5. Optimize performance

## License

This is a personal project. Feel free to modify and customize for your own use!

## Acknowledgments

Inspired by:
- JARVIS from Marvel's Iron Man
- Gideon from The CW's The Flash

Built with love and Python 🐍

---

**Created by**: Voris Development Team
**Version**: 1.0.0
**Status**: Active Development
