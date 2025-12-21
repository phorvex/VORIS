"""
Plugin System for Voris
Allows users to create and load custom extension modules
"""

import importlib.util
import inspect
from pathlib import Path
import json

class PluginManager:
    """Manages plugin loading and execution"""
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.plugins_dir = self.config_dir / "plugins"
        self.plugins_dir.mkdir(exist_ok=True)
        
        self.plugins_config = self.config_dir / "plugins.json"
        self.loaded_plugins = {}
        
        # Create example plugin if none exist
        self._create_example_plugin()
    
    def _create_example_plugin(self):
        """Create an example plugin for users to reference"""
        example_file = self.plugins_dir / "example_plugin.py"
        if not example_file.exists():
            example_code = '''"""
Example Voris Plugin
Shows how to create a custom plugin for Voris

A plugin is a Python module with:
1. A PLUGIN_INFO dictionary with metadata
2. One or more functions that will be callable by Voris
3. Each function should return a dictionary with results
"""

PLUGIN_INFO = {
    "name": "Example Plugin",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "An example plugin that demonstrates the plugin system",
    "commands": {
        "example_command": "Demonstrates a basic command",
        "greet": "Greets the user with a custom message"
    }
}

def example_command(voris, args):
    """
    Example command function
    
    Args:
        voris: The Voris instance (access to all Voris functionality)
        args: Dictionary of arguments passed from the user's command
    
    Returns:
        Dictionary with success status and message
    """
    return {
        "success": True,
        "message": "This is an example plugin command! It works!",
        "data": {
            "timestamp": "2024",
            "custom_field": "You can return any data structure"
        }
    }

def greet(voris, args):
    """Custom greeting function"""
    name = args.get("name", "friend")
    style = args.get("style", "casual")
    
    if style == "formal":
        greeting = f"Good day, {name}. How may I assist you?"
    elif style == "casual":
        greeting = f"Hey {name}! What's up?"
    else:
        greeting = f"Hello {name}!"
    
    return {
        "success": True,
        "message": greeting
    }
'''
            with open(example_file, 'w') as f:
                f.write(example_code)
    
    def load_plugin(self, plugin_name):
        """
        Load a plugin by name
        
        Args:
            plugin_name: Name of the plugin file (without .py extension)
        """
        plugin_path = self.plugins_dir / f"{plugin_name}.py"
        
        if not plugin_path.exists():
            return {
                "success": False,
                "error": f"Plugin file not found: {plugin_path}"
            }
        
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Validate plugin has required PLUGIN_INFO
            if not hasattr(module, 'PLUGIN_INFO'):
                return {
                    "success": False,
                    "error": "Plugin missing PLUGIN_INFO dictionary"
                }
            
            plugin_info = module.PLUGIN_INFO
            
            # Get all functions in the module
            functions = {}
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    functions[name] = obj
            
            # Store loaded plugin
            self.loaded_plugins[plugin_name] = {
                "module": module,
                "info": plugin_info,
                "functions": functions,
                "path": str(plugin_path)
            }
            
            return {
                "success": True,
                "message": f"Plugin '{plugin_info.get('name', plugin_name)}' loaded successfully",
                "commands": list(functions.keys())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to load plugin: {str(e)}"
            }
    
    def load_all_plugins(self):
        """Load all plugins from the plugins directory"""
        results = []
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue  # Skip private files
            
            plugin_name = plugin_file.stem
            result = self.load_plugin(plugin_name)
            results.append({
                "plugin": plugin_name,
                "result": result
            })
        
        return {
            "success": True,
            "loaded": len([r for r in results if r["result"]["success"]]),
            "failed": len([r for r in results if not r["result"]["success"]]),
            "results": results
        }
    
    def unload_plugin(self, plugin_name):
        """Unload a plugin"""
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            return {
                "success": True,
                "message": f"Plugin '{plugin_name}' unloaded"
            }
        return {
            "success": False,
            "error": "Plugin not loaded"
        }
    
    def execute_plugin_command(self, plugin_name, command_name, voris, args=None):
        """
        Execute a command from a plugin
        
        Args:
            plugin_name: Name of the plugin
            command_name: Name of the command function
            voris: The Voris instance
            args: Optional arguments dictionary
        """
        if plugin_name not in self.loaded_plugins:
            return {
                "success": False,
                "error": f"Plugin '{plugin_name}' not loaded"
            }
        
        plugin = self.loaded_plugins[plugin_name]
        
        if command_name not in plugin["functions"]:
            return {
                "success": False,
                "error": f"Command '{command_name}' not found in plugin '{plugin_name}'"
            }
        
        try:
            func = plugin["functions"][command_name]
            result = func(voris, args or {})
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Plugin command failed: {str(e)}"
            }
    
    def list_plugins(self):
        """List all loaded plugins"""
        plugins = []
        for name, plugin in self.loaded_plugins.items():
            info = plugin["info"]
            plugins.append({
                "name": name,
                "title": info.get("name", name),
                "version": info.get("version", "unknown"),
                "author": info.get("author", "unknown"),
                "description": info.get("description", ""),
                "commands": list(plugin["functions"].keys())
            })
        return plugins
    
    def get_plugin_help(self, plugin_name):
        """Get help information for a plugin"""
        if plugin_name not in self.loaded_plugins:
            return {
                "success": False,
                "error": "Plugin not loaded"
            }
        
        plugin = self.loaded_plugins[plugin_name]
        info = plugin["info"]
        
        commands_help = {}
        for cmd_name, func in plugin["functions"].items():
            commands_help[cmd_name] = {
                "description": info.get("commands", {}).get(cmd_name, "No description"),
                "docstring": func.__doc__ or "No documentation available"
            }
        
        return {
            "success": True,
            "plugin": info.get("name", plugin_name),
            "version": info.get("version", "unknown"),
            "description": info.get("description", ""),
            "commands": commands_help
        }
