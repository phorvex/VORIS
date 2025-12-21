"""
Natural Language Processing Module for Voris
Handles command parsing, intent recognition, and response generation
"""

import re
from datetime import datetime
import json

class NLPModule:
    """Natural language processing for understanding user commands"""
    
    def __init__(self):
        self.intents = self.load_intents()
        self.context = {}
        
    def load_intents(self):
        """Define command intents and patterns"""
        return {
            "greeting": {
                "patterns": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
                "responses": [
                    "Hello. How may I assist you?",
                    "Greetings. Standing by for your command.",
                    "Hello. What can I do for you today?"
                ]
            },
            "farewell": {
                "patterns": ["goodbye", "bye", "exit", "quit", "see you", "farewell"],
                "responses": [
                    "Goodbye. Powering down.",
                    "Until next time.",
                    "Farewell. Systems shutting down."
                ]
            },
            "status": {
                "patterns": ["status", "report", "system status", "how are you", "diagnostics"],
                "action": "status_report"
            },
            "time": {
                "patterns": ["time", "what time", "current time", "clock"],
                "action": "get_time"
            },
            "date": {
                "patterns": ["date", "what date", "today", "what day"],
                "action": "get_date"
            },
            "weather": {
                "patterns": ["weather", "temperature", "forecast"],
                "action": "get_weather"
            },
            "open_app": {
                "patterns": ["open", "launch", "start", "run"],
                "action": "open_application"
            },
            "close_app": {
                "patterns": ["close", "quit", "kill", "stop"],
                "action": "close_application"
            },
            "search": {
                "patterns": ["search", "find", "look for", "locate"],
                "action": "search"
            },
            "file_operation": {
                "patterns": ["create file", "create folder", "delete", "move", "copy", "rename"],
                "action": "file_operation"
            },
            "system_info": {
                "patterns": ["system info", "hardware", "specs", "cpu", "memory", "ram", "disk"],
                "action": "system_info"
            },
            "help": {
                "patterns": ["help", "what can you do", "capabilities", "commands"],
                "action": "help"
            },
            "thank_you": {
                "patterns": ["thank", "thanks", "appreciate"],
                "responses": [
                    "You're welcome.",
                    "Happy to assist.",
                    "Always at your service."
                ]
            },
            "identity": {
                "patterns": ["who are you", "what is your name", "what are you", "your name", "introduce yourself",
                           "what's your name", "whats your name", "tell me your name"],
                "action": "identity"
            },
            "user_identity": {
                "patterns": ["who am i", "who i am", "do you know me", "remember me"],
                "action": "user_identity"
            },
            "user_name_set": {
                "patterns": ["my name is", "call me", "i am", "i'm", "name's"],
                "action": "user_name_set"
            },
            "capabilities": {
                "patterns": ["what can you do", "your abilities", "your functions", "what do you know"],
                "action": "capabilities"
            },
            "web_search": {
                "patterns": ["search for", "look up", "find information about", "google", "search the web"],
                "action": "web_search"
            },
            "question": {
                "patterns": ["who is", "what is", "when is", "where is", "why is", "how is", "who was", "what was",
                           "how do", "how does", "is the", "are the", "was the", "were the",
                           "current president", "tell me about", "explain", "can you tell"],
                "action": "question"
            },
            "calculation": {
                "patterns": ["calculate", "what is", "compute", "solve", "math", "+", "-", "*", "/", "="],
                "action": "calculation"
            },
            "battery": {
                "patterns": ["battery", "battery level", "battery status", "how much battery", "charge"],
                "action": "battery"
            },
            "location": {
                "patterns": ["where am i", "my location", "current location", "what city", "what country", 
                           "geographic location", "gps location", "where i am", "what is my location", "locate me"],
                "action": "location"
            },
            "timezone": {
                "patterns": ["timezone", "time zone", "what timezone", "what time zone"],
                "action": "timezone"
            },
            "custom_command_add": {
                "patterns": ["create command", "add command", "when i say", "teach you", "learn this command"],
                "action": "custom_command_add"
            },
            "custom_command_list": {
                "patterns": ["list commands", "show commands", "my commands", "custom commands"],
                "action": "custom_command_list"
            },
            "custom_command_remove": {
                "patterns": ["remove command", "delete command", "forget command"],
                "action": "custom_command_remove"
            },
            "continuous_listen": {
                "patterns": ["start listening", "continuous mode", "always listen", "wake word mode", "voice activation"],
                "action": "continuous_listen"
            },
            "system_update": {
                "patterns": ["update system", "upgrade system", "system update", "update my system", "upgrade my system"],
                "action": "system_update"
            },
            "more_info": {
                "patterns": ["tell me more", "more information", "continue", "keep going", "more", "display more", "show more"],
                "action": "more_info"
            },
            "set_reminder": {
                "patterns": ["remind me", "set reminder", "create reminder", "reminder to", "don't forget"],
                "action": "set_reminder"
            },
            "set_timer": {
                "patterns": ["set timer", "start timer", "timer for", "countdown"],
                "action": "set_timer"
            },
            "list_reminders": {
                "patterns": ["list reminders", "show reminders", "my reminders", "upcoming reminders"],
                "action": "list_reminders"
            },
            "list_timers": {
                "patterns": ["list timers", "show timers", "active timers", "my timers"],
                "action": "list_timers"
            },
            "news": {
                "patterns": ["news", "headlines", "latest news", "what's happening", "news update"],
                "action": "news"
            },
            "tech_news": {
                "patterns": ["tech news", "technology news", "tech headlines"],
                "action": "tech_news"
            },
            "check_email": {
                "patterns": ["check email", "read email", "any emails", "unread emails", "email check",
                           "check my email", "read my email", "any new emails", "new email", "email"],
                "action": "check_email"
            },
            "latest_emails": {
                "patterns": ["latest emails", "recent emails", "show emails", "last emails",
                           "show my emails", "my emails", "recent messages", "latest messages"],
                "action": "latest_emails"
            },
            "list_plugins": {
                "patterns": ["list plugins", "show plugins", "available plugins", "loaded plugins"],
                "action": "list_plugins"
            },
            "load_plugin": {
                "patterns": ["load plugin", "enable plugin", "activate plugin"],
                "action": "load_plugin"
            },
            "plugin_command": {
                "patterns": ["plugin", "run plugin", "execute plugin"],
                "action": "plugin_command"
            },
            "show_on_map": {
                "patterns": ["show on map", "open in maps", "view on google maps", "show in google maps", "map my location"],
                "action": "show_on_map"
            },
            "ip_info": {
                "patterns": ["my ip", "ip address", "what is my ip", "show my ip", "check ip", "ip information", "ip details"],
                "action": "ip_info"
            },
            "website_status": {
                "patterns": ["check website", "is website up", "website status", "check if", "website down", ".com up", ".org up", ".net up"],
                "action": "website_status"
            },
            "crypto_price": {
                "patterns": ["bitcoin price", "ethereum price", "crypto price", "cryptocurrency", "btc price", "eth price", "dogecoin", "price of"],
                "action": "crypto_price"
            },
            "currency_convert": {
                "patterns": ["convert currency", "currency conversion", "exchange rate", "convert to", "usd to", "eur to"],
                "action": "currency_convert"
            },
            "random_fact": {
                "patterns": ["random fact", "tell me a fact", "interesting fact", "fun fact", "give me a fact"],
                "action": "random_fact"
            },
            "joke": {
                "patterns": ["tell me a joke", "tell joke", "make me laugh", "say something funny", "joke"],
                "action": "joke"
            },
            "shorten_url": {
                "patterns": ["shorten url", "short link", "tiny url", "shorten this", "make short"],
                "action": "shorten_url"
            },
            "github_user": {
                "patterns": ["github user", "github profile", "github info", "look up github"],
                "action": "github_user"
            },
            "search_maps": {
                "patterns": ["on maps", "on google maps", "in maps", "search maps", "maps search"],
                "action": "search_maps"
            },
            "get_directions": {
                "patterns": ["directions to", "how do i get to", "navigate to", "route to"],
                "action": "get_directions"
            },
            "distance": {
                "patterns": ["how far", "distance from", "distance to", "how many miles", "calculate distance"],
                "action": "distance"
            }
        }
    
    def parse_command(self, text):
        """Parse user command and extract intent and entities"""
        text = text.lower().strip()
        
        # Match intent
        intent = self.match_intent(text)
        
        # Extract entities (parameters)
        entities = self.extract_entities(text, intent)
        
        return {
            "text": text,
            "intent": intent,
            "entities": entities,
            "confidence": self.calculate_confidence(text, intent)
        }
    
    def match_intent(self, text):
        """Match text to an intent using word boundaries and priority"""
        import re
        
        # Priority order for intent matching to avoid conflicts
        priority_intents = [
            "calculation",  # Check math first
            "user_name_set",  # Check name setting
            "identity",  # Check self-identity before questions
            "user_identity",  # Check user identity
            "weather",  # Check weather queries
            "location",  # Check location queries
            "timezone",  # Check timezone
            "distance",  # Check distance queries
            "website_status",  # Website checks before generic search
            "crypto_price",  # Crypto prices before generic search
            "currency_convert",  # Currency conversion before generic search
            "github_user",  # GitHub lookups before generic search
            "shorten_url",  # URL shortening before generic search
            "search_maps",  # Maps search before generic search
            "get_directions",  # Directions before generic search
            "question",  # Questions should be checked before generic patterns
            "web_search",  # Web searches
        ]
        
        # First, check priority intents
        for intent_name in priority_intents:
            if intent_name in self.intents:
                intent_data = self.intents[intent_name]
                patterns = intent_data.get("patterns", [])
                for pattern in patterns:
                    # Special handling for calculation - verify it's actually math
                    if intent_name == "calculation" and pattern in ["what is", "what's"]:
                        if pattern in text and self.is_math_query(text):
                            return intent_name
                        continue
                    
                    if ' ' in pattern:
                        # Multi-word pattern
                        if pattern in text:
                            return intent_name
                    else:
                        # Single word with boundaries
                        if re.search(r'\b' + re.escape(pattern) + r'\b', text):
                            return intent_name
        
        # Then check remaining intents
        for intent_name, intent_data in self.intents.items():
            if intent_name in priority_intents:
                continue  # Already checked
            
            patterns = intent_data.get("patterns", [])
            for pattern in patterns:
                if ' ' in pattern:
                    # Multi-word pattern
                    if pattern in text:
                        return intent_name
                else:
                    # Single word with boundaries
                    if re.search(r'\b' + re.escape(pattern) + r'\b', text):
                        return intent_name
        
        return "unknown"
    
    def extract_entities(self, text, intent):
        """Extract relevant entities from text based on intent"""
        entities = {}
        
        if intent == "open_app":
            # Extract application name
            app_match = re.search(r'(?:open|launch|start|run)\s+(.+)', text)
            if app_match:
                entities["app_name"] = app_match.group(1).strip()
        
        elif intent == "search":
            # Extract search query
            search_match = re.search(r'(?:search|find|look for|locate)\s+(?:for\s+)?(.+)', text)
            if search_match:
                entities["query"] = search_match.group(1).strip()
        
        elif intent == "weather":
            # Extract location if specified
            location_match = re.search(r'weather\s+(?:in|at|for|of)?\s*(.+)', text)
            if location_match:
                location = location_match.group(1).strip()
                # Remove common filler words and time references
                location = re.sub(r'^(in|at|for|of)\s+', '', location)
                # Remove time-related words anywhere in the string
                location = re.sub(r'\s*(tonight|today|tomorrow|this\s+week|this\s+weekend)\s*', ' ', location, flags=re.IGNORECASE)
                location = location.strip()
                # Remove trailing question marks
                location = location.rstrip('?')
                entities["location"] = location
        
        elif intent == "user_name_set":
            # Extract user's name
            name_patterns = [
                r'my name is\s+([a-z]+)',
                r'call me\s+([a-z]+)',
                r'i am\s+([a-z]+)',
                r"i'm\s+([a-z]+)",
                r"name's\s+([a-z]+)"
            ]
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities["name"] = match.group(1).capitalize()
                    break
        
        elif intent == "file_operation":
            # Extract file operation details
            if "create" in text:
                entities["operation"] = "create"
                if "folder" in text or "directory" in text:
                    entities["type"] = "directory"
                else:
                    entities["type"] = "file"
                # Extract name
                name_match = re.search(r'(?:create|make)\s+(?:folder|directory|file)\s+(?:called|named)?\s*(.+)', text)
                if name_match:
                    entities["name"] = name_match.group(1).strip()
        
        elif intent == "search_maps":
            # Extract location/place to search on maps
            maps_match = re.search(r'(?:find|search|locate)\s+(.+?)\s+(?:on|in)\s+(?:google\s+)?maps?', text)
            if maps_match:
                entities["query"] = maps_match.group(1).strip()
            else:
                # Fallback: get everything after the command
                maps_match = re.search(r'(?:maps search|search maps)\s+(.+)', text)
                if maps_match:
                    entities["query"] = maps_match.group(1).strip()
        
        elif intent == "get_directions":
            # Extract destination
            dest_match = re.search(r'(?:directions to|navigate to|route to|how do i get to)\s+(.+)', text)
            if dest_match:
                entities["destination"] = dest_match.group(1).strip()
        
        elif intent == "distance":
            # Extract origin and destination from "how far from X to Y" or "distance from X to Y"
            from_to_match = re.search(r'(?:how far|distance|how many miles)\s+from\s+(.+?)\s+to\s+(.+)', text, re.IGNORECASE)
            if from_to_match:
                entities["origin"] = from_to_match.group(1).strip()
                entities["destination"] = from_to_match.group(2).strip()
            else:
                # "how far to X", "how many miles to X", "distance to X" - use current location as origin
                to_match = re.search(r'(?:how far|distance|how many miles)\s+(?:to|is it to)\s+(.+)', text, re.IGNORECASE)
                if to_match:
                    entities["destination"] = to_match.group(1).strip()
        
        elif intent == "website_status":
            # Extract website URL
            # Look for domain patterns
            url_match = re.search(r'(?:check|is|status)\s+(?:website\s+)?(?:if\s+)?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})', text)
            if url_match:
                entities["website"] = url_match.group(1).strip()
            else:
                # Try to find any URL-like pattern
                url_match = re.search(r'([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})', text)
                if url_match:
                    entities["website"] = url_match.group(1).strip()
        
        elif intent == "crypto_price":
            # Extract cryptocurrency name
            crypto_match = re.search(r'(bitcoin|ethereum|dogecoin|litecoin|cardano|ripple|btc|eth|doge|ltc|ada|xrp)', text, re.IGNORECASE)
            if crypto_match:
                entities["crypto"] = crypto_match.group(1).lower()
        
        elif intent == "github_user":
            # Extract GitHub username
            user_match = re.search(r'github\s+(?:user|profile|info)?\s*([a-zA-Z0-9\-]+)', text)
            if user_match:
                entities["username"] = user_match.group(1).strip()
        
        elif intent == "shorten_url":
            # Extract URL to shorten
            url_match = re.search(r'(https?://[^\s]+)', text)
            if url_match:
                entities["url"] = url_match.group(1).strip()
        
        return entities
    
    def calculate_confidence(self, text, intent):
        """Calculate confidence score for intent matching"""
        if intent == "unknown":
            return 0.0
        
        patterns = self.intents[intent].get("patterns", [])
        max_score = 0.0
        
        for pattern in patterns:
            if pattern == text:
                return 1.0
            elif pattern in text:
                # Calculate based on pattern length vs text length
                score = len(pattern) / len(text)
                max_score = max(max_score, score)
        
        return max_score
    
    def generate_response(self, intent, entities=None):
        """Generate appropriate response based on intent"""
        intent_data = self.intents.get(intent, {})
        responses = intent_data.get("responses", [])
        
        if responses:
            import random
            return random.choice(responses)
        
        action = intent_data.get("action")
        if action:
            return {"action": action, "entities": entities}
        
        return "I'm not sure how to help with that. Could you rephrase?"
    
    def analyze_sentiment(self, text):
        """Basic sentiment analysis"""
        positive_words = ["good", "great", "excellent", "wonderful", "amazing", "love", "perfect", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "hate", "horrible", "poor", "worst"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def is_math_query(self, text):
        """Check if text contains mathematical expression"""
        # Check for numbers and operators (including word forms)
        import re
        
        # Check for numeric operators
        math_pattern = r'\d+\s*[+\-*/x×÷]\s*\d+'
        if re.search(math_pattern, text):
            return True
        
        # Check for word-form operators
        word_operators = ['plus', 'minus', 'times', 'divided by', 'multiplied by', 'multiply', 'divide', 'add', 'subtract']
        text_lower = text.lower()
        
        # Check if there are numbers and word operators
        has_numbers = bool(re.search(r'\d+', text))
        has_word_operator = any(op in text_lower for op in word_operators)
        
        return has_numbers and has_word_operator
    
    def extract_time_references(self, text):
        """Extract time-related information from text"""
        time_refs = {
            "absolute": None,
            "relative": None
        }
        
        # Absolute time patterns
        time_pattern = r'(\d{1,2}):(\d{2})\s*(am|pm)?'
        time_match = re.search(time_pattern, text, re.IGNORECASE)
        if time_match:
            time_refs["absolute"] = time_match.group(0)
        
        # Relative time patterns
        relative_patterns = [
            (r'in (\d+) (second|minute|hour|day)s?', 'future'),
            (r'(\d+) (second|minute|hour|day)s? ago', 'past'),
            (r'(tomorrow|yesterday|today)', 'relative_day')
        ]
        
        for pattern, ref_type in relative_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                time_refs["relative"] = {
                    "type": ref_type,
                    "match": match.group(0)
                }
                break
        
        return time_refs
    
    def calculate_math(self, expression):
        """Safely evaluate a mathematical expression"""
        import re
        
        # Extract just the math expression
        expression = expression.lower()
        # Remove question marks and common words
        expression = re.sub(r'(what is|calculate|compute|solve|equals?|=|\?)', '', expression)
        expression = expression.strip()
        
        # Replace word operators with symbols
        expression = expression.replace(' plus ', '+').replace(' add ', '+')
        expression = expression.replace(' minus ', '-').replace(' subtract ', '-')
        expression = expression.replace(' times ', '*').replace(' multiplied by ', '*').replace(' multiply ', '*')
        expression = expression.replace(' divided by ', '/').replace(' divide ', '/')
        
        # Replace common symbols
        expression = expression.replace('x', '*').replace('×', '*').replace('÷', '/')
        
        # Only allow numbers, operators, spaces, parentheses, and decimal points
        if not re.match(r'^[0-9+\-*/.() ]+$', expression):
            return {"success": False, "error": "Invalid characters in expression"}
        
        try:
            # Safely evaluate
            result = eval(expression)
            return {
                "success": True,
                "expression": expression,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
