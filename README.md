# Pizzaria WhatsApp Bot

Este projeto é uma aplicação web desenvolvida com Flask para automatizar pedidos de pizza via WhatsApp, utilizando a API do Twilio. O sistema permite que clientes façam pedidos, recebam confirmações e interajam com o bot de forma simples e rápida.

## Funcionalidades
- Recebimento de pedidos via WhatsApp
- Resposta automática e conversacional
- Integração com banco de dados usando SQLAlchemy
- Interface web para acompanhamento dos pedidos
- Modularização do código para facilitar manutenção
- Proteção de credenciais sensíveis (Twilio)

## Estrutura do Projeto
```
app.py                # App principal Flask, rotas e lógica de negócio
app_factory.py        # Criação da aplicação e inicialização do banco
whatsapp_twilio.py    # Integração com Twilio para envio de mensagens
config_twilio.py      # Credenciais do Twilio (não versionado)
db_models.py          # Modelos do banco de dados
index.html            # Página principal
script.js             # Scripts JS da interface
style.css             # Estilos da interface
requirements.txt      # Dependências do projeto
Procfile              # Comando de inicialização para deploy
.gitignore            # Arquivos/pastas ignorados pelo Git
```

## Como rodar localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure suas credenciais Twilio em `config_twilio.py` (não suba este arquivo para o GitHub).
3. Execute o app Flask:
   ```bash
   python app.py
   ```
4. Para testes com WhatsApp, use o sandbox do Twilio e configure o webhook.

## Deploy
- O deploy pode ser feito facilmente no Render ou Heroku.
- O arquivo `Procfile` já está configurado para uso com Gunicorn:
  ```
  web: gunicorn app:app
  ```

## Observações
- O arquivo `config_twilio.py` está listado no `.gitignore` para proteger suas credenciais.
- O sandbox do Twilio possui limite de mensagens por dia.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
