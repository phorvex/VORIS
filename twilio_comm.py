import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, Response
import threading

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ADMIN_NUMBER = os.getenv("ADMIN_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

app = Flask(__name__)
voris_handler = None

# ── OUTBOUND SMS ──────────────────────────────────────────────

def send_sms(message, to=None):
    try:
        to = to or ADMIN_NUMBER
        client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=to
        )
        return True
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def alert(message):
    send_sms(f"VORIS ALERT: {message}")

def critical_alert(message):
    send_sms(f"🚨 VORIS CRITICAL: {message}")

# ── OUTBOUND CALLING ──────────────────────────────────────────

def call_admin(message):
    try:
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{message}</Say>
    <Pause length="2"/>
    <Say voice="alice">This was an automated alert from VORIS. Goodbye.</Say>
</Response>"""
        call = client.calls.create(
            twiml=twiml,
            to=ADMIN_NUMBER,
            from_=TWILIO_NUMBER
        )
        return True
    except Exception as e:
        print(f"Call error: {e}")
        return False

# ── INBOUND SMS HANDLER ───────────────────────────────────────

@app.route("/sms", methods=["POST"])
def handle_sms():
    from_number = request.form.get("From")
    body = request.form.get("Body", "").strip()
    resp = MessagingResponse()

    if from_number != ADMIN_NUMBER:
        resp.message("Unauthorized.")
        return Response(str(resp), mimetype="text/xml")

    if voris_handler:
        response = voris_handler(body)
        resp.message(response)
    else:
        resp.message("VORIS is not available right now.")

    return Response(str(resp), mimetype="text/xml")

# ── INBOUND CALL HANDLER ──────────────────────────────────────

@app.route("/voice", methods=["POST"])
def handle_voice():
    from_number = request.form.get("From")
    resp = VoiceResponse()

    if from_number != ADMIN_NUMBER:
        resp.say("Unauthorized access.")
        return Response(str(resp), mimetype="text/xml")

    gather = resp.gather(
        input="speech",
        action="/voice/respond",
        language="en-US",
        speech_timeout="auto"
    )
    gather.say("VORIS online. What do you need?")
    return Response(str(resp), mimetype="text/xml")

@app.route("/voice/respond", methods=["POST"])
def handle_voice_respond():
    speech = request.form.get("SpeechResult", "")
    resp = VoiceResponse()

    if voris_handler and speech:
        response = voris_handler(speech)
        resp.say(response)
        gather = resp.gather(
            input="speech",
            action="/voice/respond",
            language="en-US",
            speech_timeout="auto"
        )
        gather.say("Anything else?")
    else:
        resp.say("I did not catch that. Goodbye.")

    return Response(str(resp), mimetype="text/xml")

# ── FLASK SERVER ──────────────────────────────────────────────

def start_server(handler=None, port=5000):
    global voris_handler
    voris_handler = handler
    t = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=port, debug=False),
        daemon=True
    )
    t.start()
    print(f"VORIS Twilio server running on port {port}")

def set_handler(handler):
    global voris_handler
    voris_handler = handler
