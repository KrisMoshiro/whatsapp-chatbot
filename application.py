import os
from flask import Flask, request
import src.util as utils
import src.whatsappservice as whatsap_api_service

# EB busca un objeto WSGI llamado "application"
application = Flask(__name__)

@application.route('/welcome', methods=['GET'])
def index():
    return "Welcome to the Flask App!"

# Webhook verification: devuelve el challenge sin validar token (según tu pedido)
@application.route('/whatsapp', methods=['GET'])
def VeirfyToken():

    try:
        access_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token != None and challenge != None and token == access_token:
            return challenge
        else:
            return "",400
    except:
        return "",400


# Mensajes entrantes (Meta envía POST a /whatsapp con el JSON que muestras)
@application.route('/whatsapp', methods=['POST'])
def received_message():
    try:
        body = request.get_json(force=True, silent=True) or {}
        entry = (body.get('entry') or [{}])[0]
        changes = (entry.get('changes') or [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages') or []

        if not messages:
            print("[received_message] payload sin 'messages'")
            return "EVENT_RECEIVED", 200

        message = messages[0]
        number = message.get('from', '')  # <-- este es el 'to' al que responderás
        text = utils.GetTextUser(message)

        generate_message(text, number)
        print(f"[received_message] text='{text}' from={number}")

        return "EVENT_RECEIVED", 200
    except Exception as e:
        print(f"[received_message] error: {e}")
        return "EVENT_RECEIVED", 200

def generate_message(text, number):
    text_lower = (text or "").lower()

    if "text" in text_lower:
        data = utils.TextMessage(text, number)  # corregido: usa variables, no literales
    elif "format" in text_lower:
        data = utils.TextFormatMessage(number)
    elif "image" in text_lower:
        data = utils.ImageMessage(number)
    elif "video" in text_lower:
        data = utils.VideoMessage(number)
    elif "audio" in text_lower:
        data = utils.AudioMessage(number)
    elif "document" in text_lower:
        data = utils.DocumentMessage(number)
    elif "location" in text_lower:
        data = utils.LocationMessage(number)
    elif "button" in text_lower:
        data = utils.ButtonMessage(number)
    elif "list" in text_lower:
        data = utils.ListMessage(number)
    else:
        data = utils.TextMessage("No entendí tu mensaje", number)

    whatsap_api_service.SendMessageWhatsaap(data)

if __name__ == '__main__':
    # Local o EB
    application.run(host="0.0.0.0", port=5000, debug=True)