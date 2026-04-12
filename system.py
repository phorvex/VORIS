import platform
import psutil
import os
import socket
import subprocess

def get_system_info():
    return {
        "machine": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "disk_total": round(psutil.disk_usage("/").total / (1024**3), 2),
        "disk_used": round(psutil.disk_usage("/").used / (1024**3), 2),
        "disk_percent": psutil.disk_usage("/").percent,
        "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "home_dir": os.path.expanduser("~"),
        "current_dir": os.getcwd(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
    }

def get_system_summary():
    info = get_system_info()
    return (
        f"Running on {info['machine']} ({info['os']}) "
        f"as {info['user']}. "
        f"CPU at {info['cpu_percent']}% across {info['cpu_cores']} cores ({info['cpu_threads']} threads), "
        f"RAM {info['ram_used']}GB of {info['ram_total']}GB used ({info['ram_percent']}%), "
        f"Disk {info['disk_used']}GB of {info['disk_total']}GB used ({info['disk_percent']}%). "
        f"Hostname: {info['hostname']}, IP: {info['ip_address']}."
    )

def get_running_processes(limit=10):
    processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                       key=lambda p: p.info['memory_percent'] or 0, reverse=True)[:limit]:
        try:
            processes.append(
                f"PID {proc.info['pid']}: {proc.info['name']} "
                f"(CPU: {proc.info['cpu_percent']}%, RAM: {round(proc.info['memory_percent'], 2)}%)"
            )
        except:
            pass
    return "\n".join(processes) if processes else "No processes found."

def get_network_info():
    info = []
    for interface, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                info.append(f"{interface}: {addr.address}")
    stats = psutil.net_io_counters()
    info.append(f"Sent: {round(stats.bytes_sent / (1024**2), 2)}MB, Received: {round(stats.bytes_recv / (1024**2), 2)}MB")
    return "\n".join(info) if info else "No network info available."

def get_installed_packages():
    try:
        result = subprocess.run(["pip", "list"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split("\n")[2:]
        packages = [line.split()[0] for line in lines if line]
        return f"Installed packages ({len(packages)}): {', '.join(packages[:20])}{'...' if len(packages) > 20 else ''}"
    except:
        return "Could not retrieve installed packages."

def get_environment_vars():
    important = ["PATH", "HOME", "USER", "SHELL", "LANG", "TERM", "VIRTUAL_ENV", "CONDA_ENV"]
    env = {}
    for var in important:
        val = os.getenv(var)
        if val:
            env[var] = val
    return "\n".join([f"{k}: {v}" for k, v in env.items()]) if env else "No environment variables found."

def get_disk_partitions():
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append(
                f"{part.device} mounted at {part.mountpoint} "
                f"({round(usage.used / (1024**3), 2)}GB used of {round(usage.total / (1024**3), 2)}GB)"
            )
        except:
            pass
    return "\n".join(partitions) if partitions else "No partitions found."

def get_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "charging" if battery.power_plugged else "discharging"
            return f"Battery at {round(battery.percent)}% and {status}."
        return "No battery detected — likely a desktop or server."
    except:
        return "Battery info unavailable."

def get_uptime():
    import datetime
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"System has been up for {hours}h {minutes}m {seconds}s."