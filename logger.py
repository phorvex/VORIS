import os
import gzip
import shutil
import datetime
import traceback
import threading

# Where all logs live — hidden folder in your home directory
LOG_DIR = os.path.expanduser("~/.voris/logs")

# Every category of log we track
CATEGORIES = [
    "system",        # CPU, RAM, boot, shutdown, hardware
    "security",      # access attempts, unknown faces, violations
    "conversation",  # every exchange with VORIS
    "smart_home",    # device commands and results
    "errors",        # crashes, exceptions, failures
    "learning",      # what she learned and from where
    "self",          # her personal record, emotional states
    "performance",   # response times, trends
    "master",        # everything in one place
    "twilio"         # SMS, calls, failures
]

# Severity levels from least to most important
LEVELS = ["DEBUG", "INFO", "WARNING", "ALERT", "CRITICAL"]

def ensure_dirs():
    # Creates all log folders if they don't exist yet
    # Runs every time we log so we never crash from missing folders
    for cat in CATEGORIES:
        os.makedirs(os.path.join(LOG_DIR, cat), exist_ok=True)
    # Special subfolder for unknown face images
    os.makedirs(os.path.join(LOG_DIR, "security", "unknown_faces"), exist_ok=True)

def today():
    # Returns today's date as a string for filenames like 2026-06-01.log
    return datetime.datetime.now().strftime("%Y-%m-%d")

def now():
    # Returns full timestamp for log entries like 2026-06-01 14:32:01
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(category, level, source, message, details=""):
    # The core logging function — everything flows through here
    # category: which log file to write to
    # level: how serious this is
    # source: what part of VORIS generated this
    # message: what happened
    # details: extra info like tracebacks or extra context
    ensure_dirs()
    if level not in LEVELS:
        level = "INFO"
    if category not in CATEGORIES:
        category = "master"

    # Build the log entry — clean and readable
    entry = f"[{now()}] [{category.upper()}] [{level}] [{source}]\n{message}\n"
    if details:
        entry += f"{details}\n"
    entry += "---\n"

    # Write to the specific category log AND the master log
    # So you can look at just errors or see everything in one place
    cat_file = os.path.join(LOG_DIR, category, f"{today()}.log")
    master_file = os.path.join(LOG_DIR, "master", f"{today()}.log")
    for path in [cat_file, master_file]:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"[LOGGER ERROR] Could not write log: {e}")

    # Print critical and alert messages to terminal immediately
    # So you see them even if you're watching the terminal
    if level in ["ALERT", "CRITICAL"]:
        print(f"\n[VORIS {level}] {message}")

# ── SPECIFIC LOG FUNCTIONS ────────────────────────────────────
# These are shortcuts so the rest of the code doesn't have to
# remember category names and levels every time

def log_system(message, level="INFO", details=""):
    # For system health — CPU, RAM, boot, shutdown, hardware changes
    log("system", level, "SYSTEM", message, details)

def log_security(message, level="INFO", source="SECURITY", details=""):
    # For all security events — access attempts, face detection, violations
    log("security", level, source, message, details)

def log_conversation(user, user_input, intent, response, response_time):
    # Logs every exchange — who said what, what VORIS understood, how long it took
    msg = f"User: {user} | Intent: {intent} | Time: {response_time:.2f}s"
    details = f"Input: {user_input}\nResponse: {response[:500]}"
    log("conversation", "INFO", user, msg, details)

def log_error(source, message, exc=None):
    # Logs errors with full traceback if an exception is provided
    # exc=True means grab the current exception automatically
    details = traceback.format_exc() if exc else ""
    log("errors", "CRITICAL", source, message, details)
    # Also write to master so it shows up when reading all logs
    log("master", "CRITICAL", source, f"ERROR in {source}: {message}", details)

def log_learning(topic, content, source):
    # Logs every new thing VORIS learns — topic, what she learned, where it came from
    msg = f"Learned: {topic} | Source: {source}"
    details = content[:500] if content else ""
    log("learning", "INFO", "VORIS", msg, details)

def log_self(message, details=""):
    # VORIS's personal log — emotional states, self observations, development notes
    log("self", "INFO", "VORIS", message, details)

def log_performance(stats):
    # Logs performance snapshots — response times, search latency, trends
    # stats is a dictionary like {"avg_response": 1.2, "searches": 14}
    details = "\n".join([f"{k}: {v}" for k, v in stats.items()])
    log("performance", "INFO", "SYSTEM", "Performance snapshot", details)

def log_smart_home(user, command, device, result):
    # Logs every smart home action — who did it, what device, what happened
    msg = f"User: {user} | Command: {command} | Device: {device} | Result: {result}"
    log("smart_home", "INFO", user, msg)

def log_twilio(direction, to_from, content, result):
    # Logs all Twilio activity — SMS sent/received, calls made/received
    # direction: "SENT" or "RECEIVED"
    msg = f"{direction} | {to_from} | Result: {result}"
    details = f"Content: {content[:200]}"
    log("twilio", "INFO", "TWILIO", msg, details)

