from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQLalq

db = SQLalq()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

class Usuario(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))

# def __init__(self, id, nome, endereco, email, senha):
#     self.id = id
#     self.nome = nome
#     self.endereco = endereco
#     self.email = email
#     self.senha = senha

#usado pra criar o bd
with app.app_context():
    db.create_all()
    

    
    
    