# app_factory.py
from flask import Flask
from db_models import db, Produto, Pedido
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('pizzaria.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "cleverson_super_secreto"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if Produto.query.count() == 0:
            produtos_iniciais = [
                Produto(nome="Pizza Margherita", preco=30),
                Produto(nome="Pizza Calabresa", preco=35),
                Produto(nome="Pizza Quatro Queijos", preco=38),
                Produto(nome="Pizza Portuguesa", preco=40)
            ]
            db.session.add_all(produtos_iniciais)
            db.session.commit()

    return app
