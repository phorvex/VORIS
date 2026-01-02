#!/usr/bin/env python3
"""
Comprehensive VORIS Testing Suite
Tests all modules and features
"""

import sys
import os
import importlib.util

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n" + "="*70)
    print("  DEPENDENCY CHECK")
    print("="*70 + "\n")
    
    required_modules = {
        'psutil': 'System utilities',
        'pyttsx3': 'Text-to-speech',
        'speech_recognition': 'Speech recognition',
        'requests': 'HTTP requests'
    }
    
    missing = []
    for module_name, description in required_modules.items():
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"❌ {module_name:20} - {description} [MISSING]")
            missing.append(module_name)
        else:
            print(f"✅ {module_name:20} - {description} [OK]")
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} dependencies. Install with:")
        print(f"   sudo apt install python3-psutil python3-requests python3-pyttsx3 python3-speechrecognition")
        print(f"   or: pip install --user " + " ".join(missing))
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def test_modules():
    """Test if all VORIS modules can be imported"""
    print("\n" + "="*70)
    print("  MODULE IMPORT TEST")
    print("="*70 + "\n")
    
    modules_to_test = [
        'modules.voice_module',
        'modules.nlp_module',
        'modules.system_tasks',
        'modules.personality',
        'modules.web_module',
        'modules.custom_commands',
        'modules.scheduler',
        'modules.news_module',
        'modules.email_module',
        'modules.plugin_system',
        'modules.ollama_module'
    ]
    
    failed = []
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:30} [OK]")
        except Exception as e:
            print(f"❌ {module_name:30} [FAILED]: {str(e)[:50]}")
            failed.append(module_name)
    
    if failed:
        print(f"\n⚠️  {len(failed)} modules failed to import")
        return False
    
    print("\n✅ All modules imported successfully!")
    return True

def test_main_files():
    """Test main VORIS files"""
    print("\n" + "="*70)
    print("  MAIN FILES SYNTAX CHECK")
    print("="*70 + "\n")
    
    files_to_test = [
        'voris_ai.py',
        'voris_advanced.py',
        'check_ollama.py',
        'complete_demo.py'
    ]
    
    import py_compile
    failed = []
    
    for filename in files_to_test:
        if not os.path.exists(filename):
            print(f"⚠️  {filename:30} [SKIPPED - not found]")
            continue
            
        try:
            py_compile.compile(filename, doraise=True)
            print(f"✅ {filename:30} [OK]")
        except Exception as e:
            print(f"❌ {filename:30} [FAILED]: {str(e)[:50]}")
            failed.append(filename)
    
    if failed:
        print(f"\n⚠️  {len(failed)} files failed syntax check")
        return False
    
    print("\n✅ All files passed syntax check!")
    return True

def test_voris_basic():
    """Test basic VORIS functionality"""
    print("\n" + "="*70)
    print("  BASIC FUNCTIONALITY TEST")
    print("="*70 + "\n")
    
    try:
        from voris_advanced import VorisAdvanced
        print("✅ VorisAdvanced imported")
        
        print("\nInitializing VORIS (voice disabled for testing)...")
        voris = VorisAdvanced(voice_enabled=False)
        print("✅ VORIS instance created")
        
        # Test basic methods
        print("\nTesting basic methods:")
        
        # Test personality
        greeting = voris.personality.generate_greeting()
        print(f"✅ Personality greeting: '{greeting[:50]}...'")
        
        # Test NLP
        parsed = voris.nlp.parse_command("what time is it")
        print(f"✅ NLP command parsing: '{parsed.get('action', 'unknown')}'")
        
        # Test system info
        info = voris.system.get_system_info()
        print(f"✅ System info retrieved: OS={info['os']}, CPU={info['cpu_percent']}%")
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_features():
    """Test web-related features"""
    print("\n" + "="*70)
    print("  WEB FEATURES TEST")
    print("="*70 + "\n")
    
    try:
        from modules.web_module import WebModule
        web = WebModule()
        print("✅ WebModule initialized")
        
        # Test location detection
        location = web.get_location_info()
        if location and location.get('success'):
            print(f"✅ Location detected: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}")
        else:
            print("⚠️  Location detection failed (network issue?)")
        
        # Test weather (if location worked)
        if location and location.get('success'):
            weather = web.get_weather()
            if weather and weather.get('success'):
                print(f"✅ Weather retrieved: {weather.get('temp', 'N/A')}°C")
            else:
                print("⚠️  Weather retrieval failed")
        
        print("\n✅ Web features test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Web features test failed: {e}")
        return False

def test_ollama():
    """Test Ollama integration"""
    print("\n" + "="*70)
    print("  OLLAMA LLM INTEGRATION TEST")
    print("="*70 + "\n")
    
    try:
        from modules.ollama_module import OllamaModule
        ollama = OllamaModule()
        
        if ollama.available:
            print(f"✅ Ollama is available at {ollama.base_url}")
            print(f"✅ Using model: {ollama.model}")
            
            # Test query
            response = ollama.query("Hello", use_context=False)
            if response:
                print(f"✅ Ollama response received: '{response[:50]}...'")
            else:
                print("⚠️  Ollama query returned no response")
        else:
            print("⚠️  Ollama is not running or not installed")
            print("   This is optional - VORIS works without it")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Ollama test skipped: {e}")
        return True  # Not critical

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  VORIS COMPREHENSIVE TEST SUITE")
    print("  " + "="*68)
    print("="*70)
    
    results = {
        'Dependencies': test_dependencies(),
        'Main Files': test_main_files(),
        'Modules': test_modules(),
        'Basic Functionality': test_voris_basic(),
        'Web Features': test_web_features(),
        'Ollama': test_ollama()
    }
    
    print("\n" + "="*70)
    print("  TEST RESULTS SUMMARY")
    print("="*70 + "\n")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed! VORIS is ready to use!")
        print("\nRun: python3 voris_advanced.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
