from flask import Flask, render_template, request, redirect, url_for, jsonify
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

@app.route("/aluno/<int:u>", methods=["POST", "GET"])
def aluno(u):
    if request.method == "GET":
        aluno = db.session.get(Aluno, u)
        inst = db.session.get(Instituicao, aluno.id_instituicao)
        tp = Transacao.query.filter_by(destino=u).all()
        tf = Transacao.query.filter_by(origem=u)
        prof = Professor.query.all()
        prod = Produto.query.all()
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
            "transacoes_recebidas": [{
                "id": t.id,
                "origem": t.origem,
                "destino": t.destino,
                "valor": t.valor,
                "data": t.data,
                "mensagem": t.mensagem
            } for t in tp],
            "transacoes_enviadas": [{
                "id": t.id,
                "origem": t.origem,
                "destino": t.destino,
                "valor": t.valor,
                "data": t.data,
                "mensagem": t.mensagem
            } for t in tf],
            "professores": [{
                "id": p.id,
                "nome": p.nome,
                "endereco": p.endereco,
                "email": p.email,
                "senha": p.senha,
                "tipo": p.tipo,
                "cpf": p.cpf,
                "departamento": p.departamento,
                "moedas": p.moedas
            } for p in prof],
            "produtos": [{
                "id": p.id,
                "nome": p.nome,
                "descricao": p.descricao,
                "preco": p.preco
            } for p in prod]
        })
        res.headers.add("Content-Type", "application/json")
        return res
    # elif request.method == "POST":
        # lógica para criar um novo aluno


if __name__ == '__main__':
   app.run()
    