from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy as SQLalq
from model import Usuario, db, app

@app.route("/")
def mostra():
    return "asd"

@app.route('/test')
def show_all():
    usuario = Usuario(
        id = 1,
        nome = "Jose",
        endereco = "rua 1",
        email = "mail@mail.com",
        senha = "123"
    )
    db.session.add(usuario)
    db.session.commit()
    
    return render_template('/views/test.html', user = usuario.query.all() )

if __name__ == '__main__':
   app.run()
   #db.create_all()