import subprocess
import os

INTERACTIVE_COMMANDS = [
    "nano", "vim", "vi", "emacs", "top", "htop", "less", "more",
    "dpkg --configure", "apt upgrade", "apt install", "mysql", "python",
    "bash", "sh", "zsh", "fish", "ssh"
]

def is_interactive(command):
    for cmd in INTERACTIVE_COMMANDS:
        if cmd in command.lower():
            return True
    return False

def run_command(command):
    if is_interactive(command):
        return f"That command requires an interactive terminal. Run it directly in your terminal instead."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "Command ran but returned no output."
    except subprocess.TimeoutExpired:
        return "Command timed out after 60 seconds. If it needs longer, run it directly in your terminal."
    except Exception as e:
        return f"Error running command: {str(e)}"

def create_file(path, content=""):
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File created at {path}."
    except Exception as e:
        return f"Couldn't create file: {str(e)}"

def list_directory(path="."):
    try:
        items = os.listdir(path)
        files = [f for f in items if os.path.isfile(os.path.join(path, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]
        result = []
        if dirs:
            result.append(f"Folders: {', '.join(dirs)}")
        if files:
            result.append(f"Files: {', '.join(files)}")
        return "\n".join(result) if result else "Directory is empty."
    except Exception as e:
        return f"Couldn't list directory: {str(e)}"

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Couldn't read file: {str(e)}"

def delete_file(path):
    try:
        os.remove(path)
        return f"Deleted {path}."
    except Exception as e:
        return f"Couldn't delete file: {str(e)}"