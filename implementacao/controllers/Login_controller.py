from flask import Flask, render_template, request, redirect, url_for, make_response
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
import weasyprint

def verificar():
    id = request.form["id"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]
    match tipo:
        case 'aluno':
            a = Aluno.query.all()
            sm = db.session.get(Aluno, id)
            if(sm in a and senha == sm.senha):
                return redirect(url_for("aluno", u=sm.id))
            
        case 'prof':
            a = Professor.query.all()
            sm = db.session.get(Professor, id)
            if(sm in a and senha == sm.senha):
                return redirect(url_for("professor", u=sm.id))
        
        case 'parc':
            a = Parceiro.query.all()
            sm = db.session.get(Parceiro, id)
            if(sm in a and senha == sm.senha):
                return redirect(url_for("parceiro", u=sm.id))
            
        case 'admin':
            a = Administrador.query.all()
            sm = db.session.get(Administrador, id)
            if(sm in a and senha == sm.senha):
                return redirect(url_for("administrador", u=sm.id))

    return render_template("login.html") #talvez retortnar popup

def registrar():
    tipo = request.form["tipo"]
    nome = request.form["nome"]
    endereco = request.form["endereco"]
    email = request.form["email"]
    senha = request.form["senha"]
    match tipo:
        case 'aluno':
            cpf = request.form["cpf"]
            rg = request.form["rg"]
            curso = request.form["curso"]
            instituicao = request.form["instituicao"]
            cpf_existe = Aluno.query.filter_by(cpf=cpf).first()
            rg_existe = Aluno.query.filter_by(rg=rg).first()
            if(not cpf_existe and not rg_existe):
                n = Aluno(nome=nome, endereco=endereco, email=email,
                        senha=senha, tipo=tipo, cpf=cpf, rg=rg,
                        curso=curso, id_instituicao=instituicao, moedas=0)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for("aluno", u=n.id))

        case 'parceiro':            
            cnpj = request.form["cnpj"]
            cnpj_existe = Parceiro.query.filter_by(cnpj=cnpj).first()
            if(not cnpj_existe):
                n = Parceiro(nome=nome, endereco=endereco, email=email,
                            senha=senha, tipo=tipo, cnpj=cnpj)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for("parceiro", u=n.id))
    
    return redirect(url_for("registrar"))
