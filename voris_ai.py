#!/usr/bin/env python3
"""
VORIS - Voice Operated Responsive Intelligence System
A custom AI assistant combining JARVIS sophistication with Gideon's informative nature
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

class Voris:
    """Main Voris AI class"""
    
    def __init__(self):
        self.name = "Voris"
        self.version = "1.0.0"
        self.active = False
        self.config_dir = Path.home() / ".voris"
        self.config_file = self.config_dir / "config.json"
        self.memory_file = self.config_dir / "memory.json"
        
        # Initialize directories
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        self.memory = self.load_memory()
        
        # Personality traits
        self.personality = {
            "formal": True,
            "helpful": True,
            "sophisticated": True,
            "informative": True,
            "warm": True
        }
        
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
            "learning_enabled": True
        }
    
    def save_config(self):
        """Save Voris configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_memory(self):
        """Load Voris memory (conversation history, preferences)"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "conversations": [],
            "user_preferences": {},
            "learned_commands": {}
        }
    
    def save_memory(self):
        """Save Voris memory"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)
    
    def speak(self, text, priority="normal"):
        """
        Voris speaks to the user
        Priority: low, normal, high, critical
        """
        print(f"[VORIS]: {text}")
        # TODO: Integrate TTS when voice module is implemented
        
    def greeting(self):
        """Generate context-aware greeting"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good evening"
        
        greetings = [
            f"{time_greeting}. Voris online and ready to assist.",
            f"{time_greeting}. All systems operational. How may I be of service?",
            f"{time_greeting}. Voris intelligence system active. Awaiting your command."
        ]
        
        import random
        return random.choice(greetings)
    
    def initialize(self):
        """Initialize Voris systems"""
        self.active = True
        self.speak(self.greeting())
        self.speak("Running system diagnostics...")
        # TODO: Add actual system checks
        self.speak("All systems nominal. Standing by.")
    
    def shutdown(self):
        """Gracefully shutdown Voris"""
        self.speak("Powering down. Until next time.")
        self.save_config()
        self.save_memory()
        self.active = False
    
    def process_command(self, command):
        """Process user command"""
        command = command.lower().strip()
        
        # Basic command processing
        if command in ["exit", "quit", "goodbye", "bye"]:
            self.shutdown()
            return True
        elif command in ["hello", "hi", "hey"]:
            self.speak("Hello. How may I assist you?")
        elif "status" in command or "report" in command:
            self.give_status_report()
        elif "help" in command:
            self.show_help()
        else:
            # TODO: Implement advanced NLP processing
            self.speak(f"Processing: {command}")
            self.speak("Advanced command processing will be implemented in the NLP module.")
        
        return False
    
    def give_status_report(self):
        """Provide system status report (Gideon-style)"""
        self.speak("System Status Report:")
        self.speak(f"- Voris Core: Operational")
        self.speak(f"- Date: {datetime.now().strftime('%B %d, %Y')}")
        self.speak(f"- Time: {datetime.now().strftime('%I:%M %p')}")
        self.speak(f"- Configuration: Loaded")
        self.speak(f"- Memory Systems: Active")
        # TODO: Add more system checks
    
    def show_help(self):
        """Display available commands"""
        help_text = """
Available Commands:
- "status" or "report" - Get system status
- "help" - Show this help message
- "exit" or "goodbye" - Shutdown Voris
        
More commands will be available as modules are implemented.
        """
        self.speak(help_text.strip())
    
    def run(self):
        """Main run loop"""
        self.initialize()
        
        try:
            while self.active:
                user_input = input("\n> ").strip()
                if user_input:
                    should_exit = self.process_command(user_input)
                    if should_exit:
                        break
        except KeyboardInterrupt:
            print()  # New line after ^C
            self.shutdown()
        except Exception as e:
            self.speak(f"Error encountered: {str(e)}")
            self.shutdown()


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   VORIS - Voice Operated Responsive Intelligence      ║
    ║         System v1.0.0                                 ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    voris = Voris()
    voris.run()


if __name__ == "__main__":
    main()
