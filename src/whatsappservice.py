# src/whatsapp_api_service.py
import requests
from src.secrets_gcp import _fetch_secret_raw

GRAPH_VERSION = "v22.0"
API_TIMEOUT = 15

# Leer secretos una sola vez al iniciar el servicio
GRAPH_TOKEN = _fetch_secret_raw(
    "projects/592174418442/secrets/whatsapp_graph_token_moshiro/versions/latest"
)
PHONE_NUMBER_ID = _fetch_secret_raw(
    "projects/592174418442/secrets/whatsapp_phone_number_id_moshiro/versions/latest"
)

def SendMessageWhatsaap(data):
    try:
        if not GRAPH_TOKEN or not PHONE_NUMBER_ID:
            print("[whatsapp] Falta token o phone_number_id")
            return False

        api_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {GRAPH_TOKEN}",
            "Content-Type": "application/json",
        }

        resp = requests.post(api_url, json=data, headers=headers, timeout=API_TIMEOUT)

        print("Status code:", resp.status_code)
        print("Response:", resp.text)

        return resp.status_code in (200, 201, 202)

    except requests.Timeout:
        print("[whatsapp] Timeout al llamar a Graph API")
        return False
    except Exception as exc:
        print("Error enviando mensaje a WhatsApp:", exc)
        return False