from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    tipo = db.Column(db.String(20))
    transacoes = db.relationship("Transacao", foreign_keys="[Transacao.origem, Transacao.destino]", backref="usuario", primaryjoin="Usuario.id == Transacao.origem")

class Aluno(Usuario):
    id_aluno = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cpf = db.Column(db.Integer) 
    rg = db.Column(db.Integer)
    curso = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))

class Professor(Usuario):
    id_professor = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cpf = db.Column(db.Integer)  
    departamento = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))

class Parceiro(Usuario):
    id_parceiro = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cnpj = db.Column(db.Integer)
    produtos = db.relationship("Produto", backref="parceiro", lazy=True)#um parceiro tem vários produtos

class Administrador(Usuario):
    id_administrador = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)


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
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro.id_parceiro")) #relação
    

class Transacao(db.Model):
    id = db.Column("id_transacao", db.Integer, primary_key=True)
    origem = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    destino = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    valor = db.Column(db.Integer)
    data = db.Column(db.String(20))
    mensagem = db.Column(db.String(100))
    
    