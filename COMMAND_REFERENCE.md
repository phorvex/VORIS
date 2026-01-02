# VORIS Extended Capabilities - Command Reference

## Media Control Commands

### Volume Control
- `volume up` / `increase volume` - Raise volume by 10%
- `volume down` / `decrease volume` - Lower volume by 10%
- `mute` / `unmute` - Toggle mute
- `set volume to 50` - Set specific volume level (0-100)

### Music & Media
- `play [song name]` - Search and play music
- `play [song] on youtube` - Play on YouTube
- `open spotify` - Launch Spotify
- `pause` / `resume` - Control playback
- `next track` / `previous track` - Skip songs

### Favorites & Playlists
- `add to favorites [song]` - Save to favorites
- `show favorites` - List favorite songs
- `create playlist [name]` - New playlist
- `add [song] to playlist [name]` - Add to playlist

---

## Automation Commands

### File Management
- `organize downloads` - Sort files by type
- `organize [folder]` - Organize specific folder
- `find duplicates in [folder]` - Find duplicate files
- `clean temp files` - Remove temporary files

### System Utilities
- `take screenshot` - Capture screen
- `monitor resources` - Show CPU/Memory/Disk usage
- `create backup of [folder]` - Backup directory
- `check disk space` - Show available space

---

## Communication Commands

### Messaging
- `send slack message [text] to [channel]` - Post to Slack
- `send discord message [text] to [webhook]` - Post to Discord
- `send sms [message] to [number]` - Send SMS via Twilio

### Translation
- `translate [text] to [language]` - Translate text
- `detect language of [text]` - Identify language
- Supported: Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese

---

## Smart Context & Productivity

### Habit Tracking
- `add habit [name] daily` - Create daily habit
- `add habit [name] weekly` - Create weekly habit
- `log habit [name]` - Mark habit complete
- `show habits` - View all habits
- `habit stats` - Show statistics

### Focus & Productivity
- `start focus mode` - Start 25-min Pomodoro
- `start focus mode for [X] minutes` - Custom duration
- `stop focus mode` - End current session
- `show focus history` - View past sessions

### Reminders
- `remind me at [location] to [task]` - Location-based reminder
- `show reminders` - List all reminders
- `delete reminder [name]` - Remove reminder

---

## Developer Tools Commands

### Git Operations
- `git status` - Show repository status
- `git commit [message]` - Commit changes
- `git push` - Push to remote
- `git pull` - Pull latest changes
- `git diff` - Show changes

### Docker Management
- `docker ps` - List containers
- `docker start [container]` - Start container
- `docker stop [container]` - Stop container
- `docker logs [container]` - View logs
- `docker images` - List images

### Code Snippets
- `save snippet [name]` - Save code snippet
- `get snippet [name]` - Retrieve snippet
- `list snippets` - Show all snippets
- `search snippets [tag]` - Search by tag

### Dev Servers
- `start dev server [type] on port [number]` - Start server
- `stop dev server [name]` - Stop server
- `list dev servers` - Show running servers

---

## Home Automation Commands

### Roku Control
- `roku play` - Resume playback
- `roku pause` - Pause playback
- `roku home` - Go to home screen
- `roku up/down/left/right` - Navigate menu
- `roku back` - Go back
- `roku select` - Select item

### Smart Lights
- `turn on [device name]` - Turn on light
- `turn off [device name]` - Turn off light
- `set [device] brightness to [0-100]` - Set brightness
- `brighten [device]` - Increase brightness
- `dim [device]` - Decrease brightness

### Device Management
- `register device [name] [type] [ip]` - Add device
- `list devices` - Show all devices
- `device info [name]` - Show device details

### Routines
- `create routine [name]` - New automation routine
- `execute routine [name]` - Run routine
- `list routines` - Show all routines

---

## Health & Wellness Commands

### Water Tracking
- `log [X]ml water` - Log water intake
- `log water` - Log 250ml (default)
- `water stats` - Show today's intake
- `start water reminders` - Enable hourly reminders

### Exercise Tracking
- `log exercise [type] [duration] [calories]` - Log workout
- `log [X] minutes of [activity]` - Quick log
- `exercise stats` - View exercise history

### Wellness Monitoring
- `start screen time tracking` - Monitor screen use
- `screen time stats` - View usage
- `start posture reminders` - Posture alerts
- `health summary` - Overall wellness report

---

## Finance Commands

### Expense Tracking
- `add expense $[amount] [category]` - Add expense
- `add expense $[amount] [category] [description]` - With note
- `show expenses` - View all expenses
- `show expenses [category]` - Filter by category
- `month total` - Total for current month

### Budget Management
- `set budget [category] $[amount]` - Set category budget
- `set monthly budget $[amount]` - Set overall budget
- `check budget` - Check budget status
- `budget alert` - Get budget warnings

### Stocks & Investments
- `add stock [symbol]` - Add to watchlist
- `stock price [symbol]` - Get current price
- `remove stock [symbol]` - Remove from watchlist
- `show watchlist` - View all stocks

### Currency & Savings
- `convert $[amount] [from] to [to]` - Convert currency
- `set savings goal [name] $[amount]` - Create goal
- `savings progress [name]` - Check goal progress

---

## General Commands

### System
- `help` - Show all commands
- `time` / `what time is it` - Current time
- `date` / `what's the date` - Current date
- `weather` - Local weather
- `open [app]` - Launch application

### Information
- `news` - Latest headlines
- `search [query]` - Web search
- `wikipedia [topic]` - Wikipedia search
- `calculate [expression]` - Math calculation

### Voice Control
- Start with `--voice` flag: `python3 voris_advanced.py --voice`
- Say "VORIS" to wake
- Say "exit" or "quit" to stop

---

## Configuration Files

All data is stored in `~/.voris/` directory:

```
~/.voris/
  ├── media/          # Playlists, favorites
  ├── context/        # Habits, focus sessions
  ├── finance/        # Expenses, budgets, stocks
  ├── dev/            # Code snippets, projects
  ├── home/           # Smart devices, routines
  └── health/         # Water, exercise, wellness
```

---

## Tips & Tricks

1. **Natural Language**: VORIS understands variations
   - "increase volume" = "volume up" = "louder"
   - "what time is it" = "time" = "current time"

2. **Command Chaining**: Some commands can be combined
   - "organize downloads and take screenshot"
   - "check weather and show news"

3. **Abbreviations**: Many commands have shortcuts
   - `docker ps` = `list containers`
   - `git st` = `git status`

4. **Smart Context**: VORIS remembers recent actions
   - "add that to favorites" (refers to last played song)
   - "turn it off" (refers to last controlled device)

5. **Voice Mode**: Best practices
   - Speak clearly and naturally
   - Wait for response before next command
   - Use wake word "VORIS" for better recognition

---

## Troubleshooting

### Common Issues

**"Volume control not available"**
- Install: `sudo apt-get install pulseaudio-utils` or `alsa-utils`

**"Device not found"**
- Register device first: `register device [name] [type] [ip]`
- Check device is on the same network

**"SMS failed"**
- Configure Twilio credentials in environment variables
- Set: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE`

**"API error"**
- Check internet connection
- Some features require API keys
- Rate limits may apply to free APIs

### Getting Help

- Say `help [category]` for specific help
- Check logs in terminal for errors
- Configuration files are in `~/.voris/`
- Test individual modules: `python3 test_new_features.py`

---

**Quick Start:**
```bash
cd /home/phorvex/LLM/VORIS/VORIS
source venv/bin/activate
python3 voris_advanced.py
```

Type `help` for full command list!
