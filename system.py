import platform
import psutil
import os

def get_system_info():
    info = {
        "machine": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "disk_total": round(psutil.disk_usage("/").total / (1024**3), 2),
        "disk_used": round(psutil.disk_usage("/").used / (1024**3), 2),
        "disk_percent": psutil.disk_usage("/").percent,
        "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    }
    return info

def get_system_summary():
    info = get_system_info()
    return (
        f"Running on {info['machine']} ({info['os']}) "
        f"as {info['user']}. "
        f"CPU at {info['cpu_percent']}%, "
        f"RAM {info['ram_used']}GB of {info['ram_total']}GB used ({info['ram_percent']}%), "
        f"Disk {info['disk_used']}GB of {info['disk_total']}GB used ({info['disk_percent']}%)."
    )