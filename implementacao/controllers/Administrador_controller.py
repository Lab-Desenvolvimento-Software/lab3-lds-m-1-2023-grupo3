from flask import Flask, render_template, request, redirect, url_for, make_response
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
import weasyprint

def dados(u):
        adm = db.session.get(Administrador, u)
        adms = Administrador.query.all()
        parca = Parceiro.query.all()
        prof = Professor.query.all()
        inst = Instituicao.query.all()
        dict_inst = {ins.id: ins for ins in inst}
        aluno = Aluno.query.all()
        return render_template("administrador.html", adm=adm, adms=adms, parca=parca, prof=prof, inst=inst, dict_inst=dict_inst, aluno=aluno)

def editar(u, tipo, id):
    match tipo:
        case 'aluno':
            alun = db.session.get(Aluno, id)
            alun.nome = request.form["nome"]
            alun.endereco = request.form["endereco"]
            alun.email = request.form["email"]
            alun.senha = request.form["senha"]
            alun.cpf = request.form["cpf"]
            alun.rg = request.form["rg"]
            alun.curso = request.form["curso"]
            alun.instituicao = db.session.get(Instituicao, request.form["instituicao"])
            alun.moedas = request.form["moedas"]
            db.session.commit()

        case 'prof':
            prof = db.session.get(Professor, id)
            prof.nome = request.form["nome"]
            prof.endereco = request.form["endereco"]
            prof.email = request.form["email"]
            prof.senha = request.form["senha"]
            prof.cpf = request.form["cpf"]
            prof.departamento = request.form["departamento"]
            prof.instituicao = db.session.get(Instituicao, request.form["instituicao"])
            prof.moedas = request.form["moedas"]
            db.session.commit()

        case 'parc':
            parca = db.session.get(Parceiro, id)
            parca.nome = request.form["nome"]
            parca.endereco = request.form["endereco"]
            parca.email = request.form["email"]
            parca.senha = request.form["senha"]
            parca.cnpj = request.form["cnpj"]
            db.session.commit()

        case 'inst':
            inst = db.session.get(Instituicao, id)
            inst.nome = request.form["nome"]
            db.session.commit()

        case 'adim':
            adim = db.session.get(Administrador, id)
            adim.nome = request.form["nome"]
            adim.endereco = request.form["endereco"]
            adim.email = request.form["email"]
            adim.senha = request.form["senha"]
            db.session.commit()

def adicionar(u, tipo):
    match tipo: 
        case 'prof':
            prof = Professor(nome=request.form["nome"],
                            endereco=request.form["endereco"], 
                            senha=request.form["senha"],
                            email=request.form["email"], 
                            cpf=request.form["cpf"], 
                            departamento=request.form["departamento"],
                            instituicao=db.session.get(Instituicao, request.form["instituicao"]),
                            moedas=0)
            db.session.add(prof)
            db.session.commit()
    
        case 'inst':
            inst = Instituicao(nome=request.form["nome"])
            db.session.add(inst)
            db.session.commit()

        case 'adim':
            admin = Administrador(nome=request.form["nome"],
                                endereco=request.form["endereco"], 
                                email=request.form["email"], 
                                senha=request.form["senha"])
            db.session.add(admin)
            db.session.commit()

def remover(u, tipo, id):
    match tipo:
        case 'aluno':
            al = db.session.get(Aluno, id)
            db.session.delete(al)
            db.session.commit()

        case 'prof':
            prof = db.session.get(Professor, id)
            db.session.delete(prof)
            db.session.commit()
    
        case 'parc':
            parc = db.session.get(Parceiro, id)
            db.session.delete(parc)
            db.session.commit()
        
        case 'adim':
            adim = db.session.get(Administrador, id)
            db.session.delete(adim)
            db.session.commit()