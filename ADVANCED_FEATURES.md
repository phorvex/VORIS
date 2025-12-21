# VORIS - Advanced Features Guide

## 🎉 All Features Now Active!

Voris has been enhanced with powerful new capabilities:

## 🌐 Web Integration

### Web Search
```
> search for Python programming
> look up quantum computing
> find information about artificial intelligence
```

### General Knowledge Q&A
```
> who is the current president of the United States
> what is quantum entanglement
> tell me about the Eiffel Tower
> when was the Declaration of Independence signed
```

### Weather Information
```
> weather
> weather in New York
> weather in Tokyo Japan
```

## 📍 Location & Timezone

### Location Detection
```
> where am i
> my location
> what city am i in
```

### Timezone Information
```
> what timezone am i in
> what time zone
> timezone
```

## 🎯 Custom Commands

Create your own voice shortcuts!

### Creating Commands

**Execute System Commands:**
```
> when I say "check updates", run "sudo apt update"
> when I say "list files", run "ls -la"
```

**Open Applications:**
```
> when I say "open browser", open firefox
> when I say "start code", open vscode
```

**Custom Responses:**
```
> when I say "hello world", say "Greetings from Voris"
```

### Managing Commands
```
> list commands          # Show all custom commands
> remove command [name]  # Delete a custom command
```

### Using Custom Commands
Once created, just say the trigger phrase:
```
> check updates
> open browser
> hello world
```

## 🎤 Voice Activation

### Wake Word Mode
Activate continuous listening with wake word:
```
> start listening
> continuous mode
> wake word mode
```

Then use: **"Voris [your command]"**

Example:
```
You: "Voris, what time is it?"
Voris: "The current time is 7:30 PM"

You: "Voris, weather in Miami"
Voris: [provides weather information]
```

### Running Voice Mode
```bash
python3 voris_advanced.py --voice
```

## 💡 Example Conversation

```
> hello
[VORIS]: Hello. How may I assist you?

> my name is Phillippi
[VORIS]: I'll remember that. Hello, Phillippi.

> what's the weather in Miami?
[VORIS]: Analyzing...
[VORIS]: Weather for Miami, Florida, United States:
[VORIS]: Temperature: 78°F (26°C)
[VORIS]: Conditions: Partly cloudy
[VORIS]: Feels like: 82°F
[VORIS]: Humidity: 65%
[VORIS]: Wind: 15 km/h E

> who is the current president
[VORIS]: Processing...
[VORIS]: [Provides current information from web]

> where am i
[VORIS]: Based on your IP address:
[VORIS]: City: [Your City], [Your State]
[VORIS]: Country: [Your Country]
[VORIS]: Timezone: America/New_York

> create a command: when I say "quick update", run "sudo apt update && sudo apt upgrade -y"
[VORIS]: Custom command 'quick update' added successfully.

> list commands
[VORIS]: You have 1 custom commands:
[VORIS]: - 'quick update': Custom command created from...

> quick update
[VORIS]: [Executes the update command]

> start listening
[VORIS]: Activating continuous listening mode with wake word detection.
[VORIS]: Say 'voris' followed by your command.
[Listening for 'voris'...]

# Now you can say: "Voris, what time is it?"
```

## 🔧 Configuration

Voris stores settings in `~/.voris/`:
- `config.json` - System configuration
- `memory.json` - Your name, preferences, conversation history
- `custom_commands.json` - Your custom commands

### Editing Config
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

Change `wake_word` to customize (e.g., "jarvis", "computer", "assistant")

## 📚 All Available Commands

Type `help` in Voris to see the complete command list!

### Categories:
1. **Basic Interaction** - Greetings, farewells, identity
2. **Information & Knowledge** - Q&A, explanations, facts
3. **Weather** - Current conditions, forecasts
4. **Web & Search** - Web searches, Wikipedia lookups
5. **System Tasks** - File operations, app control
6. **Location & Time** - Timezone, location, time/date
7. **Custom Commands** - Create your own shortcuts
8. **Voice Control** - Wake word, continuous listening

## 🚀 Tips & Tricks

### Natural Language
Voris understands variations:
- "what time is it" = "time" = "what's the time"
- "who am I" = "do you know me" = "remember me"
- "search for" = "look up" = "find information about"

### Chaining Information
```
> my name is Alex
> where am i
> what's the weather here
> what timezone am i in
```

### Quick Facts
```
> who is Elon Musk
> what is blockchain
> tell me about Mars
> when was Python created
```

### System Control
```
> status
> system info
> open firefox
> create folder Projects
```

## 🎯 Power User Features

### Complex Custom Commands
Create multi-step commands:
```
> when I say "morning routine", run "firefox https://news.google.com && thunderbird"
```

### Voice Automation
Set up wake word mode for hands-free operation:
```bash
python3 voris_advanced.py --voice
> start listening
```

### Personalization
Voris learns your preferences:
- Remembers your name
- Tracks interaction patterns
- Stores frequently used commands

## ⚡ Quick Reference

| Command | Action |
|---------|--------|
| `hello` | Greet Voris |
| `my name is [name]` | Introduce yourself |
| `who am I` | Check if remembered |
| `weather` | Local weather |
| `weather in [city]` | Weather elsewhere |
| `where am I` | Location info |
| `what timezone` | Timezone info |
| `who is [person]` | Get info about someone |
| `what is [thing]` | Explain something |
| `search for [query]` | Web search |
| `time` | Current time |
| `date` | Current date |
| `status` | System report |
| `open [app]` | Launch application |
| `help` | Full command list |
| `start listening` | Voice activation |
| `list commands` | Custom commands |
| `goodbye` | Exit Voris |

---

**Enjoy your fully enhanced Voris AI! 🎉**

For issues or questions, check the main README.md or examine the module files in `modules/`.
