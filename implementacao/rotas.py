from flask import Flask, render_template, request, redirect, url_for, jsonify
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

@app.route("/transacoes/<int:u>", methods=["POST", "GET"])
def transacoes(u):
    if request.method == "GET":
        tp = Transacao.query.filter_by(destino=u).all()
        tf = Transacao.query.filter_by(origem=u).all()
        def user(usr):
            usuario = db.session.get(Usuario, usr)
            return usuario

        res = jsonify({
            "transacoes_recebidas": [{
                "id": t.id,
                "origem": user(t.origem).nome,
                "tipo": user(t.origem).tipo,
                "valor": t.valor,
                "data": t.data,
                "mensagem": t.mensagem
            } for t in tp],
            "transacoes_enviadas": [{
                "id": t.id,
                "destino": user(t.destino).nome,
                "tipo": user(t.origem).tipo,
                "valor": t.valor,
                "data": t.data,
                "mensagem": t.mensagem
            } for t in tf],
        })
        res.headers.add("Content-Type", "application/json")
        return res

@app.route("/aluno/<int:u>", methods=["POST", "GET"])
def aluno(u):
    if request.method == "GET":
        aluno = db.session.get(Aluno, u)
        inst = db.session.get(Instituicao, aluno.id_instituicao)
        # tp = Transacao.query.filter_by(destino=u).all()
        # tf = Transacao.query.filter_by(origem=u).all()
        # prof = Professor.query.all()
        prod = Produto.query.all()
        # transacoes = transacoes(u)
        res = jsonify({
            "aluno": {
                "id": aluno.id,
                "nome": aluno.nome,
                "endereco": aluno.endereco,
                "email": aluno.email,
                "senha": aluno.senha,
                "tipo": aluno.tipo,
                "cpf": aluno.cpf,
                "rg": aluno.rg,
                "curso": aluno.curso,
                "moedas": aluno.moedas
            },
            "instituicao": {
                "id": inst.id,
                "nome": inst.nome
            },
            "produtos": [{
                "id": p.id,
                "nome": p.nome,
                "descricao": p.descricao,
                "preco": p.preco
            } for p in prod],
        })
        res.headers.add("Content-Type", "application/json")
        return res

@app.route("/aluno/<int:u>/compra/<int:prod>", methods=["GET", "POST"])
def compra_prod(u, prod):
    if request.method == "POST":
        aluno = db.session.get(Aluno, u)
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado."}), 404
        
        produto = db.session.get(Produto, prod)
        if produto is None:
            return jsonify({"error": "Produto não encontrado."}), 404

        if aluno.moedas < produto.preco:
            return jsonify({"error": "saldo insuficiente"}), 400

        transacao = Transacao(
            origem=aluno.id,
            destino=prod.id,
            valor=produto.preco,
            data=datetime.now(),
            mensagem=f"Compra do produto: {produto.nome}"
        )
        db.session.add(transacao)
        aluno.moedas -= produto.preco
        db.session.commit()

        return jsonify({"success": True, "message": "Compra realizada com sucesso!"}), 200


# @app.route("transacao/<int:origem>/<int:destino>", methods=["POST, GET"])
# def transacao(origem, destino):
    
#     return res

if __name__ == '__main__':
   app.run()