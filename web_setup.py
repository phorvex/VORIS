#!/usr/bin/env python3
"""
VORIS Web Setup Server
Interactive localhost interface for configuring all VORIS features
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'voris-setup-secret-key'

# Configuration directory
CONFIG_DIR = Path.home() / ".voris"
CONFIG_DIR.mkdir(exist_ok=True)

# ==================== HOME PAGE ====================
@app.route('/')
def index():
    """Main setup page"""
    return render_template('setup.html')

# ==================== CONFIGURATION API ====================

@app.route('/api/config/home_automation', methods=['GET', 'POST'])
def config_home_automation():
    """Home automation device configuration"""
    config_file = CONFIG_DIR / "home" / "devices.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify([])
    
    elif request.method == 'POST':
        devices = request.json
        with open(config_file, 'w') as f:
            json.dump(devices, f, indent=4)
        return jsonify({"success": True, "message": "Devices saved successfully"})

@app.route('/api/config/communication', methods=['GET', 'POST'])
def config_communication():
    """Communication settings (Slack, Discord, Twilio)"""
    config_file = CONFIG_DIR / "communication" / "communication_config.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify({
            "slack_webhook": "",
            "discord_webhook": "",
            "twilio_account_sid": "",
            "twilio_auth_token": "",
            "twilio_phone_number": ""
        })
    
    elif request.method == 'POST':
        config = request.json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return jsonify({"success": True, "message": "Communication settings saved"})

@app.route('/api/config/email', methods=['GET', 'POST'])
def config_email():
    """Email account configuration"""
    config_file = CONFIG_DIR / "email_config.json"
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify({"accounts": []})
    
    elif request.method == 'POST':
        config = request.json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return jsonify({"success": True, "message": "Email accounts saved"})

@app.route('/api/config/finance', methods=['GET', 'POST'])
def config_finance():
    """Finance and budget configuration"""
    config_file = CONFIG_DIR / "finance" / "budget.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify({
            "monthly_limit": 0,
            "categories": {}
        })
    
    elif request.method == 'POST':
        config = request.json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return jsonify({"success": True, "message": "Budget settings saved"})

@app.route('/api/config/health', methods=['GET', 'POST'])
def config_health():
    """Health and wellness goals"""
    config_file = CONFIG_DIR / "health" / "health_config.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify({
            "water_goal_ml": 2000,
            "water_reminder_interval": 60,
            "screen_break_interval": 30,
            "posture_check_interval": 45
        })
    
    elif request.method == 'POST':
        config = request.json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return jsonify({"success": True, "message": "Health goals saved"})

@app.route('/api/config/habits', methods=['GET', 'POST'])
def config_habits():
    """Habit tracking configuration"""
    config_file = CONFIG_DIR / "context" / "habits.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify([])
    
    elif request.method == 'POST':
        habits = request.json
        with open(config_file, 'w') as f:
            json.dump(habits, f, indent=4)
        return jsonify({"success": True, "message": "Habits saved"})

@app.route('/api/test/device', methods=['POST'])
def test_device():
    """Test device connection"""
    data = request.json
    device_type = data.get('type')
    ip_address = data.get('ip')
    
    # Simple ping test
    import subprocess
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', ip_address], 
                              capture_output=True, timeout=3)
        if result.returncode == 0:
            return jsonify({"success": True, "message": f"Device at {ip_address} is reachable"})
        else:
            return jsonify({"success": False, "message": "Device not responding"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/test/email', methods=['POST'])
def test_email():
    """Test email connection"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    imap_server = data.get('imap_server', 'imap.gmail.com')
    
    import imaplib
    try:
        mail = imaplib.IMAP4_SSL(imap_server, 993, timeout=5)
        mail.login(email, password)
        mail.logout()
        return jsonify({"success": True, "message": "Email connection successful"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Connection failed: {str(e)}"})

@app.route('/api/config/accounts', methods=['GET', 'POST'])
def config_accounts():
    """Device account integration (Google, Alexa, Microsoft, etc.)"""
    config_file = CONFIG_DIR / "accounts" / "device_accounts.json"
    config_file.parent.mkdir(exist_ok=True)
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file) as f:
                return jsonify(json.load(f))
        return jsonify({})
    
    elif request.method == 'POST':
        data = request.json
        provider = data.get('provider')
        
        # Load existing accounts
        accounts = {}
        if config_file.exists():
            with open(config_file) as f:
                accounts = json.load(f)
        
        # Update account for provider
        account_data = {k: v for k, v in data.items() if k != 'provider'}
        account_data['connected'] = True
        account_data['connected_at'] = str(Path.ctime(Path.home()))
        
        accounts[provider] = account_data
        
        # Save accounts
        with open(config_file, 'w') as f:
            json.dump(accounts, f, indent=4)
        
        return jsonify({"success": True, "message": f"{provider.capitalize()} account connected"})

@app.route('/api/test/account', methods=['POST'])
def test_account():
    """Test device account connection"""
    data = request.json
    provider = data.get('provider')
    
    config_file = CONFIG_DIR / "accounts" / "device_accounts.json"
    
    if not config_file.exists():
        return jsonify({"success": False, "error": "No account configured"})
    
    with open(config_file) as f:
        accounts = json.load(f)
    
    if provider not in accounts:
        return jsonify({"success": False, "error": f"{provider.capitalize()} account not found"})
    
    account = accounts[provider]
    
    # Basic validation - check if required fields exist
    try:
        if provider == 'google':
            if not account.get('clientId') or not account.get('clientSecret'):
                return jsonify({"success": False, "error": "Missing credentials"})
        elif provider == 'alexa':
            if not account.get('clientId') or not account.get('clientSecret'):
                return jsonify({"success": False, "error": "Missing credentials"})
        elif provider == 'microsoft':
            if not account.get('clientId') or not account.get('clientSecret'):
                return jsonify({"success": False, "error": "Missing credentials"})
        elif provider == 'ifttt':
            if not account.get('webhookKey'):
                return jsonify({"success": False, "error": "Missing webhook key"})
        elif provider == 'smartthings':
            if not account.get('token'):
                return jsonify({"success": False, "error": "Missing access token"})
        
        # If we get here, basic validation passed
        return jsonify({
            "success": True, 
            "message": f"{provider.capitalize()} credentials validated",
            "note": "Full OAuth flow would be completed in production"
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/status')
def get_status():
    """Get configuration status for all modules"""
    status = {
        "accounts": os.path.exists(CONFIG_DIR / "accounts" / "device_accounts.json"),
        "home_automation": os.path.exists(CONFIG_DIR / "home" / "devices.json"),
        "communication": os.path.exists(CONFIG_DIR / "communication" / "communication_config.json"),
        "email": os.path.exists(CONFIG_DIR / "email_config.json"),
        "finance": os.path.exists(CONFIG_DIR / "finance" / "budget.json"),
        "health": os.path.exists(CONFIG_DIR / "health" / "health_config.json"),
        "habits": os.path.exists(CONFIG_DIR / "context" / "habits.json")
    }
    return jsonify(status)

# ==================== STATIC FILES ====================
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def run_server(host='127.0.0.1', port=5000):
    """Start the web setup server"""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║         VORIS Interactive Setup Server                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\n🌐 Setup interface available at: http://{host}:{port}")
    print("📝 Configure all VORIS features through your web browser")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_server()
