import subprocess
import os
import shutil

ALLOWED_COMMANDS = [
    "ls", "pwd", "whoami", "uname", "df", "du", "top", "ps",
    "cat", "echo", "mkdir", "touch", "rm", "mv", "cp", "find",
    "grep", "ping", "curl", "wget", "git", "python", "pip",
    "ifconfig", "ip", "netstat", "ss", "nmap", "whois", "dig",
    "traceroute", "arp", "chmod", "chown", "systemctl", "service",
    "apt", "apt-get", "pacman", "dnf", "yum"
]

def is_allowed(command):
    base = command.strip().split()[0]
    return base in ALLOWED_COMMANDS

def run_command(command):
    if not is_allowed(command):
        return f"I won't run that command. It's not on my approved list."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "Command ran but returned no output."
    except subprocess.TimeoutExpired:
        return "Command timed out."
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