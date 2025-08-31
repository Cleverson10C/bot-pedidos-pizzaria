from config_twilio import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from twilio.rest import Client

# Número do destinatário (cliente)
DESTINATARIO = 'whatsapp:+5541992356589'

def enviar_pedido_whatsapp(mensagem):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensagem,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=DESTINATARIO
    )
    return message.sid

# Exemplo de uso:
if __name__ == "__main__": 
    texto_pedido = "Pedido: Pizza Margherita, Pizza Calabresa"
    sid = enviar_pedido_whatsapp(texto_pedido)
    print(f"Mensagem enviada! SID: {sid}")
