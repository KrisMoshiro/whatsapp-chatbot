import os
from flask import Flask, request
import src.utils as utils
import src.whatsappservice as whatsap_api_service  # OJO: ideal renombrar a whatsapp_api_service.py
from src.secrets_gcp import _fetch_secret_raw  # usa tu utilitario

# EB busca un objeto WSGI llamado "application"
application = Flask(__name__)

# Lee el secreto una sola vez al cargar el módulo
VERIFY_TOKEN = _fetch_secret_raw(
    "projects/592174418442/secrets/WHATSAPP_VERIFY_TOKEN_SECRET_PATH_MOSHIRO/versions/latest"
)

@application.route('/welcome', methods=['GET'])
def index():
    return "Welcome to the Flask App!"

@application.route('/whatsapp', methods=['GET'])
def VeirfyToken():
    try:
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token is not None and challenge is not None and token == VERIFY_TOKEN:
            return challenge
        else:
            return "", 400
    except Exception as e:
        print(f"[verify] error leyendo token: {e}")
        return "", 400

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
        number = message.get('from', '')
        text = utils.GetTextUser(message)

        ProcessMessages(text, number)
        print(f"[received_message] text='{text}' from={number}")

        return "EVENT_RECEIVED", 200
    except Exception as e:
        print(f"[received_message] error: {e}")
        return "EVENT_RECEIVED", 200

def ProcessMessages(text,number):
    text = text.lower()
    listData = []

    if "hola" in text or "option" in text:
        data = utils.TextMessage("hola weon qlo, que pasa hijo de la perra", number)
        dataMenu = utils.ListMessage(number)

        listData.append(data)
        listData.append(dataMenu)

    elif "chao" in text:
        data =  utils.TextMessage("chao conchetumare, no vimo", number)
    else:
        data =  utils.TextMessage("hola chileno qlo, no soy na venezolano", number)

    for item in listData:
        whatsap_api_service.SendMessageWhatsaap(data)

def generate_message(text, number):
    text_lower = (text or "").lower()

    if "text" in text_lower:
        data = utils.TextMessage(text, number)
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

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)