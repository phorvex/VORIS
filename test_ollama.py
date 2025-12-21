#!/usr/bin/env python3
"""
Quick test script to demonstrate Ollama integration with VORIS
"""

import sys
sys.path.insert(0, '/run/media/phorvex/LLM/VORIS')

from modules.ollama_module import OllamaModule

def test_ollama():
    """Test Ollama module"""
    print("=" * 60)
    print("VORIS Ollama LLM Integration Test")
    print("=" * 60)
    
    # Initialize Ollama
    ollama = OllamaModule()
    
    print(f"\nOllama Available: {ollama.available}")
    if not ollama.available:
        print("\n❌ Ollama is not running or not accessible.")
        print("\nTo use Ollama:")
        print("1. Install: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Pull model: ollama pull llama3.2")
        print("3. Start service: ollama serve")
        print("\nFor more info, see OLLAMA_INTEGRATION.md")
        return
    
    print(f"Ollama URL: {ollama.base_url}")
    print(f"Model: {ollama.model}")
    
    # Get model info
    models = ollama.get_model_info()
    if models:
        print(f"\nAvailable models: {len(models.get('models', []))}")
        for model in models.get('models', [])[:3]:
            print(f"  - {model['name']}")
    
    # Test queries
    test_queries = [
        "what is your name",
        "who are you",
        "that's not what I meant",
        "explain how you work",
        "what can you help me with"
    ]
    
    print("\n" + "=" * 60)
    print("Testing sample queries...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n> {query}")
        
        context = {
            "user_name": "User",
            "system_info": "Linux"
        }
        
        response = ollama.get_response(query, context)
        if response:
            print(f"[VORIS]: {response}")
        else:
            print("[ERROR]: No response from Ollama")
        print("-" * 60)
    
    print("\n✅ Ollama integration test complete!")
    print("\nYou can now run VORIS and it will use Ollama for")
    print("conversational queries and unknown commands.")

if __name__ == "__main__":
    test_ollama()
