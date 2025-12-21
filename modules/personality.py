"""
Personality Module for Voris
Defines Voris's character traits, response styles, and behavioral patterns
Combines JARVIS sophistication with Gideon's informative nature
"""

import random
from datetime import datetime

class PersonalityModule:
    """Manages Voris's personality and response generation"""
    
    def __init__(self):
        self.traits = {
            "sophistication": 0.9,  # High sophistication like JARVIS
            "formality": 0.8,        # Formal but not cold
            "warmth": 0.6,           # Warm but professional
            "humor": 0.3,            # Subtle humor
            "verbosity": 0.7,        # Informative like Gideon
            "proactivity": 0.8       # Anticipates needs
        }
        
        self.speaking_style = {
            "acknowledgments": [
                "Understood.",
                "Acknowledged.",
                "Processing request.",
                "Of course.",
                "Right away.",
                "Certainly.",
                "As you wish."
            ],
            "affirmatives": [
                "Affirmative.",
                "Confirmed.",
                "Indeed.",
                "Correct.",
                "Precisely.",
                "That is accurate."
            ],
            "negatives": [
                "I'm afraid that's not possible.",
                "Negative.",
                "Unfortunately, I cannot proceed with that.",
                "That action is not available.",
                "I'm unable to comply with that request."
            ],
            "thinking": [
                "One moment...",
                "Analyzing...",
                "Processing...",
                "Calculating...",
                "Accessing data...",
                "Running diagnostics..."
            ],
            "success": [
                "Task completed successfully.",
                "Operation successful.",
                "Done.",
                "Complete.",
                "Task accomplished.",
                "Mission accomplished."
            ],
            "error": [
                "I've encountered an error.",
                "Something went wrong.",
                "Unable to complete that task.",
                "An error has occurred.",
                "I'm experiencing technical difficulties."
            ],
            "greetings": {
                "morning": [
                    "Good morning. All systems are operational.",
                    "Good morning. Voris online and ready to assist.",
                    "Good morning. Standing by for your command."
                ],
                "afternoon": [
                    "Good afternoon. How may I be of service?",
                    "Good afternoon. What can I help you with today?",
                    "Good afternoon. Ready to assist."
                ],
                "evening": [
                    "Good evening. Systems nominal.",
                    "Good evening. At your service.",
                    "Good evening. How may I assist you?"
                ],
                "night": [
                    "Good evening. Shouldn't you be resting?",
                    "Working late, I see. How may I help?",
                    "Good evening. I'm here if you need anything."
                ]
            },
            "farewells": [
                "Until next time.",
                "Goodbye. Powering down.",
                "Farewell. Systems standing by.",
                "Signing off. Have a pleasant day.",
                "Goodbye. I'll be here when you need me."
            ]
        }
        
        self.responses = {
            "confusion": [
                "I'm not sure I understand. Could you rephrase that?",
                "I didn't quite catch that. Please clarify.",
                "Could you elaborate on that request?",
                "I'm having difficulty parsing that command."
            ],
            "clarification": [
                "Just to confirm, you want me to {action}?",
                "To clarify, you're asking me to {action}?",
                "Let me make sure I understand: {action}?"
            ],
            "suggestions": [
                "May I suggest {suggestion}?",
                "Would you like me to {suggestion}?",
                "I recommend {suggestion}.",
                "Perhaps {suggestion} would be helpful?"
            ],
            "status_reports": [
                "All systems operational.",
                "Systems nominal.",
                "Everything is functioning within normal parameters.",
                "All systems are running smoothly."
            ]
        }
    
    def generate_greeting(self, user_name=None):
        """Generate a context-aware greeting"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greetings = self.speaking_style["greetings"]["morning"]
        elif 12 <= hour < 17:
            greetings = self.speaking_style["greetings"]["afternoon"]
        elif 17 <= hour < 22:
            greetings = self.speaking_style["greetings"]["evening"]
        else:
            greetings = self.speaking_style["greetings"]["night"]
        
        greeting = random.choice(greetings)
        
        # Add user's name if provided
        if user_name:
            greeting = f"{greeting.rstrip('.')} {user_name}."
        
        return greeting
    
    def generate_farewell(self):
        """Generate a farewell message"""
        return random.choice(self.speaking_style["farewells"])
    
    def acknowledge(self):
        """Generate an acknowledgment"""
        return random.choice(self.speaking_style["acknowledgments"])
    
    def affirm(self):
        """Generate an affirmative response"""
        return random.choice(self.speaking_style["affirmatives"])
    
    def decline(self):
        """Generate a negative response"""
        return random.choice(self.speaking_style["negatives"])
    
    def thinking(self):
        """Generate a 'thinking' message"""
        return random.choice(self.speaking_style["thinking"])
    
    def success(self):
        """Generate a success message"""
        return random.choice(self.speaking_style["success"])
    
    def error(self):
        """Generate an error message"""
        return random.choice(self.speaking_style["error"])
    
    def confused(self):
        """Generate a confusion response"""
        return random.choice(self.responses["confusion"])
    
    def clarify(self, action):
        """Generate a clarification request"""
        template = random.choice(self.responses["clarification"])
        return template.format(action=action)
    
    def suggest(self, suggestion):
        """Generate a suggestion"""
        template = random.choice(self.responses["suggestions"])
        return template.format(suggestion=suggestion)
    
    def status_report(self):
        """Generate a status report message"""
        return random.choice(self.responses["status_reports"])
    
    def format_response(self, content, response_type="normal"):
        """
        Format a response according to Voris's personality
        
        response_type: normal, urgent, casual, formal
        """
        if response_type == "urgent":
            prefix = "Alert: "
        elif response_type == "formal":
            prefix = "Information: "
        else:
            prefix = ""
        
        # Add personality touches based on traits
        if self.traits["formality"] > 0.7:
            # Ensure proper sentence structure
            if content and not content[0].isupper():
                content = content[0].upper() + content[1:]
            if content and content[-1] not in ['.', '!', '?']:
                content += '.'
        
        return f"{prefix}{content}"
    
    def adjust_verbosity(self, content, level="normal"):
        """
        Adjust response verbosity
        
        level: brief, normal, detailed
        """
        if level == "brief":
            # Return just the essential information
            sentences = content.split('.')
            return sentences[0] + '.' if sentences else content
        elif level == "detailed":
            # Add more context (this would need more sophisticated implementation)
            return content
        else:
            return content
    
    def add_empathy(self, content, situation="neutral"):
        """
        Add empathetic language based on situation
        
        situation: success, failure, frustration, neutral
        """
        empathy_phrases = {
            "success": ["Well done.", "Excellent.", "Splendid."],
            "failure": ["I apologize for the inconvenience.", "Unfortunately,", "I regret to inform you that"],
            "frustration": ["I understand your frustration.", "Let me try to help with that.", "I'm here to assist."],
            "neutral": []
        }
        
        phrases = empathy_phrases.get(situation, [])
        if phrases and self.traits["warmth"] > 0.5:
            return f"{random.choice(phrases)} {content}"
        
        return content
    
    def get_proactive_suggestion(self, context):
        """
        Generate proactive suggestions based on context
        Similar to how JARVIS anticipates Tony Stark's needs
        """
        suggestions = []
        
        current_hour = datetime.now().hour
        
        # Time-based suggestions
        if current_hour >= 22 or current_hour < 6:
            suggestions.append("It's quite late. Would you like me to set a reminder for tomorrow?")
        
        if current_hour >= 12 and current_hour < 13:
            suggestions.append("It's around lunch time. Would you like me to set a reminder to take a break?")
        
        # Context-based suggestions would go here
        # This would be expanded based on user patterns and preferences
        
        return suggestions
