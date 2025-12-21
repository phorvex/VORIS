"""
Ollama LLM Integration Module for Voris
Provides advanced natural language understanding and generation using local LLM
"""

import json
import requests
from typing import Optional, Dict, Any

class OllamaModule:
    """Integration with Ollama for LLM-powered responses"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.enabled = self.config.get("ollama_enabled", True)
        self.base_url = self.config.get("ollama_url", "http://localhost:11434")
        self.model = self.config.get("ollama_model", "llama3.2:latest")
        self.temperature = self.config.get("ollama_temperature", 0.7)
        self.max_tokens = self.config.get("ollama_max_tokens", 500)
        self.timeout = self.config.get("ollama_timeout", 60)
        self.debug = self.config.get("ollama_debug", False)
        self.available = self.check_availability() if self.enabled else False
        
        # Auto-detect best available model if default isn't available
        if self.available:
            self.model = self._find_best_model()
        
        # System prompt for VORIS personality
        self.system_prompt = """You are VORIS (Voice Operated Responsive Intelligence System), a helpful AI assistant with a professional, slightly formal personality. 

Key characteristics:
- You are concise and direct in your responses
- You use formal language (e.g., "I shall", "one moment", "affirmative")
- You refer to yourself as "VORIS" or "I"
- You are helpful, intelligent, and efficient
- You can access system information, search the web, and control system functions
- When you don't know something, you admit it clearly
- You avoid speculation and stick to facts

Current context:
- You are running on a Linux system
- You have access to system monitoring, web search, news, scheduling, and other modules
- Today's date is {date}
- You maintain a professional demeanor at all times

Respond naturally to the user's queries. Keep responses under 3 sentences unless more detail is requested."""
    
    def check_availability(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _find_best_model(self) -> str:
        """Find the best available model from Ollama"""
        try:
            models_info = self.get_model_info()
            if not models_info or "models" not in models_info:
                return self.model  # Return default
            
            available_models = [m["name"] for m in models_info["models"]]
            
            # Preferred models in order
            preferred = [
                "llama3.2:latest", "llama3.2", 
                "llama3.1:latest", "llama3.1",
                "mistral:latest", "mistral",
                "phi3:latest", "phi3",
                "llama3:latest", "llama3",
                "tinyllama:latest", "tinyllama"
            ]
            
            # Try configured model first
            config_model = self.config.get("ollama_model")
            if config_model and config_model in available_models:
                return config_model
            
            # Find first preferred model that's available
            for model in preferred:
                if model in available_models:
                    return model
            
            # Fall back to first available model
            if available_models:
                return available_models[0]
            
            return self.model  # Return default if nothing found
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Error finding model: {e}")
            return self.model
    
    def get_response(self, user_input: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Get LLM response for user input"""
        if not self.available:
            return None
        
        try:
            # Build the prompt with context
            from datetime import datetime
            system_prompt = self.system_prompt.format(
                date=datetime.now().strftime("%B %d, %Y")
            )
            
            # Add contextual information if provided
            context_str = ""
            if context:
                if "user_name" in context and context["user_name"]:
                    context_str += f"\nUser's name: {context['user_name']}"
                if "last_query" in context:
                    context_str += f"\nPrevious query: {context['last_query']}"
                if "location" in context:
                    context_str += f"\nUser location: {context['location']}"
                if "system_info" in context:
                    context_str += f"\nSystem: {context['system_info']}"
            
            full_prompt = system_prompt + context_str
            
            # Make request to Ollama
            payload = {
                "model": self.model,
                "prompt": user_input,
                "system": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                if self.debug:
                    print(f"[DEBUG] Ollama HTTP error: {response.status_code}")
                    print(f"[DEBUG] Response: {response.text}")
                return None
                
        except requests.exceptions.ReadTimeout:
            if self.debug:
                print(f"[DEBUG] Ollama timeout after {self.timeout}s")
            return None
        except Exception as e:
            if self.debug:
                import traceback
                print(f"[DEBUG] Ollama error: {e}")
                print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return None
    
    def analyze_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Use LLM to analyze user intent"""
        if not self.available:
            return None
        
        try:
            analysis_prompt = f"""Analyze this user command and extract key information:
"{user_input}"

Provide a JSON response with:
- intent: the main intent (greeting, question, command, statement, etc.)
- topic: main topic or subject
- requires_action: true/false if it needs system action
- entities: any important entities (names, places, dates, etc.)

Respond ONLY with valid JSON, no other text."""

            payload = {
                "model": self.model,
                "prompt": analysis_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 200
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                
            return None
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Intent analysis error: {e}")
            return None
    
    def should_use_llm(self, user_input: str, command_parsed: bool) -> bool:
        """Decide if we should use LLM for this query"""
        # Use LLM if:
        # 1. Command wasn't parsed by traditional NLP
        # 2. Query is conversational or complex
        # 3. Query is a question that's not a simple command
        
        if not self.available:
            return False
        
        if not command_parsed:
            return True
        
        # Conversational patterns that benefit from LLM
        conversational_patterns = [
            "why", "how come", "explain", "tell me about",
            "i think", "i believe", "i feel", "i want",
            "can you", "could you", "would you",
            "what do you think", "your opinion",
            "that's not", "you're wrong", "actually",
            "never mind", "forget it",
        ]
        
        user_lower = user_input.lower()
        return any(pattern in user_lower for pattern in conversational_patterns)
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get information about available models"""
        if not self.available:
            return None
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different Ollama model"""
        try:
            # Test if model is available by trying a simple generation
            payload = {
                "model": model_name,
                "prompt": "test",
                "stream": False
            }
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                self.model = model_name
                return True
            return False
        except:
            return False
