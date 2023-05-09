from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    # __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    tipo = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

class Aluno(db.Model):
    # __tablename__ = 'alunos'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cpf = db.Column(db.Integer) 
    rg = db.Column(db.Integer)
    curso = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))
    # transacoesAluno = db.relationship("TransacaoAluno", backref="aluno")
    # transacoesProf = db.relationship("TransacaoProfessor", backref="aluno")
    __mapper_args__ = {
        'polymorphic_identity': 'aluno'
    }

class Professor(db.Model):
    # __tablename__ = 'professores'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cpf = db.Column(db.Integer)  
    departamento = db.Column(db.String(40))
    moedas = db.Column(db.Integer)
    id_instituicao = db.Column(db.Integer, db.ForeignKey('instituicao.id_instituicao'))
    # transacoesProf = db.relationship("TransacaoProfessor", backref="professor")
    # transacoesAluno = db.relationship("TransacaoAluno", backref="professor")
    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }

class Parceiro(db.Model):
    # __tablename__ = 'parceiros'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cnpj = db.Column(db.Integer)
    produtos = db.relationship("Produto", backref="parceiro", lazy=True)#um parceiro tem vários produtos
    __mapper_args__ = {
        'polymorphic_identity': 'parceiro'
    }
    
class Administrador(db.Model):
    # __tablename__ = 'administradores'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'administrador'
    }

class Instituicao(db.Model):
    id = db.Column("id_instituicao", db.Integer, primary_key=True)
    nome = db.Column(db.String(40))
    # professores = db.relationship("Professor", backref="instituicao")
    # alunos = db.relationship("Aluno", backref="instituicao")
    consituentes = db.relationship("Usuario", backref="instituicao")

class Produto(db.Model):
    id = db.Column("id_produto", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(320))
    preco = db.Column(db.Integer)
    id_parceiro = db.Column(db.Integer, db.ForeignKey("parceiro.id")) #relação
    
    
class Transacao(db.Model):
    id = db.Column("id_transacao", db.Integer, primary_key=True)
    origem = db.Column(db.Integer, db.ForeignKey("usuario.id")) #sempre professor
    destino = db.Column(db.Integer, db.ForeignKey("usuario.id")) #sempre aluno
    valor = db.Column(db.Integer)
    data = db.Column(db.String(20))
    mensagem = db.Column(db.String(100))

# class TransacaoProfessor(db.Model):
#     id = db.Column("id_transacao_prof", db.Integer, primary_key=True)
#     origem = db.Column(db.Integer, db.ForeignKey("professor.id")) #sempre professor
#     destino = db.Column(db.Integer, db.ForeignKey("aluno.id")) #sempre aluno
#     valor = db.Column(db.Integer)
#     data = db.Column(db.String(20))
#     mensagem = db.Column(db.String(100))

# class TransacaoAluno(db.Model):
#     id = db.Column("id_transacao_aluno", db.Integer, primary_key=True)
#     origem = db.Column(db.Integer, db.ForeignKey("aluno.id"))#sempre aluno
#     destino = db.Column(db.Integer, db.ForeignKey("professor.id"))#sempre parceiro 
#     valor = db.Column(db.Integer)
#     data = db.Column(db.String(20))
#     mensagem = db.Column(db.String(100))
