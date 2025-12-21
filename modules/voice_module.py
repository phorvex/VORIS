"""
Voice Module for Voris
Handles text-to-speech and speech recognition
"""

import os
import platform

class VoiceModule:
    """Handles voice input and output for Voris"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.tts_engine = None
        self.stt_engine = None
        self.enabled = self.config.get('voice_enabled', True)
        self.wake_word = self.config.get('wake_word', 'voris').lower()
        self.listening_for_wake_word = False
        
        if self.enabled:
            self.initialize_tts()
            self.initialize_stt()
    
    def initialize_tts(self):
        """Initialize Text-to-Speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configure voice properties
            rate = self.config.get('voice_rate', 150)
            volume = self.config.get('voice_volume', 0.9)
            
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # Try to set a female voice (for Gideon-like character)
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            print("[Voice Module] TTS initialized successfully")
        except ImportError:
            print("[Voice Module] pyttsx3 not installed. TTS disabled.")
            print("Install with: pip install pyttsx3")
            self.tts_engine = None
        except Exception as e:
            print(f"[Voice Module] TTS initialization error: {e}")
            self.tts_engine = None
    
    def initialize_stt(self):
        """Initialize Speech-to-Text engine"""
        try:
            import speech_recognition as sr
            self.stt_engine = sr.Recognizer()
            print("[Voice Module] STT initialized successfully")
        except ImportError:
            print("[Voice Module] speech_recognition not installed. STT disabled.")
            print("Install with: pip install SpeechRecognition pyaudio")
            self.stt_engine = None
        except Exception as e:
            print(f"[Voice Module] STT initialization error: {e}")
            self.stt_engine = None
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.enabled or not self.tts_engine:
            return False
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"[Voice Module] TTS error: {e}")
            return False
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input and convert to text"""
        if not self.enabled or not self.stt_engine:
            return None
        
        try:
            import speech_recognition as sr
            
            with sr.Microphone() as source:
                print("[Listening...]")
                self.stt_engine.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.stt_engine.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("[Processing...]")
            text = self.stt_engine.recognize_google(audio)
            return text
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("[Voice Module] Could not understand audio")
            return None
        except Exception as e:
            print(f"[Voice Module] STT error: {e}")
            return None
    
    def set_voice_rate(self, rate):
        """Adjust speech rate"""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
            self.config['voice_rate'] = rate
    
    def set_voice_volume(self, volume):
        """Adjust speech volume (0.0 to 1.0)"""
        if self.tts_engine:
            self.tts_engine.setProperty('volume', min(1.0, max(0.0, volume)))
            self.config['voice_volume'] = volume
    
    def listen_for_wake_word(self, timeout=5):
        """
        Listen specifically for the wake word
        Returns True if wake word detected, False otherwise
        """
        if not self.enabled or not self.stt_engine:
            return False
        
        try:
            import speech_recognition as sr
            
            with sr.Microphone() as source:
                print(f"[Listening for '{self.wake_word}'...]")
                self.stt_engine.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.stt_engine.listen(source, timeout=timeout, phrase_time_limit=3)
            
            text = self.stt_engine.recognize_google(audio).lower()
            
            # Check if wake word is in the recognized text
            if self.wake_word in text:
                print(f"[Wake word '{self.wake_word}' detected!]")
                return True
            
            return False
        
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except Exception as e:
            print(f"[Voice Module] Wake word detection error: {e}")
            return False
    
    def continuous_listen_mode(self, callback, wake_word_mode=True):
        """
        Continuous listening mode
        
        Args:
            callback: Function to call when command is recognized
            wake_word_mode: If True, only listens after wake word is detected
        """
        if not self.enabled or not self.stt_engine:
            print("[Voice Module] Voice recognition not available")
            return
        
        print("[Continuous Listen Mode Active]")
        if wake_word_mode:
            print(f"[Say '{self.wake_word}' followed by your command]")
        else:
            print("[Always listening for commands]")
        
        self.listening_for_wake_word = wake_word_mode
        
        try:
            while True:
                if wake_word_mode:
                    # Wait for wake word
                    if self.listen_for_wake_word(timeout=5):
                        # Wake word detected, now listen for command
                        print("[Listening for command...]")
                        command = self.listen(timeout=5, phrase_time_limit=10)
                        if command:
                            callback(command)
                else:
                    # Always listening mode
                    command = self.listen(timeout=5, phrase_time_limit=10)
                    if command:
                        callback(command)
        
        except KeyboardInterrupt:
            print("\n[Continuous Listen Mode Stopped]")
            self.listening_for_wake_word = False
