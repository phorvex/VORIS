#!/usr/bin/env python3
"""
Simple quick test for VORIS with Ollama integration
Tests without actually querying Ollama (just checks availability)
"""

import sys
sys.path.insert(0, '/run/media/phorvex/LLM/VORIS')

from modules.ollama_module import OllamaModule

def quick_test():
    """Quick test without actual LLM queries"""
    print("=" * 60)
    print("VORIS Ollama Quick Check")
    print("=" * 60)
    
    # Initialize Ollama
    ollama = OllamaModule()
    
    print(f"\n✓ Ollama Available: {ollama.available}")
    if ollama.available:
        print(f"✓ Ollama URL: {ollama.base_url}")
        print(f"✓ Selected Model: {ollama.model}")
        
        # Get model info
        models = ollama.get_model_info()
        if models and 'models' in models:
            print(f"✓ Models installed: {len(models['models'])}")
            for model in models['models']:
                print(f"  - {model['name']}")
        
        print("\n✅ VORIS can use Ollama for intelligent responses!")
        print("\nNote: First query may be slow as the model loads.")
        print("Consider pulling llama3.2 for better performance:")
        print("  ollama pull llama3.2")
    else:
        print("\n⚠️  Ollama not available")
        print("\nTo enable LLM features:")
        print("1. Install: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Pull model: ollama pull llama3.2")
        print("3. Start: ollama serve")
    
    print("\n" + "=" * 60)
    print("Test complete! Run VORIS with: python3 voris_advanced.py")
    print("=" * 60)

if __name__ == "__main__":
    quick_test()
