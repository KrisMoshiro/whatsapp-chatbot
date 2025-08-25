import os
import requests

GRAPH_VERSION = "v22.0"
GRAPH_TOKEN = os.getenv("WHATSAPP_GRAPH_TOKEN", "")          
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")  
API_TIMEOUT = 15

def SendMessageWhatsaap(data):
    try:
        if not GRAPH_TOKEN or not PHONE_NUMBER_ID:
            print("[whatsapp] Falta token o phone_number_id")
            return False

        api_url = f"https://graph.facebook.com/%7BGRAPH_VERSION%7D/%7BPHONE_NUMBER_ID%7D/messages"
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