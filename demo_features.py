#!/usr/bin/env python3
"""
Quick demo of new Voris features
Shows scheduling, news, email, and plugins in action
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_new_features():
    """Demonstrate the new features"""
    
    print("=" * 60)
    print("VORIS NEW FEATURES DEMO")
    print("=" * 60)
    print()
    
    print("This demo will show you the new capabilities:")
    print("  1. Scheduling & Reminders")
    print("  2. News Headlines")
    print("  3. Email Integration")
    print("  4. Plugin System")
    print()
    
    from voris_advanced import VorisAdvanced
    
    print("Initializing Voris...")
    voris = VorisAdvanced(voice_enabled=False)
    print()
    
    # Demo 1: Scheduling
    print("\n" + "=" * 60)
    print("DEMO 1: Scheduling & Reminders")
    print("=" * 60)
    
    commands = [
        "set timer for 10 seconds",
        "remind me to check the demo in 30 seconds",
        "list timers",
        "list reminders"
    ]
    
    for cmd in commands:
        print(f"\n> {cmd}")
        voris.process_command(cmd)
    
    # Demo 2: News
    print("\n" + "=" * 60)
    print("DEMO 2: News Headlines")
    print("=" * 60)
    
    commands = [
        "news",
        "tech news"
    ]
    
    for cmd in commands:
        print(f"\n> {cmd}")
        voris.process_command(cmd)
    
    # Demo 3: Email (will show setup needed if not configured)
    print("\n" + "=" * 60)
    print("DEMO 3: Email Integration")
    print("=" * 60)
    
    print("\nNote: Email requires configuration. See NEW_FEATURES_GUIDE.md")
    print("> check email")
    voris.process_command("check email")
    
    # Demo 4: Plugins
    print("\n" + "=" * 60)
    print("DEMO 4: Plugin System")
    print("=" * 60)
    
    commands = [
        "list plugins"
    ]
    
    for cmd in commands:
        print(f"\n> {cmd}")
        voris.process_command(cmd)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print("Try these features yourself with:")
    print("  python3 voris_advanced.py")
    print()
    print("For more information:")
    print("  - README.md - Overview and installation")
    print("  - NEW_FEATURES_GUIDE.md - Detailed feature guide")
    print("  - ADVANCED_FEATURES.md - Advanced usage")
    print()


if __name__ == "__main__":
    demo_new_features()
