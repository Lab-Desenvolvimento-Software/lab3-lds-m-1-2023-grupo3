from flask import Flask, render_template, request, redirect, url_for, make_response
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
from controller import *
# from app import app
import weasyprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

def cria():
    p = Parceiro(nome="parca", endereco="rua123", email="mail", senha="123", tipo="parceiro", cnpj=123)
    c = Instituicao(nome="PUCMG")
    a = Administrador(nome="ademir", endereco="rua123", email="mail", senha="123", tipo="administrador")
    db.session.add(p)
    db.session.add(c)
    db.session.add(a)
    db.session.commit()

    prof = Professor(nome="prof", endereco="rua123", email="mail", senha="123", tipo="professor", cpf=123, departamento="ICEI", moedas=1000, id_instituicao=c.id)
    alun = Aluno(nome="alun", endereco="rua123", email="mail", senha="123", tipo="aluno", cpf=123, rg=123123, curso="curso", moedas=1000, id_instituicao=c.id)
    db.session.add(prof)
    db.session.add(alun)
    db.session.commit()

    prod = Produto(nome="produto", descricao="1 produto", preco=50, id_parceiro=p.id)
    db.session.add(prod)
    db.session.commit()

# usado pra criar o bd
with app.app_context():
    db.create_all()
    # cria()


#PROFESSOR
@app.route("/professor/<int:u>", methods=["POST", "GET"])
def professor(u):
    return Professor_controller.dados(u)

@app.route("/professor/<int:u>/<int:j>", methods=["POST", "GET"])
def mandarMoedas(u, j):
    Professor_controller.mandarMoedas(u, j)
    return redirect(url_for("professor_dados", u=u))

@app.route("/professor/<int:u>/relatorio", methods=["POST", "GET"])
def relatorioProf(u):
    return Professor_controller.relatorio(u)



# ALUNO
@app.route("/aluno/<int:u>", methods=["POST", "GET"])
def aluno(u):
    return Aluno_controller.dados(u)

@app.route("/aluno/<int:u>/<int:j>", methods=["POST", "GET"])
def compraProd(u, j):
    Aluno_controller.compraProduto(u, j)
    return redirect(url_for("aluno", u=u))

@app.route("/aluno/<int:u>/relatorio", methods=["POST", "GET"])
def relatorioAluno(u):
    return Aluno_controller.relatorio(u)


#PARCEIRO
@app.route("/parceiro/<int:u>", methods=["POST", "GET"])
def parceiro(u):
    return Parceiro_controller.dados(u)

@app.route("/parceiro/<int:u>/add", methods=["POST", "GET"])
def addProd(u):
    Parceiro_controller.addProduto(u)
    return redirect(url_for("parceiro", u=u))

@app.route("/parceiro/<int:u>/<int:j>", methods=["POST", "GET"])
def editProd(u, j):
    Parceiro_controller.editProduto(u, j)
    return redirect(url_for("parceiro", u=u))

@app.route("/parceiro/<int:u>/delete/<int:j>", methods=["POST", "GET", "REMOVE"])
def delProd(u, j):
    Parceiro_controller.delProduto(u, j)
    return redirect(url_for("parceiro", u=u))


#ADMINISTRADOR
@app.route("/administrador/<int:u>", methods=["POTS", "GET"])
def administrador(u):
    return Administrador_controller.dados(u)

@app.route("/administrador/<int:u>/<tipo>/<int:id>", methods=["POST", "GET"])
def amdEdit(u, tipo, id):
    Administrador_controller.editar(u, tipo, id)
    return redirect(url_for("administrador", u=u))

@app.route("/administrador/<int:u>/<tipo>", methods=["POST", "GET"])
def admAdd(u, tipo):
    Administrador_controller.adicionar(u, tipo)
    return redirect(url_for("administrador", u=u))

@app.route("/administrador/<int:u>/rm/<tipo>/<int:id>", methods=["POST", "GET", "REMOVE"])
def admRm(u, tipo, id):
    Administrador_controller.remover(u, tipo, id)
    return redirect(url_for("administrador", u=u))


#LOGIN/REGISTRAR
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/verifica", methods=["GET", "POST"])
def verifica():
    return Login_controller.verificar()

@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    inst = Instituicao.query.all()
    return render_template("registrar.html", inst=inst)

@app.route("/registrando", methods=["POST", "GET"])
def registrando():
    return Login_controller.registrar()


if __name__ == '__main__':
   app.run()
    