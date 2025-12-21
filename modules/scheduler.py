"""
Scheduling and Reminder Module for Voris
Handles timers, alarms, reminders, and scheduled tasks
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

class SchedulerModule:
    """Manages scheduled tasks, reminders, timers, and alarms"""
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.schedules_file = self.config_dir / "schedules.json"
        self.schedules = self.load_schedules()
        self.active_timers = {}
        self.running = True
        
        # Start background scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def load_schedules(self):
        """Load scheduled tasks from file"""
        if self.schedules_file.exists():
            try:
                with open(self.schedules_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except (json.JSONDecodeError, ValueError):
                # If file is corrupted, backup and recreate
                import shutil
                backup_file = self.schedules_file.with_suffix('.json.bak')
                shutil.copy(self.schedules_file, backup_file)
                print(f"[Scheduler] Corrupted schedules file backed up to {backup_file}")
        
        return {
            "reminders": [],
            "alarms": [],
            "recurring": []
        }
    
    def save_schedules(self):
        """Save schedules to file"""
        with open(self.schedules_file, 'w') as f:
            json.dump(self.schedules, f, indent=4)
    
    def add_reminder(self, message, when, recurring=False):
        """
        Add a reminder
        
        Args:
            message: The reminder message
            when: datetime object or timedelta for when to remind
            recurring: If True, reminder repeats
        """
        if isinstance(when, timedelta):
            target_time = datetime.now() + when
        else:
            target_time = when
        
        reminder = {
            "id": len(self.schedules["reminders"]) + 1,
            "message": message,
            "time": target_time.isoformat(),
            "recurring": recurring,
            "completed": False
        }
        
        self.schedules["reminders"].append(reminder)
        self.save_schedules()
        
        return {
            "success": True,
            "message": f"Reminder set for {target_time.strftime('%I:%M %p on %B %d')}",
            "id": reminder["id"]
        }
    
    def add_timer(self, duration_seconds, label="Timer"):
        """
        Start a countdown timer
        
        Args:
            duration_seconds: Timer duration in seconds
            label: Optional label for the timer
        """
        timer_id = f"timer_{time.time()}"
        end_time = datetime.now() + timedelta(seconds=duration_seconds)
        
        self.active_timers[timer_id] = {
            "label": label,
            "duration": duration_seconds,
            "end_time": end_time,
            "started": datetime.now()
        }
        
        return {
            "success": True,
            "message": f"{label} set for {self._format_duration(duration_seconds)}",
            "timer_id": timer_id,
            "end_time": end_time.strftime('%I:%M:%S %p')
        }
    
    def list_active_timers(self):
        """Get list of active timers"""
        active = []
        for timer_id, timer in self.active_timers.items():
            remaining = (timer["end_time"] - datetime.now()).total_seconds()
            if remaining > 0:
                active.append({
                    "id": timer_id,
                    "label": timer["label"],
                    "remaining": remaining,
                    "remaining_formatted": self._format_duration(int(remaining))
                })
        return active
    
    def list_reminders(self, include_completed=False):
        """Get list of upcoming reminders"""
        reminders = []
        for reminder in self.schedules["reminders"]:
            if include_completed or not reminder["completed"]:
                remind_time = datetime.fromisoformat(reminder["time"])
                if remind_time > datetime.now() or include_completed:
                    reminders.append({
                        "id": reminder["id"],
                        "message": reminder["message"],
                        "time": remind_time.strftime('%I:%M %p on %B %d, %Y'),
                        "completed": reminder["completed"]
                    })
        return reminders
    
    def cancel_reminder(self, reminder_id):
        """Cancel a reminder by ID"""
        for i, reminder in enumerate(self.schedules["reminders"]):
            if reminder["id"] == reminder_id:
                self.schedules["reminders"].pop(i)
                self.save_schedules()
                return {"success": True, "message": f"Reminder {reminder_id} cancelled"}
        return {"success": False, "error": "Reminder not found"}
    
    def cancel_timer(self, timer_id):
        """Cancel a timer by ID"""
        if timer_id in self.active_timers:
            del self.active_timers[timer_id]
            return {"success": True, "message": "Timer cancelled"}
        return {"success": False, "error": "Timer not found"}
    
    def parse_time_expression(self, expression):
        """
        Parse natural language time expressions
        
        Examples:
            "in 5 minutes"
            "in 2 hours"
            "tomorrow at 3pm"
            "at 5:30pm"
        """
        expression = expression.lower().strip()
        now = datetime.now()
        
        # "in X minutes/hours/days"
        import re
        in_pattern = r'in (\d+)\s*(second|minute|hour|day)s?'
        match = re.search(in_pattern, expression)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            
            if unit == "second":
                return now + timedelta(seconds=amount)
            elif unit == "minute":
                return now + timedelta(minutes=amount)
            elif unit == "hour":
                return now + timedelta(hours=amount)
            elif unit == "day":
                return now + timedelta(days=amount)
        
        # "at HH:MM am/pm"
        at_pattern = r'at\s+(\d{1,2}):?(\d{2})?\s*(am|pm)?'
        match = re.search(at_pattern, expression)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            meridiem = match.group(3)
            
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if target < now:
                target += timedelta(days=1)
            
            # Check if "tomorrow" is in expression
            if "tomorrow" in expression:
                target += timedelta(days=1)
            
            return target
        
        # "tomorrow"
        if "tomorrow" in expression:
            return now + timedelta(days=1)
        
        return None
    
    def _format_duration(self, seconds):
        """Format duration in seconds to human readable string"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if secs > 0 or not parts:
            parts.append(f"{secs} second{'s' if secs > 1 else ''}")
        
        return " and ".join(parts)
    
    def _scheduler_loop(self):
        """Background thread that checks for due reminders and timers"""
        while self.running:
            try:
                now = datetime.now()
                
                # Check reminders
                for reminder in self.schedules["reminders"]:
                    if not reminder["completed"]:
                        remind_time = datetime.fromisoformat(reminder["time"])
                        if now >= remind_time:
                            self._trigger_reminder(reminder)
                
                # Check timers
                completed_timers = []
                for timer_id, timer in self.active_timers.items():
                    if now >= timer["end_time"]:
                        self._trigger_timer(timer)
                        completed_timers.append(timer_id)
                
                # Remove completed timers
                for timer_id in completed_timers:
                    del self.active_timers[timer_id]
                
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"[Scheduler] Error: {e}")
    
    def _trigger_reminder(self, reminder):
        """Trigger a reminder notification"""
        print(f"\n🔔 REMINDER: {reminder['message']}")
        reminder["completed"] = True
        self.save_schedules()
        # TODO: Add system notification
    
    def _trigger_timer(self, timer):
        """Trigger a timer completion notification"""
        print(f"\n⏰ TIMER COMPLETE: {timer['label']}")
        # TODO: Add system notification
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
