"""
Advanced Voris AI - Enhanced Version with All Modules Integrated
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Import Voris modules
from modules.voice_module import VoiceModule
from modules.nlp_module import NLPModule
from modules.system_tasks import SystemTasksModule
from modules.personality import PersonalityModule
from modules.web_module import WebModule
from modules.custom_commands import CustomCommandsModule
from modules.scheduler import SchedulerModule
from modules.news_module import NewsModule
from modules.email_module import EmailModule
from modules.plugin_system import PluginManager
from modules.ollama_module import OllamaModule

# Import new capability modules
from modules.media_control import MediaController
from modules.automation import AutomationModule
from modules.communication import CommunicationModule
from modules.smart_context import SmartContextModule
from modules.developer_tools import DeveloperToolsModule
from modules.home_automation import HomeAutomationModule
from modules.health_wellness import HealthWellnessModule
from modules.finance import FinanceModule

class VorisAdvanced:
    """Enhanced Voris AI with full module integration"""
    
    def __init__(self, voice_enabled=True):
        self.name = "Voris"
        self.version = "1.0.0"
        self.active = False
        
        # Setup directories
        self.config_dir = Path.home() / ".voris"
        self.config_file = self.config_dir / "config.json"
        self.memory_file = self.config_dir / "memory.json"
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration and memory
        self.config = self.load_config()
        self.memory = self.load_memory()
        
        # Store last response for continuation
        self.last_full_response = None
        self.last_response_source = None
        self.last_location = None
        
        # Initialize modules
        print("Initializing Voris systems...")
        self.personality = PersonalityModule()
        self.voice = VoiceModule(self.config) if voice_enabled else None
        self.nlp = NLPModule()
        self.system = SystemTasksModule()
        self.web = WebModule()
        self.custom_commands = CustomCommandsModule(self.config_dir)
        self.scheduler = SchedulerModule(self.config_dir)
        self.news = NewsModule()
        self.email = EmailModule(self.config_dir)
        self.plugins = PluginManager(self.config_dir)
        
        # Initialize new capability modules
        self.media = MediaController()
        self.automation = AutomationModule()
        self.communication = CommunicationModule()
        self.context = SmartContextModule()
        self.dev_tools = DeveloperToolsModule()
        self.home = HomeAutomationModule()
        self.health = HealthWellnessModule()
        self.finance = FinanceModule()
        
        # Initialize Ollama LLM (optional)
        self.ollama = OllamaModule(self.config)
        if self.ollama.available:
            print(f"Ollama LLM available (model: {self.ollama.model})")
        
        # Auto-load all plugins
        self.plugins.load_all_plugins()
        
        print("All modules loaded.")
    
    def load_config(self):
        """Load Voris configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "voice_enabled": True,
            "voice_rate": 150,
            "voice_volume": 0.9,
            "wake_word": "voris",
            "always_listening": False,
            "learning_enabled": True,
            "use_voice_output": False  # Set to True to enable TTS
        }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_memory(self):
        """Load memory"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                # Sanitize user name on load
                if "user_preferences" in memory and "name" in memory["user_preferences"]:
                    name = memory["user_preferences"]["name"]
                    if not self.is_name_acceptable(name):
                        memory["user_preferences"]["name"] = ""
                        self.save_memory_data(memory)  # Save cleaned version
                return memory
        return {
            "conversations": [],
            "user_preferences": {},
            "learned_commands": {},
            "interaction_count": 0
        }
    
    def save_memory(self):
        """Save memory"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)
    
    def save_memory_data(self, memory_data):
        """Save specific memory data"""
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=4)
    
    def is_name_acceptable(self, name):
        """Check if a name is acceptable (not offensive)"""
        if not name:
            return False
        import re
        # Normalize: lowercase, replace common substitutions, remove non-letters
        normalized = name.lower()
        # First replace multi-char substitutions
        for chars, letter in [('|<', 'k'), ('|{', 'k'), ('ck', 'ck')]:
            normalized = normalized.replace(chars, letter)
        
        # Replace common leetspeak/numeric substitutions
        substitutions = {
            '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's',
            '7': 't', '8': 'b', '9': 'g', '@': 'a', '$': 's',
            '!': 'i', '€': 'e'
        }
        for num, letter in substitutions.items():
            normalized = normalized.replace(num, letter)
        
        # Special case: '4' can also represent 'u' in some contexts (like f4ck -> fuck)
        # Check both interpretations
        normalized_alt = normalized.replace('a', 'u', 1) if 'a' in normalized else normalized
        # Remove all non-letters
        normalized = re.sub(r'[^a-z]', '', normalized)
        
        # Comprehensive list of inappropriate words/patterns
        offensive_patterns = [
            "nigger", "nigga", "nig", "negro",
            "fuck", "fuk", "fck", "fuc",
            "shit", "sht", "shyt",
            "bitch", "btch", "bich",
            "asshole", "ass", "arsehole",
            "cunt", "cnt",
            "dick", "dik", "cock",
            "pussy", "puss",
            "whore", "hore", "slut",
            "fag", "faggot",
            "retard", "retrd"
        ]
        # Check if any offensive pattern is in the normalized name or alternative
        for pattern in offensive_patterns:
            if pattern in normalized or pattern in normalized_alt:
                return False
        return True
    
    def speak(self, text, priority="normal"):
        """Output text (and speak if voice enabled)"""
        # Format with personality
        formatted_text = self.personality.format_response(text)
        print(f"[VORIS]: {formatted_text}")
        
        # TTS if enabled
        if self.voice and self.config.get("use_voice_output", False):
            self.voice.speak(formatted_text)
    
    def listen(self):
        """Listen for voice input"""
        if not self.voice:
            return None
        
        return self.voice.listen()
    
    def initialize(self):
        """Initialize Voris"""
        self.active = True
        
        # Personalized greeting if we know the user
        user_name = self.memory["user_preferences"].get("name")
        if user_name and self.is_name_acceptable(user_name):
            greeting = f"{self.personality.generate_greeting()} Welcome back, {user_name}."
        else:
            if user_name and not self.is_name_acceptable(user_name):
                # Clear offensive name
                self.memory["user_preferences"]["name"] = ""
                self.save_memory()
            greeting = self.personality.generate_greeting()
        
        self.speak(greeting)
        
        # System diagnostics
        self.speak("Running system diagnostics...")
        sys_info = self.system.get_system_info()
        self.speak(f"System: {sys_info['os']} {sys_info['architecture']}")
        self.speak(f"CPU: {sys_info['cpu_count']} cores at {sys_info['cpu_percent']}% utilization")
        self.speak(f"Memory: {sys_info['memory']['available']}GB available")
        self.speak(self.personality.status_report())
        
        # Show help hint
        self.speak("Say 'help' for available commands.")
        self.speak("Say 'setup' to configure devices, email, and other features.")
    
    def shutdown(self):
        """Shutdown Voris"""
        farewell = self.personality.generate_farewell()
        self.speak(farewell)
        self.save_config()
        self.save_memory()
        self.active = False
    
    def process_command(self, command_text):
        """Process a command using NLP"""        # Check for custom commands first
        custom_cmd = self.custom_commands.match_command(command_text)
        if custom_cmd:
            result = self.custom_commands.execute_command(custom_cmd, self.system)
            if result["success"]:
                if "response" in result:
                    self.speak(result["response"])
                if "output" in result and result["output"]:
                    self.speak(result["output"])
                return False
            else:
                self.speak(f"Error executing custom command: {result.get('error', 'Unknown error')}")
                return False
                # Parse command
        parsed = self.nlp.parse_command(command_text)
        intent = parsed["intent"]
        entities = parsed["entities"]
        confidence = parsed["confidence"]
        
        # Log to memory
        self.memory["interaction_count"] += 1
        self.memory["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "input": command_text,
            "intent": intent,
            "confidence": confidence
        })
        
        # Keep only last 100 conversations
        if len(self.memory["conversations"]) > 100:
            self.memory["conversations"] = self.memory["conversations"][-100:]
        
        # Handle intent
        if intent == "farewell":
            self.shutdown()
            return True
        
        elif intent == "greeting":
            response = self.nlp.generate_response(intent)
            self.speak(response)
        
        elif intent == "thank_you":
            response = self.nlp.generate_response(intent)
            self.speak(response)
        
        elif "setup" in command_text.lower() or "configure" in command_text.lower():
            # Setup interface command
            self.speak("Opening the VORIS interactive setup interface.")
            self.speak("The web-based setup wizard allows you to configure:")
            self.speak("Email accounts, smart home devices, communication services,")
            self.speak("health goals, finance budgets, developer tools, and habits.")
            self.speak("")
            self.speak("Access the setup interface at: http://localhost:5000")
            self.speak("Or run: ./setup_voris.sh in a terminal")
            self.speak("")
            
            # Try to open browser automatically
            try:
                import webbrowser
                webbrowser.open("http://localhost:5000")
                self.speak("Opening your web browser now...")
            except Exception as e:
                self.speak("Please open http://localhost:5000 in your browser manually.")
        
        elif intent == "status":
            self.give_status_report()
        
        elif intent == "time":
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
        
        elif intent == "date":
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
        
        elif intent == "system_info":
            self.give_system_info()
        
        elif intent == "open_app":
            app_name = entities.get("app_name")
            if app_name:
                self.speak(self.personality.acknowledge())
                result = self.system.open_application(app_name)
                if result["success"]:
                    self.speak(self.personality.success())
                else:
                    self.speak(f"Unable to open {app_name}. {result.get('message', '')}")
            else:
                self.speak("Which application would you like me to open?")
        
        elif intent == "search":
            query = entities.get("query")
            if query:
                self.speak(f"Searching for: {query}")
                # Implement search logic here
                self.speak("Search functionality is being developed.")
            else:
                self.speak("What would you like me to search for?")
        
        elif intent == "file_operation":
            operation = entities.get("operation")
            if operation == "create":
                op_type = entities.get("type", "file")
                name = entities.get("name")
                if name:
                    if op_type == "directory":
                        result = self.system.create_directory(name)
                        if result["success"]:
                            self.speak(self.personality.success())
                        else:
                            self.speak(f"Error: {result.get('error', 'Unknown error')}")
                    else:
                        self.speak("File creation will be implemented shortly.")
                else:
                    self.speak(f"What should I name the {op_type}?")
        
        elif intent == "identity":
            self.introduce_self()
        
        elif intent == "user_identity":
            # Check if we know the user's preferred name
            user_name = self.memory["user_preferences"].get("name")
            if user_name and self.is_name_acceptable(user_name):
                self.speak(f"You are {user_name}. How may I assist you?")
            else:
                if user_name and not self.is_name_acceptable(user_name):
                    # Clear offensive name
                    self.memory["user_preferences"]["name"] = ""
                    self.save_memory()
                username = os.environ.get('USER') or os.environ.get('USERNAME') or 'User'
                self.speak(f"Your system username is {username}.")
                self.speak("If you'd like, you can tell me your preferred name by saying 'my name is' followed by your name.")
        
        elif intent == "user_name_set":
            user_name = entities.get("name")
            if user_name:
                # Validate the name using centralized validation
                if not self.is_name_acceptable(user_name):
                    self.speak("I cannot accept that name. Please provide a different, respectful name.")
                    self.speak("I'm designed to maintain a professional and respectful interaction.")
                    return
                
                self.memory["user_preferences"]["name"] = user_name
                self.save_memory()
                responses = [
                    f"Understood. I will address you as {user_name}.",
                    f"Pleasure to meet you, {user_name}.",
                    f"Noted. Welcome, {user_name}.",
                    f"I'll remember that. Hello, {user_name}."
                ]
                import random
                self.speak(random.choice(responses))
            else:
                self.speak("I didn't catch your name. Could you repeat that?")
        
        elif intent == "capabilities":
            self.speak("I am Voris, a Voice Operated Responsive Intelligence System.")
            self.speak("I can monitor your system, execute commands, manage files, and assist with various tasks.")
            self.speak("My capabilities include system diagnostics, application control, and natural language interaction.")
            self.speak("Say 'help' for a list of specific commands.")
        
        elif intent == "weather":
            location = entities.get("location")
            
            # If location is "here" or similar, get actual location
            if location and location.lower() in ["here", "my location", "current location"]:
                loc_result = self.web.get_location_info()
                if loc_result["success"]:
                    location = loc_result["city"]
                else:
                    location = None
            
            self.speak(self.personality.thinking())
            result = self.web.get_weather(location)
            if result["success"]:
                self.speak(f"Weather for {result['location']}, {result['region']}, {result['country']}:")
                self.speak(f"Temperature: {result['temperature_f']}°F ({result['temperature_c']}°C)")
                self.speak(f"Conditions: {result['condition']}")
                self.speak(f"Feels like: {result['feels_like_f']}°F")
                self.speak(f"Humidity: {result['humidity']}%")
                self.speak(f"Wind: {result['wind_speed']} km/h {result['wind_dir']}")
            else:
                self.speak(f"Unable to retrieve weather information: {result.get('error', 'Unknown error')}")
        
        elif intent == "location":
            self.speak(self.personality.thinking())
            result = self.web.get_location_info()
            if result["success"]:
                self.speak(f"Based on your IP address:")
                self.speak(f"City: {result['city']}, {result['region']}")
                self.speak(f"Country: {result['country']}")
                self.speak(f"Coordinates: {result['coordinates']}")
                self.speak(f"Timezone: {result['timezone']}")
                self.speak(f"Google Maps: {result['maps_url']}")
                # Store location for map commands
                self.last_location = result
            else:
                self.speak(f"Unable to determine location: {result.get('error', 'Unknown error')}")
        
        elif intent == "timezone":
            tz_info = self.system.get_timezone_info()
            if tz_info["success"]:
                self.speak(f"Your timezone is {tz_info['timezone']}")
                self.speak(f"UTC offset: {tz_info['offset_string']}")
                self.speak(f"Local time: {tz_info['local_time']}")
            else:
                self.speak("Unable to determine timezone information")
        
        elif intent == "web_search":
            query = entities.get("query", command_text.replace("search for", "").replace("look up", "").strip())
            self.speak(f"Searching for: {query}")
            result = self.web.search_web(query)
            if result["success"]:
                if result["answer"]:
                    self.speak(f"Answer: {result['answer']}")
                elif result["abstract"]:
                    self.speak(result["abstract"][:300] + "..." if len(result["abstract"]) > 300 else result["abstract"])
                    if result["abstract_source"]:
                        self.speak(f"Source: {result['abstract_source']}")
                elif result["related_topics"]:
                    self.speak(f"Found {len(result['related_topics'])} results:")
                    for i, topic in enumerate(result["related_topics"][:3], 1):
                        self.speak(f"{i}. {topic['text'][:100]}")
                else:
                    self.speak("No specific results found for that search.")
            else:
                self.speak(f"Search failed: {result.get('error', 'Unknown error')}")
        
        elif intent == "calculation":
            # Check if it's actually a math query
            if self.nlp.is_math_query(command_text):
                result = self.nlp.calculate_math(command_text)
                if result["success"]:
                    self.speak(f"{result['expression']} equals {result['result']}")
                else:
                    self.speak(f"Unable to calculate: {result.get('error', 'Invalid expression')}")
            else:
                # Not actually math, treat as question
                self.speak(self.personality.thinking())
                result = self.web.answer_question(command_text)
                if result["success"]:
                    answer = result["answer"]
                    if len(answer) > 500:
                        answer = answer[:500] + "..."
                    self.speak(answer)
                    if result.get("source"):
                        self.speak(f"Source: {result['source']}")
                else:
                    self.speak("I don't have enough information to answer that question reliably.")
        
        elif intent == "battery":
            result = self.system.get_battery_status()
            if result["success"]:
                self.speak(f"Battery level: {result['percent']}%")
                self.speak(f"Status: {result['status']}")
                if result["time_left"] and not result["power_plugged"]:
                    hours = result["time_left"] // 3600
                    minutes = (result["time_left"] % 3600) // 60
                    if hours > 0:
                        self.speak(f"Time remaining: {hours} hours and {minutes} minutes")
                    else:
                        self.speak(f"Time remaining: {minutes} minutes")
            else:
                self.speak(result.get("error", "Unable to retrieve battery information"))
        
        elif intent == "question":
            self.speak(self.personality.thinking())
            result = self.web.answer_question(command_text)
            if result["success"]:
                answer = result["answer"]
                # Store full answer for continuation
                if len(answer) > 500:
                    self.last_full_response = answer
                    self.last_response_source = result.get("source")
                    answer = answer[:500] + "..."
                    self.speak(answer)
                    self.speak("(Say 'tell me more' to continue)")
                else:
                    self.last_full_response = None
                    self.speak(answer)
                
                if result.get("source"):
                    self.speak(f"Source: {result['source']}")
            else:
                self.speak("I don't have enough information to answer that question reliably.")
        
        elif intent == "custom_command_add":
            # Try to parse and add command
            result = self.custom_commands.create_command_from_example(command_text)
            if result["success"]:
                self.speak(result["message"])
            else:
                self.speak(result.get("error", "Could not create command"))
                self.speak("Try: 'when I say [trigger], run [command]'")
        
        elif intent == "custom_command_list":
            commands = self.custom_commands.list_commands()
            if commands:
                self.speak(f"You have {len(commands)} custom commands:")
                for cmd in commands[:5]:  # Show first 5
                    self.speak(f"- '{cmd['trigger']}': {cmd['description'] or 'No description'}")
            else:
                self.speak("You don't have any custom commands yet.")
                self.speak("Create one by saying: 'when I say [trigger], run [command]'")
        
        elif intent == "system_update":
            self.speak("Initiating system update. This may take several minutes.")
            self.speak("Running package manager update commands...")
            
            # Run update commands based on OS
            if self.system.os_type == "Linux":
                # Try apt (Debian/Ubuntu/Kali)
                result = self.system.execute_command("sudo apt update && sudo apt upgrade -y", shell=True)
                if result["success"]:
                    self.speak("System updated successfully.")
                else:
                    self.speak(f"Update encountered an issue: {result.get('error', 'Unknown error')}")
            else:
                self.speak(f"System update not yet implemented for {self.system.os_type}")
        
        elif intent == "more_info":
            if self.last_full_response:
                # Show the rest of the previously truncated response
                self.speak("Continuing from where I left off:")
                remaining = self.last_full_response[500:]  # Show the part that was truncated
                if len(remaining) > 500:
                    self.speak(remaining[:500] + "...")
                else:
                    self.speak(remaining)
                    if self.last_response_source:
                        self.speak(f"Source: {self.last_response_source}")
                    self.last_full_response = None  # Clear after showing
            else:
                self.speak("There's no previous response to continue from.")
        
        elif intent == "continuous_listen":
            if self.voice:
                self.speak("Activating continuous listening mode with wake word detection.")
                self.speak(f"Say '{self.config.get('wake_word', 'voris')}' followed by your command.")
                self.voice.continuous_listen_mode(self.process_command, wake_word_mode=True)
            else:
                self.speak("Voice recognition is not enabled.")
        
        elif intent == "set_reminder":
            # Extract time and message
            message = command_text
            for p in ["remind me to", "remind me", "reminder to", "set reminder"]:
                message = message.replace(p, "").strip()
            
            # Extract time expression
            time_words = ["in", "at", "tomorrow", "tonight", "today"]
            time_expr = None
            for word in time_words:
                if word in message.lower():
                    idx = message.lower().index(word)
                    time_expr = message[idx:].strip()
                    message = message[:idx].strip()
                    break
            
            if time_expr:
                target_time = self.scheduler.parse_time_expression(time_expr)
                if target_time:
                    result = self.scheduler.add_reminder(message, target_time)
                    if result["success"]:
                        self.speak(result["message"])
                    else:
                        self.speak(f"Failed to set reminder: {result.get('error')}")
                else:
                    self.speak("I couldn't understand the time expression. Try: 'in 5 minutes' or 'at 3pm'")
            else:
                self.speak("When should I remind you? Try: 'remind me to [task] in [time]'")
        
        elif intent == "set_timer":
            # Extract duration
            import re
            match = re.search(r'(\d+)\s*(second|minute|hour)s?', command_text.lower())
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                
                seconds = amount
                if unit == "minute":
                    seconds = amount * 60
                elif unit == "hour":
                    seconds = amount * 3600
                
                result = self.scheduler.add_timer(seconds)
                if result["success"]:
                    self.speak(result["message"])
                else:
                    self.speak(f"Failed to set timer: {result.get('error')}")
            else:
                self.speak("Please specify a duration. Example: 'set timer for 5 minutes'")
        
        elif intent == "list_reminders":
            reminders = self.scheduler.list_reminders()
            if reminders:
                self.speak(f"You have {len(reminders)} upcoming reminders:")
                for reminder in reminders[:5]:
                    self.speak(f"- {reminder['message']} at {reminder['time']}")
            else:
                self.speak("You don't have any active reminders.")
        
        elif intent == "list_timers":
            timers = self.scheduler.list_active_timers()
            if timers:
                self.speak(f"You have {len(timers)} active timers:")
                for timer in timers:
                    self.speak(f"- {timer['label']}: {timer['remaining_formatted']} remaining")
            else:
                self.speak("No active timers.")
        
        elif intent == "news":
            self.speak("Fetching latest news headlines...")
            result = self.news.get_top_headlines(limit=5)
            if result["success"]:
                self.speak(f"Top headlines from {result['source']}:")
                for i, headline in enumerate(result["headlines"], 1):
                    self.speak(f"{i}. {headline['title']}")
            else:
                self.speak(f"Failed to get news: {result.get('error')}")
        
        elif intent == "tech_news":
            self.speak("Fetching technology news...")
            result = self.news.get_tech_news(limit=5)
            if result["success"]:
                self.speak(f"Technology headlines from {result['source']}:")
                for i, headline in enumerate(result["headlines"], 1):
                    self.speak(f"{i}. {headline['title']}")
            else:
                self.speak(f"Failed to get tech news: {result.get('error')}")
        
        elif intent == "check_email":
            result = self.email.get_unread_count()
            if result["success"]:
                if result["total_unread"] > 0:
                    self.speak(f"You have {result['total_unread']} unread emails:")
                    for account in result["accounts"]:
                        if "unread" in account:
                            self.speak(f"  {account['email']}: {account['unread']} unread")
                else:
                    self.speak("You have no unread emails.")
            else:
                self.speak(f"Email check failed: {result.get('error')}")
                self.speak("To set up email, create ~/.voris/email_config.json with your IMAP settings.")
                self.speak("See NEW_FEATURES_GUIDE.md for detailed instructions.")
        
        elif intent == "latest_emails":
            result = self.email.get_latest_emails(count=5)
            if result["success"]:
                self.speak(f"Latest emails in {result['account']}:")
                for i, email_item in enumerate(result["emails"], 1):
                    unread = "🔵 " if email_item["unread"] else ""
                    self.speak(f"{i}. {unread}From: {email_item['from']}")
                    self.speak(f"   Subject: {email_item['subject']}")
            else:
                self.speak(f"Failed to get emails: {result.get('error')}")
                self.speak("To set up email, create ~/.voris/email_config.json with your IMAP settings.")
                self.speak("See NEW_FEATURES_GUIDE.md for detailed instructions.")
        
        elif intent == "list_plugins":
            plugins = self.plugins.list_plugins()
            if plugins:
                self.speak(f"Loaded plugins ({len(plugins)}):")
                for plugin in plugins:
                    self.speak(f"- {plugin['title']} v{plugin['version']}")
                    self.speak(f"  {plugin['description']}")
                    self.speak(f"  Commands: {', '.join(plugin['commands'])}")
            else:
                self.speak("No plugins loaded. Place plugin files in ~/.voris/plugins/")
        
        elif intent == "load_plugin":
            plugin_name = entities.get("plugin_name")
            if plugin_name:
                result = self.plugins.load_plugin(plugin_name)
                if result["success"]:
                    self.speak(result["message"])
                    self.speak(f"Available commands: {', '.join(result['commands'])}")
                else:
                    self.speak(f"Failed to load plugin: {result.get('error')}")
            else:
                self.speak("Which plugin would you like to load?")
        
        elif intent == "plugin_command":
            # Parse plugin command format: "plugin [name] [command] [args]"
            parts = command_text.split()
            if len(parts) >= 3:
                plugin_name = parts[1]
                cmd_name = parts[2]
                args = {"raw_command": " ".join(parts[3:])} if len(parts) > 3 else {}
                
                result = self.plugins.execute_plugin_command(plugin_name, cmd_name, self, args)
                if result["success"]:
                    self.speak(result.get("message", "Plugin command executed"))
                    if "data" in result:
                        self.speak(f"Result: {result['data']}")
                else:
                    self.speak(f"Plugin command failed: {result.get('error')}")
            else:
                self.speak("Use format: 'plugin [name] [command] [args]'")
        
        elif intent == "ip_info":
            # Show IP address information
            self.speak("Retrieving IP information...")
            result = self.web.get_ip_info()
            if result["success"]:
                self.speak(f"Your public IP address: {result['ip']}")
                self.speak(f"Location: {result['city']}, {result['region']}, {result['country']}")
                self.speak(f"Coordinates: {result['latitude']}, {result['longitude']}")
                self.speak(f"Timezone: {result['timezone']}")
                self.speak(f"ISP: {result['isp']}")
                if result['org'] != 'N/A':
                    self.speak(f"Organization: {result['org']}")
            else:
                self.speak(f"Unable to retrieve IP information: {result.get('error')}")
        
        elif intent == "website_status":
            # Check if a website is online
            website = entities.get("website") or entities.get("query")
            if not website:
                # Try to extract from command text
                website = command_text.replace("check website", "").replace("is", "").replace("up", "").replace("down", "").strip()
            
            if website:
                self.speak(f"Checking {website}...")
                result = self.web.check_website_status(website)
                if result["success"]:
                    if result["online"]:
                        self.speak(f"{result['url']} is online!")
                        self.speak(f"Status code: {result['status_code']}")
                        self.speak(f"Response time: {result['response_time_ms']} milliseconds")
                    else:
                        self.speak(f"{result['url']} appears to be down or unreachable.")
                        self.speak(f"Status code: {result['status_code']}")
                else:
                    self.speak(f"Unable to check website: {result.get('error')}")
            else:
                self.speak("Which website would you like me to check?")
        
        elif intent == "crypto_price":
            # Get cryptocurrency price
            crypto = entities.get("crypto") or entities.get("query")
            if not crypto:
                # Try to extract from command text
                for coin in ["bitcoin", "ethereum", "dogecoin", "litecoin", "cardano", "ripple", "btc", "eth", "doge"]:
                    if coin in command_text.lower():
                        crypto = coin
                        break
                if not crypto:
                    crypto = "bitcoin"  # Default
            
            self.speak(f"Fetching {crypto} price...")
            result = self.web.get_cryptocurrency_price(crypto)
            if result["success"]:
                price = result['price_usd']
                change = result['change_24h']
                change_text = f"up {abs(change):.2f}%" if change > 0 else f"down {abs(change):.2f}%"
                
                self.speak(f"{crypto.capitalize()} is currently ${price:,.2f} USD")
                self.speak(f"24-hour change: {change_text}")
                if result['market_cap']:
                    self.speak(f"Market cap: ${result['market_cap']:,.0f}")
            else:
                self.speak(f"Unable to get cryptocurrency price: {result.get('error')}")
        
        elif intent == "currency_convert":
            # Convert currency
            # Try to parse: "convert X USD to EUR" or "100 USD to EUR"
            import re
            match = re.search(r'(\d+\.?\d*)\s*([A-Za-z]{3})\s*to\s*([A-Za-z]{3})', command_text, re.IGNORECASE)
            
            if match:
                amount = float(match.group(1))
                from_curr = match.group(2)
                to_curr = match.group(3)
                
                self.speak(f"Converting {amount} {from_curr} to {to_curr}...")
                result = self.web.convert_currency(amount, from_curr, to_curr)
                if result["success"]:
                    self.speak(f"{result['amount']} {result['from_currency']} = {result['converted_amount']} {result['to_currency']}")
                    self.speak(f"Exchange rate: 1 {result['from_currency']} = {result['rate']:.4f} {result['to_currency']}")
                else:
                    self.speak(f"Currency conversion failed: {result.get('error')}")
            else:
                self.speak("Please use format: 'convert [amount] [from] to [to]' (e.g., 'convert 100 USD to EUR')")
        
        elif intent == "random_fact":
            # Get a random fact
            self.speak("Here's an interesting fact...")
            result = self.web.get_random_fact()
            if result["success"]:
                self.speak(result["fact"])
            else:
                self.speak(f"Unable to retrieve a fact: {result.get('error')}")
        
        elif intent == "joke":
            # Tell a joke
            result = self.web.get_joke()
            if result["success"]:
                self.speak(result["setup"])
                import time
                time.sleep(1)  # Brief pause for comedic effect
                self.speak(result["punchline"])
            else:
                self.speak(f"I couldn't find a joke: {result.get('error')}")
        
        elif intent == "shorten_url":
            # Shorten a URL
            url = entities.get("url") or entities.get("query")
            if not url:
                # Try to extract URL from command
                import re
                url_match = re.search(r'https?://[^\s]+', command_text)
                if url_match:
                    url = url_match.group(0)
            
            if url:
                self.speak("Shortening URL...")
                result = self.web.shorten_url(url)
                if result["success"]:
                    self.speak(f"Short URL: {result['short_url']}")
                else:
                    self.speak(f"Failed to shorten URL: {result.get('error')}")
            else:
                self.speak("Please provide a URL to shorten.")
        
        elif intent == "github_user":
            # Get GitHub user info
            username = entities.get("username") or entities.get("query")
            if not username:
                # Try to extract from command
                username = command_text.replace("github", "").replace("user", "").replace("profile", "").replace("info", "").strip()
            
            if username:
                self.speak(f"Looking up GitHub user: {username}")
                result = self.web.get_github_user(username)
                if result["success"]:
                    self.speak(f"Username: {result['username']}")
                    if result['name'] != 'N/A':
                        self.speak(f"Name: {result['name']}")
                    if result['bio'] != 'No bio':
                        self.speak(f"Bio: {result['bio']}")
                    self.speak(f"Public repositories: {result['public_repos']}")
                    self.speak(f"Followers: {result['followers']} | Following: {result['following']}")
                    if result['location'] != 'N/A':
                        self.speak(f"Location: {result['location']}")
                    if result['company'] != 'N/A':
                        self.speak(f"Company: {result['company']}")
                    self.speak(f"Profile: {result['profile_url']}")
                else:
                    self.speak(f"Unable to find GitHub user: {result.get('error')}")
            else:
                self.speak("Which GitHub user would you like to look up?")
        
        elif intent == "show_on_map":
            # Show current location on Google Maps
            result = self.web.get_location_info()
            if result["success"]:
                self.speak(f"Opening your location on Google Maps:")
                self.speak(f"{result['city']}, {result['region']}, {result['country']}")
                self.speak(f"Coordinates: {result['coordinates']}")
                self.speak(f"Map URL: {result['maps_url']}")
                self.speak("Copy and paste the URL into your browser to view the map.")
            else:
                self.speak(f"Unable to get location: {result.get('error')}")
        
        elif intent == "search_maps":
            # Search for a place on Google Maps
            query = entities.get("query")
            if query:
                result = self.web.search_maps(query)
                if result["success"]:
                    self.speak(result["message"])
                    self.speak(f"Map URL: {result['maps_url']}")
                    self.speak("Copy and paste the URL into your browser.")
                else:
                    self.speak(f"Maps search failed: {result.get('error')}")
            else:
                self.speak("What location would you like to search for?")
        
        elif intent == "get_directions":
            # Get directions between two locations
            destination = entities.get("destination")
            if destination:
                # Get current location as origin
                loc_result = self.web.get_location_info()
                if loc_result["success"]:
                    origin = f"{loc_result['city']}, {loc_result['region']}"
                    result = self.web.get_directions(origin, destination)
                    if result["success"]:
                        self.speak(result["message"])
                        self.speak(f"Directions URL: {result['directions_url']}")
                        self.speak("Copy and paste the URL into your browser.")
                    else:
                        self.speak(f"Failed to get directions: {result.get('error')}")
                else:
                    self.speak("Unable to determine your starting location.")
            else:
                self.speak("Where would you like directions to?")
        
        elif intent == "distance":
            # Calculate or show distance between two locations
            origin = entities.get("origin")
            destination = entities.get("destination")
            
            if not origin:
                # Use current location as origin
                loc_result = self.web.get_location_info()
                if loc_result["success"]:
                    origin = f"{loc_result['city']}, {loc_result['region']}"
                else:
                    self.speak("Unable to determine your current location.")
                    return False
            
            if destination:
                # Generate Google Maps URL with directions for distance calculation
                result = self.web.get_directions(origin, destination)
                if result["success"]:
                    self.speak(f"Calculating distance from {origin} to {destination}...")
                    self.speak("I can provide you with the route URL where you can see the distance.")
                    self.speak(f"Google Maps: {result['directions_url']}")
                    self.speak("Open this URL in your browser to see the exact distance and travel time.")
                else:
                    self.speak(f"Unable to calculate distance: {result.get('error')}")
            else:
                self.speak("I need both a starting point and destination to calculate distance.")
        
        elif intent == "help":
            self.show_help()
        
        # NEW EXTENDED CAPABILITIES
        # Media Control
        elif "volume" in command_text.lower() or "music" in command_text.lower() or "play" in command_text.lower() or "pause" in command_text.lower():
            self.handle_media_command(command_text)
        
        # Automation
        elif "organize downloads" in command_text.lower() or "organize files" in command_text.lower():
            self.handle_automation_command(command_text)
        
        # Communication
        elif "translate" in command_text.lower() or "send notification" in command_text.lower():
            self.handle_communication_command(command_text)
        
        # Smart Context / Productivity
        elif "focus mode" in command_text.lower() or "track habit" in command_text.lower() or "habit stats" in command_text.lower():
            self.handle_context_command(command_text)
        
        # Developer Tools
        elif "git" in command_text.lower() or "docker" in command_text.lower():
            self.handle_dev_tools_command(command_text)
        
        # Home Automation
        elif ("turn on" in command_text.lower() or "turn off" in command_text.lower()) and ("light" in command_text.lower() or "roku" in command_text.lower()):
            self.handle_home_automation_command(command_text)
        elif "roku" in command_text.lower():
            self.handle_home_automation_command(command_text)
        
        # Health & Wellness
        elif "log water" in command_text.lower() or "health summary" in command_text.lower() or "log exercise" in command_text.lower():
            self.handle_health_command(command_text)
        
        # Finance
        elif "add expense" in command_text.lower() or "budget status" in command_text.lower() or "stock price" in command_text.lower():
            self.handle_finance_command(command_text)
        
        elif intent == "unknown":
            # Try Ollama LLM for intelligent response
            if self.ollama.available and self.ollama.should_use_llm(command_text, False):
                self.speak(self.personality.thinking())
                
                # Build context for LLM
                context = {
                    "user_name": self.memory["user_preferences"].get("name"),
                    "system_info": f"{self.system.get_system_info()['os']}"
                }
                
                llm_response = self.ollama.get_response(command_text, context)
                if llm_response:
                    self.speak(llm_response)
                    self.speak("Source: Voris LLM.")
                else:
                    # Ollama failed (timeout or error)
                    self.speak("I apologize, but I'm unable to process that query at the moment.")
                    self.speak("The language model is taking too long to respond.")
            else:
                if confidence < 0.3:
                    confused = self.personality.confused()
                    self.speak(confused)
                else:
                    self.speak(f"I understood '{command_text}' but don't have an action for it yet.")
        
        else:
            self.speak("Command recognized but not yet implemented.")
        
        return False
    
    def give_status_report(self):
        """Provide comprehensive status report"""
        self.speak("System Status Report:")
        
        # Time and date
        now = datetime.now()
        self.speak(f"Date: {now.strftime('%B %d, %Y')}")
        self.speak(f"Time: {now.strftime('%I:%M %p')}")
        
        # System info
        sys_info = self.system.get_system_info()
        self.speak(f"Operating System: {sys_info['os']}")
        self.speak(f"CPU Usage: {sys_info['cpu_percent']}%")
        self.speak(f"Memory Usage: {sys_info['memory']['percent']}%")
        self.speak(f"Disk Usage: {sys_info['disk']['percent']}%")
        
        # Voris stats
        self.speak(f"Interactions this session: {self.memory['interaction_count']}")
        self.speak("All systems nominal.")
    
    def give_system_info(self):
        """Provide detailed system information"""
        self.speak("Gathering system information...")
        sys_info = self.system.get_system_info()
        
        self.speak(f"Operating System: {sys_info['os']} {sys_info['os_version']}")
        self.speak(f"Architecture: {sys_info['architecture']}")
        self.speak(f"Processor: {sys_info['processor']}")
        self.speak(f"CPU Cores: {sys_info['cpu_count']}")
        self.speak(f"CPU Usage: {sys_info['cpu_percent']}%")
        self.speak(f"Total Memory: {sys_info['memory']['total']}GB")
        self.speak(f"Available Memory: {sys_info['memory']['available']}GB")
        self.speak(f"Memory Usage: {sys_info['memory']['percent']}%")
        self.speak(f"Total Disk: {sys_info['disk']['total']}GB")
        self.speak(f"Free Disk: {sys_info['disk']['free']}GB")
        self.speak(f"Disk Usage: {sys_info['disk']['percent']}%")
    
    def introduce_self(self):
        """Introduce Voris"""
        intro = self.personality.format_response(
            "I am Voris - Voice Operated Responsive Intelligence System. "
            "I combine the sophistication of JARVIS with the informative nature of Gideon. "
            "I'm here to assist you with system operations, information retrieval, and task automation. "
            "My purpose is to make your computing experience more efficient and intuitive."
        )
        self.speak(intro)
    
    def show_help(self):
        """Show available commands"""
        help_text = """
Available Commands:

Basic Interaction:
  - hello, hi - Greet Voris
  - goodbye, exit - Shutdown
  - help - Show this message
  - my name is [name] - Tell Voris your name
  - setup, configure - Open interactive web setup interface

Information & Knowledge:
  - what time is it - Current time
  - what date is it - Current date
  - what timezone - Timezone information
  - where am i - Location information
  - status, report - System status
  - system info - Hardware details
  - who is [person] - Answer questions
  - what is [topic] - Explain topics
  - tell me about [topic] - Get information

Weather:
  - weather - Current weather
  - weather in [location] - Weather for location

Web & Search:
  - search for [query] - Web search
  - look up [topic] - Find information

Internet Features:
  - my ip, ip address - Show your public IP information
  - check website [url] - Check if a website is online
  - bitcoin price, crypto price - Get cryptocurrency prices
  - convert [amount] [from] to [to] - Currency conversion (e.g., 100 USD to EUR)
  - tell me a fact - Random interesting fact
  - tell me a joke - Hear a joke
  - shorten [url] - Create a short URL
  - github user [username] - Look up GitHub profile

Google Maps:
  - show on map - View your location on Google Maps
  - find [place] on maps - Search for a location
  - directions to [place] - Get directions from your location
  - how far from [place] to [place] - Calculate distance between locations
  - distance from [origin] to [destination] - Show route and distance

System Tasks:
  - open [app] - Launch application
  - create folder [name] - Create directory
  - list directory - Show files
  - update system - Update system packages
  - battery - Check battery status

Scheduling & Reminders:
  - remind me to [task] in/at [time] - Set reminder
  - set timer for [duration] - Start countdown timer
  - list reminders - Show upcoming reminders
  - list timers - Show active timers

News & Updates:
  - news, headlines - Get latest news
  - tech news - Get technology news

Email (requires configuration):
  - check email - Check for unread emails
  - latest emails - Show recent emails

Plugins:
  - list plugins - Show loaded plugins
  - load plugin [name] - Load a plugin
  - plugin [name] [command] - Execute plugin command

Continuation:
  - tell me more - Continue previous response
  - more information - Show truncated content

Custom Commands:
  - when I say [trigger], run [command] - Create command
  - list commands - Show custom commands
  - remove command [trigger] - Delete command

NEW EXTENDED CAPABILITIES:

Media Control:
  - volume up/down - Adjust system volume
  - volume [0-100] - Set specific volume
  - mute/unmute - Mute audio
  - play [song] on youtube - Play on YouTube
  - play [song] on spotify - Play on Spotify
  - pause/stop music - Pause playback
  - next/previous track - Skip tracks

Automation:
  - organize downloads - Organize files by type
  - take screenshot - Capture screen
  - monitor resources - Check CPU/memory/disk
  - find duplicates in [folder] - Find duplicate files

Communication:
  - translate [text] to [language] - Translate text
  - send notification [message] - Send to configured platforms

Productivity:
  - start focus mode for [N] minutes - Pomodoro timer
  - track habit [name] - Log habit completion
  - habit stats - View habit statistics
  - add habit [name] - Create new habit

Developer Tools:
  - git status - Check repository status
  - git commit message "[msg]" - Commit changes
  - docker ps - List running containers
  - docker start/stop [container] - Manage containers

Home Automation:
  - turn on/off lights - Control smart lights
  - roku play/pause/home - Control Roku device
  - register device [name] [type] - Add smart device

Health & Wellness:
  - log water [amount]ml - Track water intake
  - log exercise [activity] [minutes] - Track exercise
  - health summary - View health stats
  - start health reminders - Enable wellness alerts

Finance:
  - add expense [amount] for [category] - Track spending
  - budget status - Check budget
  - stock price [symbol] - Get stock quote
  - set budget [amount] - Set monthly budget

Voice Control (if voice enabled):
  - start listening - Continuous voice mode
  - wake word mode - Use wake word activation
        """
        self.speak(help_text.strip())
    
    # NEW CAPABILITY HANDLERS
    
    def handle_media_command(self, command_text):
        """Handle media control commands"""
        if "volume" in command_text.lower():
            if "up" in command_text.lower():
                result = self.media.volume_up()
            elif "down" in command_text.lower():
                result = self.media.volume_down()
            elif "mute" in command_text.lower():
                result = self.media.mute()
            else:
                import re
                match = re.search(r'(\d+)', command_text)
                if match:
                    level = int(match.group(1))
                    result = self.media.set_volume(level)
                else:
                    result = {"success": False, "message": "Specify volume level (0-100)"}
            
            if result["success"]:
                self.speak(result["message"])
            else:
                self.speak(result.get("error", "Volume control failed"))
        
        elif "play" in command_text.lower():
            if "youtube" in command_text.lower():
                query = command_text.lower().replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
                result = self.media.play_youtube(query)
                self.speak(result["message"])
            elif "spotify" in command_text.lower():
                query = command_text.lower().replace("play", "").replace("on spotify", "").replace("spotify", "").strip()
                result = self.media.open_spotify(query)
                self.speak(result["message"])
            else:
                result = self.media.play_music()
                self.speak(result["message"])
        
        elif "pause" in command_text.lower() or "stop" in command_text.lower():
            result = self.media.pause_music()
            self.speak(result["message"])
    
    def handle_automation_command(self, command_text):
        """Handle automation commands"""
        if "organize" in command_text.lower():
            self.speak("Organizing your downloads folder...")
            result = self.automation.organize_downloads()
            if result["success"]:
                self.speak(f"Organized {result['total_files']} files")
            else:
                self.speak(result["error"])
        
        elif "screenshot" in command_text.lower():
            result = self.automation.take_screenshot()
            if result["success"]:
                self.speak(f"Screenshot saved")
            else:
                self.speak(f"Screenshot failed")
    
    def handle_communication_command(self, command_text):
        """Handle communication commands"""
        if "translate" in command_text.lower() and "to" in command_text.lower():
            parts = command_text.lower().split("to")
            if len(parts) > 1:
                text_part = parts[0].replace("translate", "").strip()
                lang_part = parts[1].strip().split()[0]
                
                result = self.communication.translate_text(text_part, target_language=lang_part)
                if result["success"]:
                    self.speak(f"Translation: {result['translated']}")
                else:
                    self.speak(f"Translation failed")
    
    def handle_context_command(self, command_text):
        """Handle smart context/productivity commands"""
        if "focus mode" in command_text.lower():
            duration = 25
            import re
            match = re.search(r'(\d+) minutes?', command_text.lower())
            if match:
                duration = int(match.group(1))
            
            result = self.context.start_focus_mode(duration)
            self.speak(result["message"])
        
        elif "track habit" in command_text.lower() or "log habit" in command_text.lower():
            habit_name = command_text.replace("track habit", "").replace("log habit", "").strip()
            result = self.context.log_habit(habit_name)
            if result["success"]:
                self.speak(result["message"])
            else:
                self.speak("Habit not found")
        
        elif "habit stats" in command_text.lower():
            result = self.context.get_habit_stats()
            if result["success"] and result["habits"]:
                self.speak("Your habit statistics:")
                for habit in result["habits"][:3]:  # Top 3
                    self.speak(f"{habit['name']}: {habit['current_streak']} day streak")
            else:
                self.speak("No habits tracked yet")
    
    def handle_dev_tools_command(self, command_text):
        """Handle developer tools commands"""
        if "git status" in command_text.lower():
            result = self.dev_tools.git_status()
            if result["success"]:
                if result["clean"]:
                    self.speak("Working tree is clean")
                else:
                    self.speak(f"Git status: {result['status'][:100]}")
            else:
                self.speak("Git error")
        
        elif "docker ps" in command_text.lower() or "docker list" in command_text.lower():
            result = self.dev_tools.docker_ps()
            if result["success"]:
                self.speak(f"{result['count']} running containers")
            else:
                self.speak("Docker not available")
    
    def handle_home_automation_command(self, command_text):
        """Handle home automation commands"""
        if "turn on" in command_text.lower() or "turn off" in command_text.lower():
            action = "on" if "turn on" in command_text.lower() else "off"
            
            if "light" in command_text.lower():
                device_name = "main_light"
                if "bedroom" in command_text.lower():
                    device_name = "bedroom_light"
                elif "roku" in command_text.lower():
                    device_name = "roku_light"
                
                result = self.home.control_light(device_name, action)
                self.speak(result["message"])
        
        elif "roku" in command_text.lower():
            commands_map = {
                "home": "home",
                "play": "play",
                "pause": "pause",
                "up": "up",
                "down": "down"
            }
            
            for keyword, cmd in commands_map.items():
                if keyword in command_text.lower():
                    result = self.home.roku_command("roku", cmd)
                    self.speak(result.get("message", "Roku command sent"))
                    break
    
    def handle_health_command(self, command_text):
        """Handle health & wellness commands"""
        if "log water" in command_text.lower():
            amount = 250
            import re
            match = re.search(r'(\d+)', command_text)
            if match:
                amount = int(match.group(1))
            
            result = self.health.log_water(amount)
            self.speak(result["message"])
        
        elif "health summary" in command_text.lower():
            result = self.health.get_health_summary()
            self.speak("Health Summary:")
            self.speak(f"Water: {result['water']['today']}")
            self.speak(f"Exercise: {result['exercise']['today_minutes']} minutes today")
        
        elif "log exercise" in command_text.lower():
            import re
            match = re.search(r'log exercise (\w+) (\d+)', command_text.lower())
            if match:
                activity = match.group(1)
                duration = int(match.group(2))
                result = self.health.log_exercise(activity, duration)
                self.speak(result["message"])
    
    def handle_finance_command(self, command_text):
        """Handle finance commands"""
        if "add expense" in command_text.lower() or "spent" in command_text.lower():
            import re
            match = re.search(r'(\d+\.?\d*)', command_text)
            if match:
                amount = float(match.group(1))
                category = "general"
                if "food" in command_text.lower():
                    category = "food"
                
                result = self.finance.add_expense(amount, category)
                self.speak(result["message"])
        
        elif "budget status" in command_text.lower():
            result = self.finance.check_budget_status()
            if isinstance(result, dict):
                self.speak(f"Spent: {result['spent']} of {result['limit']}")
                self.speak(f"Status: {result['status']}")
            else:
                self.speak(result)
        
        elif "stock price" in command_text.lower():
            import re
            match = re.search(r'(?:stock price|price of) (\w+)', command_text.lower())
            if match:
                symbol = match.group(1).upper()
                result = self.finance.get_stock_price(symbol)
                if result["success"]:
                    self.speak(f"{symbol}: {result['price']} ({result['change_percent']})")
                else:
                    self.speak("Stock not found")
    
    def run(self):
        """Main run loop"""
        self.initialize()
        
        try:
            while self.active:
                # Get input (text or voice)
                if self.config.get("voice_enabled", False) and self.voice:
                    user_input = self.listen()
                    if user_input:
                        print(f"[You]: {user_input}")
                    else:
                        continue
                else:
                    user_input = input("\n> ").strip()
                
                if user_input:
                    should_exit = self.process_command(user_input)
                    if should_exit:
                        break
        
        except KeyboardInterrupt:
            print()
            self.shutdown()
        except Exception as e:
            self.speak(f"Critical error: {str(e)}")
            self.shutdown()


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ██╗   ██╗ ██████╗ ██████╗ ██╗███████╗                ║
    ║   ██║   ██║██╔═══██╗██╔══██╗██║██╔════╝                ║
    ║   ██║   ██║██║   ██║██████╔╝██║███████╗                ║
    ║   ╚██╗ ██╔╝██║   ██║██╔══██╗██║╚════██║                ║
    ║    ╚████╔╝ ╚██████╔╝██║  ██║██║███████║                ║
    ║     ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝                ║
    ║                                                          ║
    ║   Voice Operated Responsive Intelligence System         ║
    ║   Version 1.0.0                                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check for voice flag
    voice_enabled = "--voice" in sys.argv or "-v" in sys.argv
    
    if voice_enabled:
        print("Voice mode enabled. Ensure your microphone is connected.")
    else:
        print("Text mode. Use --voice or -v to enable voice commands.")
    
    print()
    
    voris = VorisAdvanced(voice_enabled=voice_enabled)
    voris.run()


if __name__ == "__main__":
    main()
