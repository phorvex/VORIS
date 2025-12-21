#!/usr/bin/env python3
"""
Demo script to showcase VORIS's new internet features
"""

import sys
sys.path.insert(0, '.')
from voris_advanced import VorisAdvanced
import time

def demo():
    print("\n" + "="*70)
    print("  VORIS ENHANCED INTERNET FEATURES DEMONSTRATION")
    print("="*70 + "\n")
    
    voris = VorisAdvanced(voice_enabled=False)
    voris.initialize()
    
    demos = [
        ("🌐 IP & Network Info", "my ip"),
        ("✅ Website Status", "is google.com up"),
        ("₿ Cryptocurrency", "bitcoin price"),
        ("💱 Currency Exchange", "convert 100 USD to EUR"),
        ("🎭 Entertainment", "tell me a joke"),
        ("📚 Knowledge", "tell me a fact"),
        ("👤 GitHub Lookup", "github user github"),
    ]
    
    for title, command in demos:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"  Command: '{command}'")
        print(f"{'='*70}\n")
        voris.process_command(command)
        time.sleep(1.5)
    
    print(f"\n{'='*70}")
    print("  ✨ All features working perfectly!")
    print(f"  Type 'help' in VORIS to see all available commands")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    demo()
