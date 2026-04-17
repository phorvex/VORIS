import requests
import json
import os
import subprocess
import re

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def get_best_model():
    try:
        import psutil
        available_gb = psutil.virtual_memory().available / (1024**3)
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = [m["name"] for m in response.json().get("models", [])]
            if available_gb > 5 and "qwen2.5-coder:latest" in models:
                return "qwen2.5-coder:latest"
            if available_gb > 5 and "qwen2.5-coder:7b" in models:
                return "qwen2.5-coder:7b"
            if "qwen2.5-coder:3b" in models:
                return "qwen2.5-coder:3b"
            if models:
                return models[0]
    except:
        pass
    return "qwen2.5-coder:3b"

CODE_MODEL = get_best_model()

VORIS_CODE_PROMPT = """You are VORIS's coding brain. You are precise, efficient, and direct.
You write clean code, explain it clearly, and never refuse a coding request.
You support every programming language. When writing code, always include brief comments.
Keep responses concise but complete."""

last_code = {
    "code": None,
    "language": None,
    "filename": None
}

def is_ollama_available():
    try:
        response = requests.get("http://127.0.0.1:11434", timeout=2)
        return True
    except:
        return False

def detect_language(code, prompt):
    prompt_lower = prompt.lower()
    if any(w in prompt_lower for w in ["python", ".py"]):
        return "python", ".py"
    if any(w in prompt_lower for w in ["javascript", "js", "node"]):
        return "javascript", ".js"
    if any(w in prompt_lower for w in ["html", "website", "webpage"]):
        return "html", ".html"
    if any(w in prompt_lower for w in ["bash", "shell", "script"]):
        return "bash", ".sh"
    if any(w in prompt_lower for w in ["css"]):
        return "css", ".css"
    if any(w in prompt_lower for w in ["java "]):
        return "java", ".java"
    if any(w in prompt_lower for w in ["c++", "cpp"]):
        return "cpp", ".cpp"
    if any(w in prompt_lower for w in ["rust"]):
        return "rust", ".rs"
    if any(w in prompt_lower for w in ["go ", "golang"]):
        return "go", ".go"
    if "```python" in code:
        return "python", ".py"
    if "```html" in code:
        return "html", ".html"
    if "```javascript" in code or "```js" in code:
        return "javascript", ".js"
    if "```bash" in code or "```sh" in code:
        return "bash", ".sh"
    return "unknown", ".txt"

def extract_code_blocks(text):
    pattern = r'```(?:\w+)?\n(.*?)```'
    blocks = re.findall(pattern, text, re.DOTALL)
    if blocks:
        return blocks[0]
    return text

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
            timeout=180
        )
        if response.status_code == 200:
            result = response.json()
            full_response = result.get("response", "").strip()
            language, ext = detect_language(full_response, prompt)
            code_only = extract_code_blocks(full_response)
            last_code["code"] = code_only
            last_code["language"] = language
            last_code["filename"] = None
            return full_response
        return None
    except Exception as e:
        print(f"Code brain error: {e}")
        return None

def save_code(filepath=None):
    if not last_code["code"]:
        return "I don't have any code to save right now."
    if not filepath:
        ext = {
            "python": ".py", "javascript": ".js", "html": ".html",
            "bash": ".sh", "css": ".css", "java": ".java",
            "cpp": ".cpp", "rust": ".rs", "go": ".go", "unknown": ".txt"
        }.get(last_code["language"], ".txt")
        filepath = os.path.expanduser(f"~/voris_code/code{ext}")
    filepath = os.path.expanduser(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(last_code["code"])
    last_code["filename"] = filepath
    return f"Saved to {filepath}."

def run_code(filepath=None):
    target = filepath or last_code["filename"]
    if not target:
        if last_code["code"] and last_code["language"] == "python":
            tmp = os.path.expanduser("~/voris_code/temp_run.py")
            os.makedirs(os.path.dirname(tmp), exist_ok=True)
            with open(tmp, "w") as f:
                f.write(last_code["code"])
            target = tmp
        else:
            return "No file to run. Save the code first."
    target = os.path.expanduser(target)
    language = last_code["language"]
    if target.endswith(".py"):
        language = "python"
    elif target.endswith(".sh"):
        language = "bash"
    elif target.endswith(".js"):
        language = "javascript"
    try:
        if language == "python":
            result = subprocess.run(["python3", target], capture_output=True, text=True, timeout=30)
        elif language == "bash":
            result = subprocess.run(["bash", target], capture_output=True, text=True, timeout=30)
        elif language == "javascript":
            result = subprocess.run(["node", target], capture_output=True, text=True, timeout=30)
        else:
            return f"I don't know how to run {language} files yet."
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "Code ran with no output."
    except subprocess.TimeoutExpired:
        return "Code timed out after 30 seconds."
    except Exception as e:
        return f"Error running code: {str(e)}"

def serve_html(filepath=None):
    target = filepath or last_code["filename"]
    if not target and last_code["language"] == "html":
        target = os.path.expanduser("~/voris_code/temp.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w") as f:
            f.write(last_code["code"])
    if not target:
        return "No HTML file to serve."
    target = os.path.expanduser(target)
    directory = os.path.dirname(target)
    try:
        subprocess.Popen(
            ["python3", "-m", "http.server", "8080"],
            cwd=directory,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return f"Serving at http://localhost:8080. Open that in your browser."
    except Exception as e:
        return f"Couldn't start server: {str(e)}"

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