from flask import render_template, request
from model import Parceiro, Produto, Transacao, db

def dados(u):
    parca = db.session.get(Parceiro, u)
    prod = Produto.query.filter_by(id_parceiro=u).all()
    ta = Transacao.query.filter_by(destino=u).all()
    return render_template("/parceiro.html", parca=parca, prod=prod, ta=ta)

def addProduto(u):
    prod = Produto(nome=request.form["nome"], 
               descricao=request.form["descricao"], 
               preco=request.form["preco"], 
               id_parceiro=u)
    arq = request.files.get("img")
    if arq:
        arq.save(f"static/imgProdutos/{arq.filename}")
        prod.img = arq.filename
        
    db.session.add(prod)
    db.session.commit()

def editProduto(u, j):
    prod = db.session.get(Produto, j)
    prod.nome=request.form["nome"]
    prod.descricao=request.form["descricao"]
    prod.preco=request.form["preco"]
    db.session.commit()

def delProduto(u, j):
    prod = db.session.get(Produto, j)
    db.session.delete(prod)
    db.session.commit()