from flask_sqlalchemy import SQLAlchemy as SQLalq

db = SQLalq()

class Usuario(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    tipo = db.relationship("", baclref="")          
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

    