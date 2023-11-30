import requests
import sett
import json
import time
import server
import dict
from server import bienvenido 

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text
  


def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    elif media_type == "image":
        media_id = sett.images.get(media_name, None)
    elif media_type == "video":
        media_id = sett.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data
  
  

listext = []
def administrar_chatbot(text,number, messageId, name):

    text = text.lower() #mensaje que envio el usuario
    list = []
    listext.append(text)
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)
    
    if "hola" in text:
      
        listext.clear()
        sett.sets = None
        textMessage = text_Message(number, "El siguiente chat permite visualizar Indicadores comericales (Cartera, ICV e ICC), así como lista de clientes antiguos y barrios")
        enviar_Mensaje_whatsapp(textMessage)
        
        body = "Hola soy SteveBoy, el chat de información y soporte comercial, ¿Qué quieres explorar?"
        footer = "📝Para continuar, Selecciona una opción"
        options = ["👥 Asesores", "🏡 Zonas", "📈 General"]
        
        #Asesor = text.upper() + " "
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        time.sleep(2)
        
    elif "inicio" in text:
        listext.clear()
        sett.sets = None
        body = "Hola de nuevo, ¿Qué quieres explorar?"
        footer = "📝Para continuar, Selecciona una opción"
        options = ["👥 Asesores", "🏡 Zonas", "📈 General"]
        
        #Asesor = text.upper() + " "
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        time.sleep(2)
        
    
    elif "asesores" in text:
        textMessage = text_Message(number, "Ingresa tu nombre. _Ej: ASESOR STIVEN_")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(2)
    
    elif "asesor" in text:
        body = "📝Para continuar, Selecciona una opción"
        footer = "¿Qué quieres explorar?"
        options = ["👥 Prospectos", "🏘️ Barrios", "📊 Indicadores"]
        
        #Asesor = text.upper() + " "
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData) 
        
        
    elif "prospectos" in text:
        
        
            # Supongamos que tienes un DataFrame llamado clientes en dict.clientes
        df = dict.clientes
        asesor = listext[1].upper() + " "
            # Filtra el DataFrame por el Asesor deseado, por ejemplo, 'ASESOR CHICA'
        filtro = df[df['Asesor'] == asesor]
        
        #texto_df = filtro.to_string(index=False)

        print(listext)

        textMessage = text_Message(number, "En un segundo te enviaré un csv con los prospectos 👉 _Ingresa al link para descargar_")
        enviar_Mensaje_whatsapp(textMessage)
        #textMessage2 = text_Message(number, texto_df)
        #enviar_Mensaje_whatsapp(textMessage2)
        
        
        sett.sets = filtro
        print(sett.sets)
        
        time.sleep(2)
        textMessage3 = text_Message(number, sett.document_url)
        enviar_Mensaje_whatsapp(textMessage3)
        
        time.sleep(2)
        body = "¿Quieres explorar algo más? Selecciona la opción Inicio"
        footer = "👇"
        options = ["👋 Inicio", "🤝 Finalizar"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
    
    elif "indicadores" in text:
        
        # Supongamos que tienes un DataFrame llamado clientes en dict.clientes
        df = dict.resultados
        #df2 = dict.datos2
        
        asesor = listext[1].upper() + " "
            # Filtra el DataFrame por el Asesor deseado, por ejemplo, 'ASESOR CHICA'
        filtro = df[df['ASESOR_CIERRE'] == asesor]
        #filtro2 = df2[df2['ASESOR_CIERRE'] == asesor]
        
        #ICV = filtro2['VENCIDO'].sum() / filtro2[' SALDO_CORTE '].sum() * 100
        #filtro = df[df.index.get_level_values('ASESOR_CIERRE') == asesor]
        #indicador = asesor + " " + ICV
        #filtro = df[df['Asesor'] == 'ASESOR CHICA ']
        #R = print(filtro)
        #server.df = filtro
        texto_df = filtro.to_string(index=False)

        
        
        textMessage = text_Message(number, "En un segundo te enviaré un csv con los prospectos 👉 _Ingresa al link para descargar_")
        enviar_Mensaje_whatsapp(textMessage)
        #textMessage2 = text_Message(number, ICV)
        #enviar_Mensaje_whatsapp(textMessage2)
        
        #document = document_Message(number, sett.document_url, "Listo 👍🏻", "clientes.pdf")

        #enviar_Mensaje_whatsapp(document)
        #time.sleep(2)
        sett.sets = filtro
        
        time.sleep(2)
        textMessage3 = text_Message(number, sett.document_url)
        enviar_Mensaje_whatsapp(textMessage3)
        
        time.sleep(2)
        body = "¿Quieres explorar algo más? Selecciona la opción Inicio"
        footer = "👇"
        options = ["👋 Inicio", "🤝 Finalizar"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
        
    elif "barrios" in text:
        body = "¡Upsss!, esta opción aún se encuentra en proceso"
        footer = "Selecciona la opción para retornar"
        options = ["👋 Inicio"]
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫤")
        list.append(replyReaction)
        list.append(replyButtonData)
      
      
        #Hasta aquí llega el código de retorno para asesor e inicia el de Zonas
    
    elif "zonas" in text:   
        
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        
        body1 = "Selecciona una de las siguientes zonas de Antioquia:"
        footer1 = "👇"
        options1 = sett.zona1
        
        body2 = "Selecciona la zona de otros departamentos:"
        footer2 = "👇"
        options2 = sett.zona2

        listReplyData = listReply_Message(number, options1, body1, footer1, "sed2",messageId)
        list.append(listReplyData)
        
        listReplyData2 = listReply_Message(number, options2, body2, footer2, "sed2",messageId)
        list.append(listReplyData2)
        
    elif text in sett.zonas:
      
        textMessage = text_Message(number, "En un segundo te enviaré un csv con los prospectos 👉 _Ingresa al link para descargar_")
        enviar_Mensaje_whatsapp(textMessage)
        
        print(text)
        
        df = dict.resultados_zona
        zona = text.upper()
        
        filtro_zona = df[df['OFICINA_CIERRE'] == zona]
        
        sett.sets = filtro_zona
        print(sett.sets)
        
        time.sleep(2)
        textMessage = text_Message(number, sett.document_url)
        enviar_Mensaje_whatsapp(textMessage)
        
        time.sleep(2)
        body = "¿Quieres explorar algo más? Selecciona la opción Inicio"
        footer = "👇"
        options = ["👋 Inicio", "🤝 Finalizar"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
    #Hasta aquí llega el código de retorno para asesor e inicia el general
    
    elif "general" in text:   
        
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        
        body = "Selecciona el detalle del informe"
        footer = "👇"
        options = ['Oficinas', 'Municipios']
        

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
    elif "oficinas" in text:
        textMessage = text_Message(number, "En un segundo te enviaré un csv con los prospectos 👉 _Ingresa al link para descargar_")
        enviar_Mensaje_whatsapp(textMessage)
        
        df = dict.resultados_lider
        
        sett.sets = df
        print(sett.sets)
        
        time.sleep(2)
        textMessage = text_Message(number, sett.document_url)
        enviar_Mensaje_whatsapp(textMessage)
        
        time.sleep(2)
        body = "¿Quieres explorar algo más? Selecciona la opción Inicio"
        footer = "👇"
        options = ["👋 Inicio", "🤝 Finalizar"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
    elif "municipios" in text:
        textMessage = text_Message(number, "En un segundo te enviaré un csv con los prospectos 👉 _Ingresa al link para descargar_")
        enviar_Mensaje_whatsapp(textMessage)
        
        df = dict.resultados_detallado
        
        sett.sets = df
        print(sett.sets)
        
        time.sleep(2)
        textMessage = text_Message(number, sett.document_url)
        enviar_Mensaje_whatsapp(textMessage)
        
        time.sleep(2)
        body = "¿Quieres explorar algo más? Selecciona la opción Inicio"
        footer = "👇"
        options = ["👋 Inicio", "Finalizar"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        
        
    elif "finalizar" in text:
        
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
      
        textMessage = text_Message(number, "Fue un gusto ayudarte, si requieres algo más enviame un Hola")
        enviar_Mensaje_whatsapp(textMessage)
        
               
    else:
        data = text_Message(number,"¡Ups!, no entendí lo que dijiste, para retornar escribe Hola🛠️")
        list.append(data)
    

    for item in list:
        enviar_Mensaje_whatsapp(item)
        
