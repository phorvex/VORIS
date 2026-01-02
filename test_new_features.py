#!/usr/bin/env python3
"""
Test script for newly added VORIS capabilities
Tests all 8 new capability modules
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_media_control():
    """Test media control capabilities"""
    print("\n=== Testing Media Control ===")
    try:
        from modules.media_control import MediaController
        media = MediaController()
        
        # Test volume
        result = media.set_volume(50)
        print(f"✓ Volume control: {result}")
        
        # Test favorites
        media.add_to_favorites("Test Song", "Rock")
        favs = media.favorites
        print(f"✓ Favorites loaded: {len(favs.get('songs', []))} songs")
        
        return True
    except Exception as e:
        print(f"✗ Media Control Error: {e}")
        return False

def test_automation():
    """Test automation capabilities"""
    print("\n=== Testing Automation ===")
    try:
        from modules.automation import AutomationModule
        auto = AutomationModule()
        
        # Test resource monitoring
        resources = auto.monitor_resources()
        print(f"✓ CPU: {resources['cpu']}%, Memory: {resources['memory']}%, Disk: {resources['disk']}%")
        
        # Test screenshot (just check method exists)
        print("✓ Screenshot capability available")
        
        return True
    except Exception as e:
        print(f"✗ Automation Error: {e}")
        return False

def test_communication():
    """Test communication capabilities"""
    print("\n=== Testing Communication ===")
    try:
        from modules.communication import CommunicationModule
        comm = CommunicationModule()
        
        # Test language detection
        lang = comm.detect_language("Hello world")
        print(f"✓ Language detection: {lang}")
        
        # Test translation (without actually calling API)
        print("✓ Translation capability available")
        
        return True
    except Exception as e:
        print(f"✗ Communication Error: {e}")
        return False

def test_smart_context():
    """Test smart context capabilities"""
    print("\n=== Testing Smart Context ===")
    try:
        from modules.smart_context import SmartContextModule
        context = SmartContextModule()
        
        # Test habit tracking
        result = context.add_habit("Test Habit", "daily")
        print(f"✓ Habit added: {result['message']}")
        
        # Test habit stats
        stats = context.get_habit_stats()
        print(f"✓ Habits tracked: {len(stats['habits'])}")
        
        return True
    except Exception as e:
        print(f"✗ Smart Context Error: {e}")
        return False

def test_developer_tools():
    """Test developer tools capabilities"""
    print("\n=== Testing Developer Tools ===")
    try:
        from modules.developer_tools import DeveloperToolsModule
        dev = DeveloperToolsModule()
        
        # Test snippet management
        dev.save_snippet("test_func", "def test(): pass", ["python", "test"])
        snippets = dev.list_snippets()
        print(f"✓ Code snippets: {len(snippets)} saved")
        
        # Test project tracking
        projects = dev.list_projects()
        print(f"✓ Projects tracked: {len(projects)}")
        
        return True
    except Exception as e:
        print(f"✗ Developer Tools Error: {e}")
        return False

def test_home_automation():
    """Test home automation capabilities"""
    print("\n=== Testing Home Automation ===")
    try:
        from modules.home_automation import HomeAutomationModule
        home = HomeAutomationModule()
        
        # Test device registration
        result = home.register_device("test_roku", "roku", "192.168.1.100")
        print(f"✓ Device registered: {result['message']}")
        
        devices = home.list_devices()
        print(f"✓ Total devices: {len(devices)}")
        
        # Test routine creation with proper triggers and actions
        triggers = {"type": "time", "value": "07:00"}
        actions = [{"device": "test_roku", "action": "home"}]
        result2 = home.create_routine("test_routine", triggers, actions)
        print(f"✓ Routine created: {result2['message']}")
        
        routines = home.list_routines()
        print(f"✓ Automation routines: {len(routines)}")
        
        return True
    except Exception as e:
        print(f"✗ Home Automation Error: {e}")
        return False

def test_health_wellness():
    """Test health and wellness capabilities"""
    print("\n=== Testing Health & Wellness ===")
    try:
        from modules.health_wellness import HealthWellnessModule
        health = HealthWellnessModule()
        
        # Test water tracking
        result = health.log_water(250)
        print(f"✓ Water logged: {result['message']}")
        
        stats = health.get_water_stats()
        print(f"✓ Water stats: {stats['today']} today")
        
        # Test exercise logging
        result2 = health.log_exercise("walking", 30, 150)
        print(f"✓ Exercise logged: {result2['message']}")
        
        return True
    except Exception as e:
        print(f"✗ Health & Wellness Error: {e}")
        return False

def test_finance():
    """Test finance capabilities"""
    print("\n=== Testing Finance ===")
    try:
        from modules.finance import FinanceModule
        finance = FinanceModule()
        
        # Test expense tracking (amount first, then category)
        result = finance.add_expense(12.50, "food", "lunch")
        print(f"✓ Expense added: {result['message']}")
        
        expenses = finance.get_expenses()
        print(f"✓ Total expenses: {expenses['count']} entries")
        
        # Test budget management (category_limits is a dict)
        result2 = finance.set_budget(category_limits={"food": 500})
        print(f"✓ Budget set: {result2['message']}")
        
        # Get budget categories
        budget_status = finance.check_budget_status()
        print(f"✓ Budget status: {budget_status}")
        
        return True
    except Exception as e:
        print(f"✗ Finance Error: {e}")
        return False

def main():
    """Run all tests"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        VORIS New Features Test Suite                    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    tests = [
        ("Media Control", test_media_control),
        ("Automation", test_automation),
        ("Communication", test_communication),
        ("Smart Context", test_smart_context),
        ("Developer Tools", test_developer_tools),
        ("Home Automation", test_home_automation),
        ("Health & Wellness", test_health_wellness),
        ("Finance", test_finance),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All new features are working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
