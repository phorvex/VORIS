"""
System Tasks Module for Voris
Handles system operations, file management, and task automation
"""

import os
import subprocess
import platform
import psutil
from pathlib import Path
from datetime import datetime

class SystemTasksModule:
    """Handles system-level operations and task automation"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.os_version = platform.version()
    
    def execute_command(self, command, shell=True):
        """Execute a shell command safely"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def get_system_info(self):
        """Get detailed system information"""
        info = {
            "os": self.os_type,
            "os_version": self.os_version,
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": self.bytes_to_gb(psutil.virtual_memory().total),
                "available": self.bytes_to_gb(psutil.virtual_memory().available),
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": self.bytes_to_gb(psutil.disk_usage('/').total),
                "used": self.bytes_to_gb(psutil.disk_usage('/').used),
                "free": self.bytes_to_gb(psutil.disk_usage('/').free),
                "percent": psutil.disk_usage('/').percent
            }
        }
        return info
    
    def get_battery_status(self):
        """Get battery status information"""
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    "success": False,
                    "error": "No battery detected. System may be a desktop or battery info unavailable."
                }
            
            return {
                "success": True,
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
                "status": "Charging" if battery.power_plugged else "Discharging"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_timezone_info(self):
        """Get current timezone information"""
        try:
            import time
            
            # Get timezone info
            if time.daylight:
                tz_offset = time.altzone
                tz_name = time.tzname[1]
            else:
                tz_offset = time.timezone
                tz_name = time.tzname[0]
            
            # Convert offset to hours
            tz_hours = -tz_offset / 3600
            
            return {
                "success": True,
                "timezone": tz_name,
                "offset_hours": tz_hours,
                "offset_string": f"UTC{tz_hours:+.1f}",
                "local_time": datetime.now().strftime("%I:%M %p"),
                "local_date": datetime.now().strftime("%B %d, %Y")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def bytes_to_gb(bytes_value):
        """Convert bytes to gigabytes"""
        return round(bytes_value / (1024 ** 3), 2)
    
    def open_application(self, app_name):
        """Open an application by name"""
        try:
            if self.os_type == "Linux":
                # Try common ways to launch apps on Linux
                commands = [
                    f"{app_name}",
                    f"gtk-launch {app_name}",
                    f"xdg-open {app_name}"
                ]
                for cmd in commands:
                    result = self.execute_command(cmd)
                    if result["success"]:
                        return {"success": True, "message": f"Launched {app_name}"}
                return {"success": False, "message": f"Could not launch {app_name}"}
            
            elif self.os_type == "Darwin":  # macOS
                result = self.execute_command(f"open -a {app_name}")
                return {"success": result["success"], "message": result.get("error", f"Launched {app_name}")}
            
            elif self.os_type == "Windows":
                result = self.execute_command(f"start {app_name}")
                return {"success": result["success"], "message": result.get("error", f"Launched {app_name}")}
            
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def list_directory(self, path="."):
        """List directory contents"""
        try:
            path_obj = Path(path).expanduser()
            if not path_obj.exists():
                return {"success": False, "error": "Path does not exist"}
            
            items = []
            for item in path_obj.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            
            return {"success": True, "items": items, "count": len(items)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_directory(self, path):
        """Create a new directory"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return {"success": True, "message": f"Directory created: {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_files(self, directory, pattern="*", recursive=True):
        """Search for files matching a pattern"""
        try:
            path_obj = Path(directory).expanduser()
            if recursive:
                files = list(path_obj.rglob(pattern))
            else:
                files = list(path_obj.glob(pattern))
            
            results = [str(f) for f in files if f.is_file()]
            return {"success": True, "files": results, "count": len(results)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_running_processes(self, limit=10):
        """Get list of running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            return {"success": True, "processes": processes[:limit]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_reminder(self, message, delay_seconds):
        """Set a reminder (using system notifications)"""
        try:
            # This would need a separate notification module
            # For now, return a placeholder
            return {
                "success": True,
                "message": f"Reminder set for {delay_seconds} seconds: {message}",
                "note": "Notification system not yet implemented"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
