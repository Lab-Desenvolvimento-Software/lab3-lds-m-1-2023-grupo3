from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy as SQLalq

#model
db = SQLalq()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

class Usuario(db.Model): #abstract
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))

class Aluno(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cpf = db.Column(db.Integer) 
    rg = db.Column(db.Integer)
    curso = db.Column(db.String(40))
    instDeEnsino = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    #transacoes = db.relationship("Transacao", backref="usuario")

class Professor(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cpf = db.Column(db.Integer)  
    departamento = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    #transacoes = db.relationship("Transacao", backref="usuario")

class Parceiro(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    cnpj = db.Column(db.Integer)
    produtos = db.relationship("Produto", backref="parceiro")#um parceiro tem vários produtos

class Administrador(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))


class Instituicao(db.Model):
    id = db.Column("id_instituicao", db.Integer, primary_key=True)
    #pessoas = db.relationship("Usuario", backref="usuario") #uma instituição tem varios usuarios(prof e alunos) TODO

class Produto(db.Model):
    id = db.Column("id_produto", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(320))
    preco = db.Column(db.Integer)
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro.id_usuario")) #relação
    
    
class Transacao(db.Model):
    id = db.Column("id_transacao", db.Integer, primary_key=True)
    #origem = db.relationship("Usuario", backref="usuario")
    #destino = db.relationship("Usuario"
    #origem = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    #destino = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    valor = db.Column(db.Integer)
    data = db.Column(db.String(20))
    mensagem = db.Column(db.String(100))


#usado pra criar o bd
with app.app_context():
    db.create_all()

def tes():
    pa = Parceiro(nome="parceiro", endereco="rua 123", email="email", senha="senha123", cnpj=123654)
    db.session.add(pa)

    pr = Produto(nome="coisa", descricao="uma coisa", preco=50, id_parceiro=pa.id)
    db.session.add(pr)

    pr = Produto(nome="pão", descricao="um pão", preco=100, id_parceiro=pa.id)
    db.session.add(pr)
    
    db.session.commit()

  
#rotas/cotroller
@app.route("/")
def lol():
    return "asd"

@app.route("/cham")
def cham():
    #tes()
    
    # cham = db.session.execute(db.select(Parceiro).order_by(Parceiro.nome)).scalars()
    # prod = db.session.execute(db.select(Produto).order_by(Produto.nome)).scalars()
    
    # return render_template("/cham.html", users=cham, produtos=prod)
    parceiros = Parceiro.query.all()
    produtos = Produto.query.all()
    return render_template("/cham.html", users=parceiros, prods=produtos)

@app.route("/mostraUser")
def mostra():
    users = db.session.execute(db.select(Usuario).order_by(Usuario.nome)).scalars()
    return render_template("/mostraUser.html", users=users)

@app.route("/criaUser", methods=["GET", "POST"])
def cria():
    if request.method == "POST":
        user = Usuario(
            nome=request.form["nome"],
            endereco=request.form["endereco"],
            email=request.form["email"],
            senha=request.form["senha"]
        )
        db.session.add(user)
        db.session.commit()
        #return redirect(url_for())
    return render_template('/criaUser.html')

@app.route("/telaCadastro", methods=["GET", "POST"])
def cadastra():
    if request.method == "POST":
        user = Usuario(
            nome=request.form["nome"],
            endereco=request.form["endereco"],
            email=request.form["email"],
            senha=request.form["senha"]
        )
        db.session.add(user)
        db.session.commit()
        
    return render_template("/telaCadastro.html")

if __name__ == '__main__':
   app.run()
   #db.create_all()
    
    