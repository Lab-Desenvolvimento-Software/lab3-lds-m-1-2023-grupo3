from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy as SQLalq
from datetime import datetime

#model
db = SQLalq()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

class Aluno(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cpf = db.Column(db.Integer) 
    rg = db.Column(db.Integer)
    curso = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))
    transacoesAluno = db.relationship("TransacaoAluno", backref="aluno")
    transacoesProf = db.relationship("TransacaoProfessor", backref="aluno")

class Professor(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cpf = db.Column(db.Integer)  
    departamento = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))
    transacoesProf = db.relationship("TransacaoProfessor", backref="professor")
    transacoesAluno = db.relationship("TransacaoAluno", backref="professor")

class Parceiro(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cnpj = db.Column(db.Integer)
    produtos = db.relationship("Produto", backref="parceiro", lazy=True)#um parceiro tem vários produtos

class Administrador(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))


class Instituicao(db.Model):
    id = db.Column("id_instituicao", db.Integer, primary_key=True)
    nome = db.Column(db.String(40))
    professores = db.relationship("Professor", backref="instituicao")
    alunos = db.relationship("Aluno", backref="instituicao")

class Produto(db.Model):
    id = db.Column("id_produto", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(320))
    preco = db.Column(db.Integer)
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro.id_usuario")) #relação
    
    
class TransacaoProfessor(db.Model):
    id = db.Column("id_transacao_prof", db.Integer, primary_key=True)
    origem = db.Column(db.Integer, db.ForeignKey("professor.id_usuario")) #sempre professor
    destino = db.Column(db.Integer, db.ForeignKey("aluno.id_usuario")) #sempre aluno
    valor = db.Column(db.Integer)
    data = db.Column(db.String(20))
    mensagem = db.Column(db.String(100))

class TransacaoAluno(db.Model):
    id = db.Column("id_transacao_aluno", db.Integer, primary_key=True)
    origem = db.Column(db.Integer, db.ForeignKey("aluno.id_usuario"))#sempre aluno
    destino = db.Column(db.Integer, db.ForeignKey("professor.id_usuario"))#sempre parceiro 
    valor = db.Column(db.Integer)
    data = db.Column(db.String(20))
    mensagem = db.Column(db.String(100))

#usado pra criar o bd
with app.app_context():
    db.create_all()

# def tes():
#     pa = Parceiro(nome="parceiro", endereco="rua 123", email="email", senha="senha123", cnpj=123654)
#     db.session.add(pa)

#     db.session.commit()

#     pr = Produto(nome="coisa", descricao="uma coisa", preco=50, id_parceiro=pa.id)
#     db.session.add(pr)

#     pr = Produto(nome="pão", descricao="um pão", preco=100, id_parceiro=pa.id)
#     db.session.add(pr)
    
#     db.session.commit()


# def relacoes():
#     inst = Instituicao(nome="PUCMG")
#     db.session.add(inst)
#     db.session.commit()

#     #instituicao + profs e alunos
#     profA = Professor(nome="prof1", endereco="rua123", email="mail", senha="123", cpf=123, id_instituicao=inst.id)
#     profB = Professor(nome="prof2", endereco="rua123", email="mail", senha="123", cpf=123, id_instituicao=inst.id)
#     alunA = Aluno(nome="aluno1", endereco="rua123", email="mail", senha="123", cpf=123, rg=123, curso="curso", id_instituicao=inst.id)
#     alunB = Aluno(nome="aluno2", endereco="rua123", email="mail", senha="123", cpf=123, rg=123, curso="curso", id_instituicao=inst.id)
#     parca = Parceiro(nome="parceiro", endereco="rua 123", email="email", senha="senha123", cnpj=123654)
#     db.session.add_all([profA, profB, alunA, alunB, parca])
#     db.session.commit()

#     #enviar moedas alunos
# def enviaMoedaAluno():
#     profA = Professor.query.filter_by(nome="prof1").first()
#     alunA = Aluno.query.filter_by(nome="aluno1").first()
    
#     transacao = TransacaoProfessor(origem=profA.id, destino=alunA.id, valor=40, data="12/05/2000", mensagem="mensg")
#     db.session.add(transacao)
#     db.session.commit()

#     #enviar moedas parceiros
# def enviaMoedaparca():
    
#     db.session.commit()

# def ktAdm():
#     adm = Administrador(nome="ademir", endereco="123", email="mail", senha="123")
#     db.session.add(adm)
#     db.session.commit()

# #rotas/cotroller
# @app.route("/")
# def barra():
#     return "asd"

# @app.route("/tes")
# def testao():
#     #tes()
#     #return "teste!!!"
    
#     #relacoes()
#     #enviaMoedaAluno()
#     #tes()
#     profs = Professor.query.all()
#     aluns = Aluno.query.all()
#     inst = Instituicao.query.all()
#     tprof = TransacaoProfessor.query.all()
#     return render_template("/dash.html", profs=profs, aluns=aluns, inst=inst, tprof=tprof)


