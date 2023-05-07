from flask import Flask, render_template, request
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

def tes():
    pa = Parceiro(nome="parceiro", endereco="rua 123", email="email", senha="senha123", cnpj=123654)
    db.session.add(pa)

    db.session.commit()

    pr = Produto(nome="coisa", descricao="uma coisa", preco=50, id_parceiro=pa.id)
    db.session.add(pr)

    pr = Produto(nome="pão", descricao="um pão", preco=100, id_parceiro=pa.id)
    db.session.add(pr)
    
    db.session.commit()


def relacoes():
    inst = Instituicao(nome="PUCMG")
    db.session.add(inst)
    db.session.commit()

    #instituicao + profs e alunos
    profA = Professor(nome="prof1", endereco="rua123", email="mail", senha="123", cpf=123, id_instituicao=inst.id)
    profB = Professor(nome="prof2", endereco="rua123", email="mail", senha="123", cpf=123, id_instituicao=inst.id)
    alunA = Aluno(nome="aluno1", endereco="rua123", email="mail", senha="123", cpf=123, rg=123, curso="curso", id_instituicao=inst.id)
    alunB = Aluno(nome="aluno2", endereco="rua123", email="mail", senha="123", cpf=123, rg=123, curso="curso", id_instituicao=inst.id)
    parca = Parceiro(nome="parceiro", endereco="rua 123", email="email", senha="senha123", cnpj=123654)
    db.session.add_all([profA, profB, alunA, alunB, parca])
    db.session.commit()

    #enviar moedas alunos
def enviaMoedaAluno():
    profA = Professor.query.filter_by(nome="prof1").first()
    alunA = Aluno.query.filter_by(nome="aluno1").first()
    
    transacao = TransacaoProfessor(origem=profA.id, destino=alunA.id, valor=40, data="12/05/2000", mensagem="mensg")
    db.session.add(transacao)
    db.session.commit()

    #enviar moedas parceiros
def enviaMoedaparca():
    
    db.session.commit()

def ktAdm():
    adm = Administrador(nome="ademir", endereco="123", email="mail", senha="123")
    db.session.add(adm)
    db.session.commit()

#rotas/cotroller
@app.route("/")
def barra():
    return "asd"

@app.route("/tes")
def testao():
    #tes()
    #return "teste!!!"
    
    #relacoes()
    #enviaMoedaAluno()
    #tes()
    profs = Professor.query.all()
    aluns = Aluno.query.all()
    inst = Instituicao.query.all()
    tprof = TransacaoProfessor.query.all()
    return render_template("/dash.html", profs=profs, aluns=aluns, inst=inst, tprof=tprof)


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
    tr = TransacaoProfessor(origem=u, destino=aluno.id, valor=request.form["valor"], data=datetime.now(), mensagem=request.form["mensagem"])
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
    tr = TransacaoAluno(origem=u, destino=prod.id_parceiro, valor=prod.preco, data="0/0/0", mensagem="msg")
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
    prod = Produto(nome=request.form["nome"], descricao=request.form["descricao"], preco=request.form["preco"], id_parceiro=u)
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

#ADMINISTRADOR
@app.route("/administrador/<int:u>", methods=["POTS", "GET"])
def adm(u):
    adm = db.session.get(Administrador, u)
    adms = Administrador.query.all()
    parca = Parceiro.query.all()
    prof = Professor.query.all()
    inst = Instituicao.query.all()
    aluno = Aluno.query.all()
    return render_template("administrador.html", adm=adm, adms=adms, parca=parca, prof=prof, inst=inst, aluno=aluno)



@app.route("/listaParceiros", methods=["POST","GET"])
def mostraParceiros():
    #users = db.session.execute(db.select(Usuario).order_by(Usuario.nome)).scalars()
    #if request.method == "REMOVE":
    #    db.session.delete(request.form)
    #    db.session.commit()
    users = Parceiro.query.all()
    produtos = Produto.query.all()
    return render_template("/listaParceiros.html", users=users, produtos=produtos)

@app.route("/listaParceiros/<int:u>", methods=["REMOVE", "GET"])
def deleteParceiro(u):
    p = Parceiro.query.get(u)
    db.session.delete(p)
    db.session.commit()
    return render_template("/listaParceiros.html")

@app.route("/editParceiro/<int:u>", methods=["POST", "GET"])
def editParceiro(u):
    p = Parceiro.query.get(u)
    if request.method == "POST":
        
        user = Parceiro(
            nome = request.form["nome"],
            endereco = request.form["endereco"],
            email = request.form["email"],
            senha = request.form["senha"],
            cnpj = request.form["cnpj"]
        )
        db.session.add(user)
        db.session.commit()
    return render_template("/listaParceiros.html")
    
@app.route("/criaParceiro", methods=["POST", "GET"])
def criaParceiro():
    if request.method == "POST":
        user = Parceiro(
            nome = request.form["nome"],
            endereco = request.form["endereco"],
            email = request.form["email"],
            senha = request.form["senha"],
            cnpj = request.form["cnpj"]
        )
        db.session.add(user)
        db.session.commit()
    return render_template("/criaParceiro.html")


@app.route("/listaAlunos", methods=["POST","GET"])
def mostraAlunos():
    
    users = Aluno.query.all()
    return render_template("/listaAlunos.html", users=users)

@app.route("/listaAlunos/<int:u>", methods=["REMOVE", "GET"])
def deleteAluno(u):
    p = Aluno.query.get(u)
    db.session.delete(p)
    db.session.commit()
    return render_template("/listaAlunos.html")
    

@app.route("/criaAluno", methods=["POST", "GET"])
def criaAluno():
    if request.method == "POST":
        user = Aluno(
            nome = request.form["nome"],
            endereco = request.form["endereco"],
            email = request.form["email"],
            senha = request.form["senha"],
            cpf = request.form["cpf"],
            rg = request.form["rg"],
            curso = request.form["curso"],
            instDeEnsino = request.form["instDeEnsino"],
            moedas = 0
        )
        db.session.add(user)
        db.session.commit()
    return render_template("/criaAluno.html")



if __name__ == '__main__':
   app.run()
   #db.create_all()
    
    