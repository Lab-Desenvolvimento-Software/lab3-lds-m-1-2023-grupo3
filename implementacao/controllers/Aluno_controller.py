from flask import Flask, render_template, request, redirect, url_for, make_response
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
import weasyprint

def dados(u):
    aluno = db.session.get(Aluno, u) #= Aluno.query.get(...)
    inst = db.session.get(Instituicao, aluno.id_instituicao)
    tp = Transacao.query.filter_by(destino=u).all()
    tf = Transacao.query.filter_by(origem=u)
    prof = Professor.query.all()
    prod = Produto.query.all()
    pf_nomes = {}
    for p in Professor.query.all():
        pf_nomes[p.id_professor] = p.nome
    pr_nomes = {}
    for pr in Parceiro.query.all():
        pr_nomes[pr.id_parceiro] = pr.nome
    return render_template("/aluno.html", aluno=aluno, inst=inst, tp=tp, tf=tf, prod=prod, prof=prof, pf_nomes=pf_nomes, pr_nomes=pr_nomes)

def compraProduto(u, j):
    aln = db.session.get(Aluno, u)
    prod = db.session.get(Produto, j)
    if aln.moedas >= prod.preco:
        msg = prod.nome + " comprado!"
        tn = Transacao(origem=u, 
                        destino=prod.id_parceiro, 
                        valor=prod.preco, 
                        data=datetime.now(),
                        mensagem=msg)
        db.session.add(tn)
        alun = db.session.get(Aluno, u)
        alun.moedas -= prod.preco
        db.session.commit()

def relatorio(u):
    aluno = db.session.get(Aluno, u) #= Aluno.query.get(...)
    inst = db.session.get(Instituicao, aluno.id_instituicao)
    tp = Transacao.query.filter_by(destino=u).all()
    tf = Transacao.query.filter_by(origem=u)
    prof = Professor.query.all()
    prod = Produto.query.all()
    pf_nomes = {}
    for p in Professor.query.all():
        pf_nomes[p.id_professor] = p.nome
    pr_nomes = {}
    for pr in Parceiro.query.all():
        pr_nomes[pr.id_parceiro] = pr.nome

    html = render_template("/relatorioAluno.html", aluno=aluno, inst=inst, tp=tp, tf=tf, prod=prod, prof=prof, pf_nomes=pf_nomes, pr_nomes=pr_nomes)
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorioAluno.pdf'
    return response