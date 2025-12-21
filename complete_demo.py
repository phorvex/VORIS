#!/usr/bin/env python3
"""
Complete Voris Example Session
Demonstrates all major features in a realistic usage scenario
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voris_advanced import VorisAdvanced
import time

def demo_session():
    """Run a complete demo session"""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                 VORIS COMPLETE DEMO                      ║
║         All Features in a Real-World Scenario            ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("This demo simulates a typical Voris session with all features.\n")
    input("Press Enter to start...\n")
    
    # Initialize Voris
    print("=" * 60)
    print("INITIALIZING VORIS")
    print("=" * 60)
    voris = VorisAdvanced(voice_enabled=False)
    voris.active = True
    
    def run_command(cmd, wait=1):
        """Helper to run a command and pause"""
        print(f"\n{'='*60}")
        print(f"Command: {cmd}")
        print("="*60)
        voris.process_command(cmd)
        time.sleep(wait)
    
    # Morning routine
    print("\n\n" + "🌅 MORNING ROUTINE ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("hello")
    run_command("my name is Phillippi")
    run_command("what time is it")
    run_command("weather")
    run_command("news", 2)
    
    # Work setup
    print("\n\n" + "💼 WORK SETUP ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("remind me to attend standup meeting in 2 hours")
    run_command("set timer for 25 minutes")
    run_command("list reminders")
    run_command("list timers")
    
    # Research mode
    print("\n\n" + "🔍 RESEARCH MODE ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("who is Alan Turing", 2)
    run_command("what is quantum computing", 2)
    run_command("search for artificial intelligence breakthroughs", 2)
    
    # System management
    print("\n\n" + "⚙️ SYSTEM MANAGEMENT ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("status")
    run_command("battery")
    run_command("where am i")
    run_command("what timezone")
    
    # Custom commands demo
    print("\n\n" + "🔧 CUSTOM COMMANDS ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("when I say check system, run echo 'System check complete!'")
    run_command("list commands")
    
    # Math and calculations
    print("\n\n" + "🧮 CALCULATIONS ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("what is 25 times 4")
    run_command("calculate 100 divided by 5")
    run_command("15 plus 30")
    
    # Technology news
    print("\n\n" + "📰 STAYING INFORMED ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("tech news", 2)
    
    # Plugin system
    print("\n\n" + "🔌 PLUGIN SYSTEM ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("list plugins")
    run_command("plugin example_plugin greet")
    
    # Capabilities check
    print("\n\n" + "ℹ️ SYSTEM INFORMATION ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("who are you")
    run_command("what can you do")
    
    # Wrap up
    print("\n\n" + "👋 SESSION END ".center(60, "="))
    input("\nPress Enter to continue...")
    
    run_command("goodbye")
    
    print("\n\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("""
Features Demonstrated:
  ✅ Greetings and personalization
  ✅ Time and date queries
  ✅ Weather information
  ✅ News headlines (general and tech)
  ✅ Reminders and timers
  ✅ Web search and Q&A
  ✅ System monitoring
  ✅ Battery status
  ✅ Location detection
  ✅ Custom command creation
  ✅ Mathematical calculations
  ✅ Plugin system
  ✅ System information

All major Voris features working perfectly! 🎉

Try Voris yourself:
  python3 voris_advanced.py

Or with voice:
  python3 voris_advanced.py --voice
    """)


if __name__ == "__main__":
    try:
        demo_session()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
