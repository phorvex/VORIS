"""
Custom Commands Module for Voris
Allows users to create and manage custom voice commands
"""

import json
import re
from pathlib import Path

class CustomCommandsModule:
    """Manages user-defined custom commands"""
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.commands_file = self.config_dir / "custom_commands.json"
        self.commands = self.load_commands()
    
    def load_commands(self):
        """Load custom commands from file"""
        if self.commands_file.exists():
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_commands(self):
        """Save custom commands to file"""
        with open(self.commands_file, 'w') as f:
            json.dump(self.commands, f, indent=4)
    
    def add_command(self, trigger, action, description=""):
        """
        Add a new custom command
        
        Args:
            trigger: The phrase that triggers the command
            action: The action to perform (command to execute or text to speak)
            description: Optional description of what the command does
        """
        command_id = trigger.lower().replace(" ", "_")
        
        self.commands[command_id] = {
            "trigger": trigger.lower(),
            "action": action,
            "description": description,
            "created": str(Path(__file__).stat().st_mtime),
            "use_count": 0
        }
        
        self.save_commands()
        return {
            "success": True,
            "message": f"Custom command '{trigger}' added successfully",
            "command_id": command_id
        }
    
    def remove_command(self, trigger):
        """Remove a custom command"""
        command_id = trigger.lower().replace(" ", "_")
        
        if command_id in self.commands:
            del self.commands[command_id]
            self.save_commands()
            return {
                "success": True,
                "message": f"Custom command '{trigger}' removed"
            }
        else:
            return {
                "success": False,
                "error": f"Command '{trigger}' not found"
            }
    
    def get_command(self, trigger):
        """Get a custom command by trigger"""
        command_id = trigger.lower().replace(" ", "_")
        return self.commands.get(command_id)
    
    def list_commands(self):
        """List all custom commands"""
        return [
            {
                "trigger": cmd["trigger"],
                "description": cmd["description"],
                "use_count": cmd["use_count"]
            }
            for cmd in self.commands.values()
        ]
    
    def match_command(self, text):
        """
        Check if text matches any custom command trigger
        Returns the matching command or None
        """
        text_lower = text.lower()
        
        for command_id, command in self.commands.items():
            trigger = command["trigger"]
            
            # Exact match
            if trigger == text_lower:
                command["use_count"] += 1
                self.save_commands()
                return command
            
            # Contains match (for longer phrases)
            if trigger in text_lower:
                command["use_count"] += 1
                self.save_commands()
                return command
        
        return None
    
    def execute_command(self, command, system_module):
        """
        Execute a custom command
        
        Args:
            command: The command dict to execute
            system_module: Reference to SystemTasksModule for executing system commands
        """
        action = command["action"]
        
        # Check if action is a system command
        if action.startswith("exec:"):
            # Execute system command
            cmd = action[5:].strip()
            result = system_module.execute_command(cmd)
            return {
                "success": result["success"],
                "output": result["output"],
                "error": result.get("error", "")
            }
        
        elif action.startswith("open:"):
            # Open application
            app_name = action[5:].strip()
            result = system_module.open_application(app_name)
            return result
        
        elif action.startswith("say:"):
            # Just speak text
            text = action[4:].strip()
            return {
                "success": True,
                "response": text
            }
        
        else:
            # Default: treat as text to speak
            return {
                "success": True,
                "response": action
            }
    
    def create_command_from_example(self, example_text):
        """
        Create a command from a natural language example
        E.g., "when I say 'check updates', run 'sudo apt update'"
        """
        patterns = [
            r"when i say ['\"](.+?)['\"],?\s+(?:run|execute|do)\s+['\"](.+?)['\"]",
            r"create command ['\"](.+?)['\"],?\s+(?:to|that)\s+(?:runs?|executes?)\s+['\"](.+?)['\"]",
            r"add command ['\"](.+?)['\"],?\s+(?:to|that)\s+(?:opens?)\s+(.+)",
        ]
        
        text_lower = example_text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                trigger = match.group(1)
                action = match.group(2)
                
                # Determine action type
                if "run" in text_lower or "execute" in text_lower:
                    action = f"exec:{action}"
                elif "open" in text_lower:
                    action = f"open:{action}"
                else:
                    action = f"say:{action}"
                
                return self.add_command(trigger, action, f"Custom command created from: {example_text}")
        
        return {
            "success": False,
            "error": "Could not parse command. Try: 'when I say \"[trigger]\", run \"[command]\"'"
        }