# ── READING LOGS ──────────────────────────────────────────────
# These functions let VORIS read her own logs and let you ask her about them

def read_log(category="master", date=None):
    # Reads a log file for a given category and date
    # If no date given it reads today's log
    # Also handles compressed (.gz) files from previous days
    ensure_dirs()
    date = date or today()
    path = os.path.join(LOG_DIR, category, f"{date}.log")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    # Check for compressed version
    gz_path = path + ".gz"
    if os.path.exists(gz_path):
        with gzip.open(gz_path, "rt", encoding="utf-8") as f:
            return f.read()
    return f"No logs found for {category} on {date}."

def get_recent_errors(n=10):
    # Returns the last n error entries so VORIS can tell you what went wrong
    content = read_log("errors")
    entries = content.split("---\n")
    # Filter out empty entries and return the last n
    entries = [e for e in entries if e.strip()]
    return "---\n".join(entries[-n:]) if entries else "No errors logged today."

def get_recent_alerts():
    # Returns all ALERT and CRITICAL entries from today's master log
    content = read_log("master")
    lines = content.split("\n")
    alerts = [l for l in lines if "[ALERT]" in l or "[CRITICAL]" in l]
    return "\n".join(alerts[-20:]) if alerts else "No alerts today."

def get_todays_summary():
    # Generates a brief summary of today's activity for the morning digest
    # Counts entries by category and level
    summary = []
    for cat in CATEGORIES:
        path = os.path.join(LOG_DIR, cat, f"{today()}.log")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            count = content.count("---")
            if count > 0:
                summary.append(f"{cat}: {count} entries")
    errors = content.count("[CRITICAL]") if "content" in dir() else 0
    result = "Today's log summary:\n" + "\n".join(summary)
    if errors:
        result += f"\n{errors} critical errors — check the error log."
    return result if summary else "No activity logged today."

# ── COMPRESSION AND CLEANUP ───────────────────────────────────
# Runs nightly at 3am to keep logs small and tidy

def compress_old_logs():
    # Compresses all log files from previous days to .gz format
    # gzip typically reduces size by 70-90%
    ensure_dirs()
    today_str = today()
    for cat in CATEGORIES:
        cat_dir = os.path.join(LOG_DIR, cat)
        if not os.path.exists(cat_dir):
            continue
        for fname in os.listdir(cat_dir):
            # Only compress plain .log files that aren't today's
            if fname.endswith(".log") and not fname.startswith(today_str):
                fpath = os.path.join(cat_dir, fname)
                gz_path = fpath + ".gz"
                if not os.path.exists(gz_path):
                    try:
                        with open(fpath, "rb") as f_in:
                            with gzip.open(gz_path, "wb") as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(fpath)
                    except Exception as e:
                        print(f"[LOGGER] Compression failed for {fname}: {e}")

def cleanup_old_logs():
    # Deletes logs older than the retention period for each category
    # Learning and self logs are kept forever — they're her personal history
    ensure_dirs()
    now_dt = datetime.datetime.now()
    retention = {
        "security":     365,   # 1 year — security is important
        "errors":       180,   # 6 months
        "conversation": 90,    # 3 months
        "smart_home":   60,    # 2 months
        "twilio":       90,    # 3 months
        "learning":     9999,  # forever
        "self":         9999,  # forever — her personal record
        "performance":  30,    # 1 month
        "system":       90,    # 3 months
        "master":       90,    # 3 months
    }
    for cat, days in retention.items():
        cat_dir = os.path.join(LOG_DIR, cat)
        if not os.path.exists(cat_dir):
            continue
        for fname in os.listdir(cat_dir):
            if not (fname.endswith(".log") or fname.endswith(".log.gz")):
                continue
            fpath = os.path.join(cat_dir, fname)
            date_str = fname.replace(".log.gz", "").replace(".log", "")
            try:
                file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                age = (now_dt - file_date).days
                if age > days:
                    os.remove(fpath)
            except Exception:
                pass  # Skip files that don't match the date format

def run_nightly_maintenance():
    # Runs compression and cleanup then logs that it happened
    compress_old_logs()
    cleanup_old_logs()
    log_self("Nightly maintenance complete. Logs compressed and cleaned.")

def schedule_nightly():
    # Starts a background thread that wakes up at 3am every night
    # and runs the maintenance tasks without interrupting VORIS
    def run():
        while True:
            now_dt = datetime.datetime.now()
            # Calculate seconds until next 3am
            next_3am = now_dt.replace(hour=3, minute=0, second=0, microsecond=0)
            if now_dt >= next_3am:
                next_3am += datetime.timedelta(days=1)
            wait = (next_3am - now_dt).total_seconds()
            threading.Event().wait(wait)
            run_nightly_maintenance()
    t = threading.Thread(target=run, daemon=True)
    # daemon=True means this thread dies when VORIS shuts down
    # so it doesn't keep the process alive after exit
    t.start()