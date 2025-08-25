def GetTextUser(message):
    """
    Extrae texto del mensaje entrante según el tipo.
    Soporta 'text' y 'interactive' (button_reply / list_reply).
    """
    try:
        msg_type = message.get('type')
        if msg_type == 'text':
            return (message.get('text') or {}).get('body', "")
        elif msg_type == 'interactive':
            interactive = message.get('interactive') or {}
            itype = interactive.get('type')
            if itype == 'button_reply':
                return (interactive.get('button_reply') or {}).get('title', "")
            elif itype == 'list_reply':
                return (interactive.get('list_reply') or {}).get('title', "")
            else:
                print("Tipo interactivo no soportado:", itype)
                return ""
        else:
            print("Tipo de mensaje no soportado:", msg_type)
            return ""
    except Exception as e:
        print("GetTextUser error:", e)
        return ""


# Si el usuario envía 'text', este modelo responde con texto simple.
def TextMessage(text, number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            # Si quieres vista previa de links, puedes agregar preview_url: True/False
            "body": text
        }
    }


# Si el usuario manda 'format', responde usando formatos de WhatsApp.
def TextFormatMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": "*Negrita*\n- _Cursiva_\n- ~Tachado~\n```Monoespaciado```"
        }
    }


# Enviar imagen por URL pública
def ImageMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "image",
        "image": {
            "link": "https://i.pinimg.com/736x/80/6b/7e/806b7e5dc3aa6de56fe8f5f06517abea.jpg"
        }
    }


# Enviar audio por URL pública
def AudioMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "audio",
        "audio": {
            "link": "https://www.myinstants.com/media/sounds/efecto-de-sonido-conchetumare.mp3"
        }
    }


# Enviar video por URL pública
def VideoMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "video",
        "video": {
            "link": "https://ssscdn.io/ssstwitter/1941853689465164001/rTYn_3UZyfR2321X"
        }
    }


# Enviar documento por URL pública
def DocumentMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "link": "https://unidel.edu.ng/focelibrary/books/A-Complete-Guide-to-the-Google-Cloud-Platform.pdf"
        }
    }


# Enviar ubicación
def LocationMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "location",
        "location": {
            "latitude": "-20.232658580098622",
            "longitude": "-70.14280943203991",
            "name": "Mallplaza Iquique",
            "address": "Av. Héroes de la Concepción 2555, 1110003 Iquique, Tarapacá"
        }
    }


# Enviar botones (interactive button)
def ButtonMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Elige una opción"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {"id": "ID_SI", "title": "Sí ✅"}
                    },
                    {
                        "type": "reply",
                        "reply": {"id": "ID_NO", "title": "No ✘"}
                    }
                ]
            }
        }
    }


# Enviar lista (interactive list)
def ListMessage(number):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": "✅ I have these options"},
            "footer": {"text": "Select an option"},
            "action": {
                "button": "See options",
                "sections": [
                    {
                        "title": "Buy and sell products",
                        "rows": [
                            {"id": "main-buy", "title": "Buy", "description": "Buy the best product your home"},
                            {"id": "main-sell", "title": "Sell", "description": "Sell your products"}
                        ]
                    },
                    {
                        "title": "📍Center of attention",
                        "rows": [
                            {"id": "main-agency", "title": "Agency", "description": "You can visit our agency"},
                            {"id": "main-contact", "title": "Contact center", "description": "One of our agents will assist you"}
                        ]
                    }
                ]
            }
        }
    }