#PROFESSOR
@app.route("/professor/<int:u>", methods=["POST", "GET"])
def professor(u):
    prof = db.session.get(Professor, u) 
    inst = db.session.get(Instituicao, prof.id_instituicao)
    tp = TransacaoProfessor.query.filter_by(origem=u).all()
    aluno = Aluno.query.all()
    return render_template("/professor.html", aluno=aluno, inst=inst, tp=tp, prof=prof)

@app.route("/professor/<int:u>/<int:j>", methods=["POST", "GET"])
def mandarMoedas(u, j):
    aluno = db.session.get(Aluno, j)
    tr = TransacaoProfessor(origem=u, 
                            destino=aluno.id, 
                            valor=request.form["valor"], 
                            data=datetime.now(), 
                            mensagem=request.form["mensagem"])
    db.session.add(tr)
    db.session.commit()
    return professor(u)

# ALUNO
@app.route("/aluno/<int:u>", methods=["POST", "GET"])
def aluno(u):
    aluno = db.session.get(Aluno, u) #= Aluno.query.get(...)
    inst = db.session.get(Instituicao, aluno.id_instituicao)
    tp = TransacaoProfessor.query.filter_by(destino=u).all()
    ta = TransacaoAluno.query.filter_by(origem=u).all()
    prof = Professor.query.all()
    prod = Produto.query.all()
    return render_template("/aluno.html", aluno=aluno, inst=inst, tp=tp, ta=ta, prod=prod, prof=prof)

@app.route("/aluno/<int:u>/<int:j>", methods=["POST", "GET"])
def compraProd(u, j):
    prod = db.session.get(Produto, j)
    tr = TransacaoAluno(origem=u, 
                        destino=prod.id_parceiro, 
                        valor=prod.preco, 
                        data="0/0/0", 
                        mensagem="msg")
    db.session.add(tr)
    db.session.commit()
    return aluno(u)

#PARCEIRO
@app.route("/parceiro/<int:u>", methods=["POST", "GET"])
def parceiro(u):
    parca = db.session.get(Parceiro, u)
    prod = Produto.query.filter_by(id_parceiro=u).all()
    ta = TransacaoAluno.query.filter_by(destino=u).all()
    return render_template("/parceiro.html", parca=parca, prod=prod, ta=ta)

@app.route("/parceiro/<int:u>/add", methods=["POST", "GET"])
def addProd(u):
    prod = Produto(nome=request.form["nome"], 
                   descricao=request.form["descricao"], 
                   preco=request.form["preco"], 
                   id_parceiro=u)
    db.session.add(prod)
    db.session.commit()
    return parceiro(u)

@app.route("/parceiro/<int:u>/<int:j>", methods=["POST", "GET"])
def editProd(u, j):
    prod = db.session.get(Produto, j)
    prod.nome=request.form["nome"]
    prod.descricao=request.form["descricao"]
    prod.preco=request.form["preco"]
    db.session.commit()
    return parceiro(u)

@app.route("/parceiro/<int:u>/delete/<int:j>", methods=["POST", "GET", "REMOVE"])
def delProd(u, j):
    prod = db.session.get(Produto, j)
    db.session.delete(prod)
    db.session.commit
    return parceiro(u)

#ADMINISTRADOR
@app.route("/administrador/<int:u>", methods=["POTS", "GET"])
def administrador(u):
    adm = db.session.get(Administrador, u)
    adms = Administrador.query.all()
    parca = Parceiro.query.all()
    prof = Professor.query.all()
    inst = Instituicao.query.all()
    aluno = Aluno.query.all()
    return render_template("administrador.html", adm=adm, adms=adms, parca=parca, prof=prof, inst=inst, aluno=aluno)

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

    return administrador(u)

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

        case 'adm':
            admin = Administrador(nome=request.form["nome"],
                                  endereco=request.form["endereco"], 
                                  email=request.form["email"], 
                                  senha=request.form["senha"])
            db.session.add(admin)
            db.session.commit()

    return administrador(u)

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

    return administrador(u)

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

    return login()

@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    inst = Instituicao.query.all()
    return render_template("registrar.html", inst=inst)

@app.route("/registrando", methods=["POST", "GET"])
def registrando():
    tipo = request.form["tipo"]
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    match tipo:
        case 'aluno':
            cpf = request.form["cpf"]
            rg = request.form["rg"]
            curso = request.form["curso"]
            instituicao = request.form["instituicao"]
            # cpfs = Aluno.query(cpf).all()
            # rgs = Aluno.query(rg).all()
            cpfs = [x.cpf for x in db.session.query(Aluno)]
            rgs = [x.rg for x in db.session.query(Aluno)]
            if not (rg in rgs or cpf in cpfs):
                n = Aluno(nome=nome, mail=email, senha=senha, 
                          cpf=cpf, curso=curso, instituicao=instituicao, 
                          rg=rg, moedas=0)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for("aluno", u=n.id))

        case 'parca':            
            cnpj = request.form["cnpj"]
            cnpjs = Parceiro.query(cnpj).all()
            if(cnpj not in cnpjs):
                n = Parceiro(nome=nome, mail=email, senha=senha, cnpj=cnpj)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for("parceiro", u=n.id))
    
    return redirect(url_for("registrar"))


if __name__ == '__main__':
   app.run()
   #db.create_all()
    
    