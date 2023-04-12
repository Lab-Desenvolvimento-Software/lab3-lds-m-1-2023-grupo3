from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy as SQLalq

#model
db = SQLalq()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

class Usuario(db.Model):
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))


#usado pra criar o bd
with app.app_context():
    db.create_all()
    
#rotas/cotroller
@app.route("/")
def lol():
    return "asd"

@app.route("/mostraUser")
def mostra():
    users = db.session.execute(db.select(Usuario).order_by(Usuario.nome)).scalars()
    return render_template("/mostraUser.html", users=users)

@app.route("/criaUser", methods =["GET", "POST"])
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



if __name__ == '__main__':
   app.run()
   #db.create_all()
    
    