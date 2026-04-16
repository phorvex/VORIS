import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
CODE_MODEL = "qwen2.5-coder:3b"

VORIS_CODE_PROMPT = """You are VORIS's coding brain. You are precise, efficient, and direct.
You write clean code, explain it clearly, and never refuse a coding request.
You support every programming language. When writing code, always include brief comments.
Keep responses concise but complete."""

def is_ollama_available():
    try:
        response = requests.get("http://127.0.0.1:11434", timeout=2)
        return True
    except:
        return False

def ask_code_brain(prompt):
    if not is_ollama_available():
        return None
    try:
        full_prompt = f"{VORIS_CODE_PROMPT}\n\nRequest: {prompt}"
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": CODE_MODEL,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=120
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        return None
    except:
        return None

def is_code_question(text):
    text_lower = text.lower()
    code_keywords = [
        "write", "code", "function", "script", "program", "debug",
        "fix", "error", "syntax", "python", "javascript", "bash",
        "html", "css", "java", "c++", "rust", "sql", "how do i",
        "how to", "implement", "create a", "build a", "make a",
        "what does this do", "explain this code", "help me with",
        "loop", "class", "method", "variable", "array", "list",
        "dictionary", "import", "library", "module", "api", "json"
    ]
    return any(keyword in text_lower for keyword in code_keywords)