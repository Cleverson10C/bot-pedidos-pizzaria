# db_models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itens = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default="Recebido")
    endereco = db.Column(db.String(200))
    pagamento = db.Column(db.String(50))
