from flask import Flask, render_template, request
from whatsapp_twilio import enviar_pedido_whatsapp
from twilio.twiml.messaging_response import MessagingResponse
import unicodedata
from db_models import db, Produto, Pedido
from app_factory import create_app

app = create_app()

cardapio = {
    "1": "Pizza Margherita",
    "2": "Pizza Calabresa",
    "3": "Pizza Quatro Queijos",
    "4": "Pizza Portuguesa"
}

conversas = {}

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

@app.route("/")
def index():
    produtos = Produto.query.all()
    if request.accept_mimetypes.best_match(["application/json", "text/html"]) == "application/json":
        return {
            "produtos": [
                {"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos
            ]
        }
    return render_template("index.html", produtos=produtos)

@app.route("/pedido", methods=["POST"])
def pedido():
    itens = []
    if request.is_json:
        data = request.get_json()
        itens = data.get("item") or data.get("itens") or []
        if isinstance(itens, str):
            itens = [itens]
    else:
        itens = request.form.getlist("item")
    if not itens:
        return "Nenhum item selecionado."
    novo_pedido = Pedido(itens=", ".join(itens))
    db.session.add(novo_pedido)
    db.session.commit()
    mensagem = f"Novo pedido recebido: {novo_pedido.itens}"
    try:
        sid = enviar_pedido_whatsapp(mensagem)
        return f"✅ Pedido recebido e enviado para WhatsApp! SID: {sid}"
    except Exception as e:
        return f"✅ Pedido recebido, mas houve erro ao enviar para WhatsApp: {e}"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    numero = request.form.get("From")
    msg = request.form.get("Body", "").strip()
    print(f"Mensagem recebida: {msg} | Número: {numero}")
    resp = MessagingResponse()

    if numero not in conversas:
        conversas[numero] = {"etapa": "cardapio"}
    etapa = conversas[numero]["etapa"]
    print(f"Etapa atual: {etapa} | Conversas: {conversas[numero]}")
    msg_normalizada = remover_acentos(msg.lower())

    if etapa == "cardapio":
        saudacoes = ["bom dia", "boa tarde", "boa noite", "ola", "oi", "hello", "hi"]
        escolha = msg.strip()
        if escolha in cardapio:
            conversas[numero]["pedido"] = cardapio[escolha]
            conversas[numero]["etapa"] = "pagamento"
            resp.message("Qual a forma de pagamento? (pix, cartao ou dinheiro)")
        elif any(s in msg_normalizada for s in saudacoes):
            if "bom dia" in msg_normalizada:
                saudacao = "Bom dia! "
            elif "boa tarde" in msg_normalizada:
                saudacao = "Boa tarde! "
            elif "boa noite" in msg_normalizada:
                saudacao = "Boa noite! "
            elif "olá" in msg_normalizada or "ola" in msg_normalizada:
                saudacao = "Olá! "
            elif "oi" in msg_normalizada:
                saudacao = "Oi! "
            else:
                saudacao = "Olá! "
            resp.message(
                saudacao +
                "Bem-vindo à Pizzaria do Cleverson! 🍕\n" +
                "Confira nosso cardápio:\n" +
                "1. Pizza Margherita - R$ 30\n" +
                "2. Pizza Calabresa - R$ 35\n" +
                "3. Pizza Quatro Queijos - R$ 38\n" +
                "4. Pizza Portuguesa - R$ 40\n" +
                "Responda com o número da pizza para fazer o pedido!"
            )
        else:
            resp.message(
                f"Bem-vindo à Pizzaria do Cleverson! 🍕\nConfira nosso cardápio:\n1. Pizza Margherita - R$ 30\n2. Pizza Calabresa - R$ 35\n3. Pizza Quatro Queijos - R$ 38\n4. Pizza Portuguesa - R$ 40\nResponda com o número da pizza para fazer o pedido!"
            )
    elif etapa == "pagamento":
        forma = msg.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ç", "c").strip()
        if forma in ["pix", "dinheiro", "cartao", "cartão"]:
            conversas[numero]["pagamento"] = forma.capitalize()
            conversas[numero]["etapa"] = "endereco"
            resp.message("Por favor, informe seu endereço para entrega:")
        else:
            resp.message("Forma de pagamento inválida. Escolha: pix, débito, crédito, cartão ou dinheiro.")
    elif etapa == "endereco":
        conversas[numero]["endereco"] = msg
        pedido = conversas[numero]["pedido"]
        pagamento = conversas[numero]["pagamento"]
        endereco = conversas[numero]["endereco"]
        resp.message(
            f"Pedido confirmado!\nPizza: {pedido}\nPagamento: {pagamento}\nEndereço: {endereco}\nObrigado pela preferência!"
        )
        conversas[numero]["etapa"] = "finalizado"
    else:
        if msg.lower().strip() in ["sim", "s", "yes", "y"]:
            resp.message(
                "Aqui está o cardápio para um novo pedido:\n"
                "1. Pizza Margherita - R$ 30\n"
                "2. Pizza Calabresa - R$ 35\n"
                "3. Pizza Quatro Queijos - R$ 38\n"
                "4. Pizza Portuguesa - R$ 40\n"
                "Responda com o número da pizza para fazer o pedido!"
            )
            conversas[numero]["etapa"] = "cardapio"
        elif msg.lower().strip() in ["não", "nao", "n", "no"]:
            resp.message("Ok! Se quiser fazer outro pedido, é só mandar uma mensagem.")
        else:
            resp.message("Seu pedido já foi registrado. Deseja ver o cardápio novamente? (sim/não)")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)