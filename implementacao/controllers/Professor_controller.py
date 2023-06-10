from flask import Flask, render_template, request, redirect, url_for, make_response
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
import weasyprint

def dados(u):
    prof = db.session.get(Professor, u) 
    inst = db.session.get(Instituicao, prof.id_instituicao)
    tp = Transacao.query.filter_by(origem=u).all()
    # tr = Transacao.query.filter_by(destino=u).all()
    aluno = Aluno.query.all()
    al_nomes = {}
    for a in Aluno.query.all():
        al_nomes[a.id_aluno] = a.nome
    return render_template("/professor.html", aluno=aluno, inst=inst, tp=tp, prof=prof, al_nomes=al_nomes)

def mandarMoedas(u, j):
    aluno = db.session.get(Aluno, j)
    prof = db.session.get(Professor, u)
    if prof.moedas >= int(request.form["valor"]):
        tr = Transacao(origem=u, 
                       destino=aluno.id, 
                       valor=request.form["valor"], 
                       data=datetime.now(), 
                       mensagem=request.form["mensagem"])
        db.session.add(tr)
        prof.moedas -= int(request.form["valor"])
        aluno.moedas += int(request.form["valor"])
        db.session.commit()
        #emaill pro aluno
    # return redirect(url_for("professor_dados", u=u))

def relatorio(u):
    prof = db.session.get(Professor, u) 
    inst = db.session.get(Instituicao, prof.id_instituicao)
    tp = Transacao.query.filter_by(origem=u).all()
    aluno = Aluno.query.all()
    al_nomes = {}
    for a in Aluno.query.all():
        al_nomes[a.id_aluno] = a.nome

    html = render_template("/relatorioProf.html", prof=prof, tp=tp, aluno=aluno, al_nomes=al_nomes, inst=inst)
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorioProf.pdf'
    return response
