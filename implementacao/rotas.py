from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy as SQLalq
# from model import Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, TransacaoProfessor, TransacaoAluno, db
from model import Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime

# db = SQLalq()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

#usado pra criar o bd
with app.app_context():
    db.create_all()



if __name__ == '__main__':
   app.run()
   db.create_all()
    