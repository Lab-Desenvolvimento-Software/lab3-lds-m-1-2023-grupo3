from flask import Flask, render_template, request, redirect, url_for
from model import Usuario, Aluno, Professor,  Parceiro, Administrador, Instituicao, Produto, Transacao, db
from datetime import datetime
from controller import *

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

    prod = Produto(nome="replho", descricao="1(uma) undade de repolho", preco=50, id_parceiro=p.id)
    db.session.add(prod)
    db.session.commit()



#usado pra criar o bd
with app.app_context():
    db.create_all()
    # cria()
    email("vayeg74730@glumark.com", "repolho")

#PROFESSOR
@app.route("/professor/<int:u>", methods=["POST", "GET"])
def professor(u):
    prof = db.session.get(Professor, u) 
    inst = db.session.get(Instituicao, prof.id_instituicao)
    tp = Transacao.query.filter_by(origem=u).all()
    # tr = Transacao.query.filter_by(destino=u).all()
    aluno = Aluno.query.all()
    al_nomes = {}
    for a in Aluno.query.all():
        al_nomes[a.id_aluno] = a.nome
    return render_template("/professor.html", aluno=aluno, inst=inst, tp=tp, prof=prof, al_nomes=al_nomes)

@app.route("/professor/<int:u>/<int:j>", methods=["POST", "GET"])
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
        db.session.commit()
        #emaill pro aluno
    return redirect(url_for("professor", u=u))


# ALUNO
@app.route("/aluno/<int:u>", methods=["POST", "GET"])
def aluno(u):
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

@app.route("/aluno/<int:u>/<int:j>", methods=["POST", "GET"])
def compraProd(u, j):
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
        # emaill parceiro c/ codigo de identificação
    return redirect(url_for("aluno", u=u))


#PARCEIRO
@app.route("/parceiro/<int:u>", methods=["POST", "GET"])
def parceiro(u):
    parca = db.session.get(Parceiro, u)
    prod = Produto.query.filter_by(id_parceiro=u).all()
    ta = Transacao.query.filter_by(destino=u).all()
    return render_template("/parceiro.html", parca=parca, prod=prod, ta=ta)

@app.route("/parceiro/<int:u>/add", methods=["POST", "GET"])
def addProd(u):
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
    return redirect(url_for("parceiro", u=u))

@app.route("/parceiro/<int:u>/<int:j>", methods=["POST", "GET"])
def editProd(u, j):
    prod = db.session.get(Produto, j)
    prod.nome=request.form["nome"]
    prod.descricao=request.form["descricao"]
    prod.preco=request.form["preco"]
    db.session.commit()
    return redirect(url_for("parceiro", u=u))

@app.route("/parceiro/<int:u>/delete/<int:j>", methods=["POST", "GET", "REMOVE"])
def delProd(u, j):
    prod = db.session.get(Produto, j)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for("parceiro", u=u))


#ADMINISTRADOR
@app.route("/administrador/<int:u>", methods=["POTS", "GET"])
def administrador(u):
    adm = db.session.get(Administrador, u)
    adms = Administrador.query.all()
    parca = Parceiro.query.all()
    prof = Professor.query.all()
    inst = Instituicao.query.all()
    dict_inst = {ins.id: ins for ins in inst}
    aluno = Aluno.query.all()
    return render_template("administrador.html", adm=adm, adms=adms, parca=parca, prof=prof, inst=inst, dict_inst=dict_inst, aluno=aluno)

@app.route("/administrador/<int:u>/<tipo>/<int:id>", methods=["POST", "GET"])
def amdEdit(u, tipo, id):
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

    return redirect(url_for("administrador", u=u))

@app.route("/administrador/<int:u>/<tipo>", methods=["POST", "GET"])
def admAdd(u, tipo):
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

    return redirect(url_for("administrador", u=u))

@app.route("/administrador/<int:u>/rm/<tipo>/<int:id>", methods=["POST", "GET", "REMOVE"])
def admRm(u, tipo, id):
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

    return redirect(url_for("administrador", u=u))

#LOGIN/REGISTRAR
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/verifica", methods=["GET", "POST"])
def verifica():
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

    return login() #talvez retortnar popup

@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    inst = Instituicao.query.all()
    return render_template("registrar.html", inst=inst)

@app.route("/registrando", methods=["POST", "GET"])
def registrando():
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


if __name__ == '__main__':
   app.run()
    