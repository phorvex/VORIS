import os
import platform
import threading
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

voris_handler = None

def set_web_handler(handler):
    global voris_handler
    voris_handler = handler

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/voris_face.jpg")
def face_image():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "voris_face.jpg")

@socketio.on("user_message")
def handle_message(data):
    text = data.get("text", "").strip()
    if not text:
        return
    emit("voris_state", {"state": "thinking"})
    if voris_handler:
        response = voris_handler(text)
    else:
        response = "I am not fully initialized yet."
    emit("voris_response", {"text": response, "speak": True})
    emit("voris_state", {"state": "idle"})

@socketio.on("connect")
def on_connect():
    emit("voris_state", {"state": "idle"})

def start_web_ui(handler=None, port=9117):
    if handler:
        set_web_handler(handler)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"), exist_ok=True)
    t = threading.Thread(
        target=lambda: socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True),
        daemon=True
    )
    t.start()
    print(f"VORIS Web UI running at http://localhost:{port}")