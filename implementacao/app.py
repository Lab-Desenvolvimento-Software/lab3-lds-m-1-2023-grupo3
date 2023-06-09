from flask import Flask, render_template, request, redirect, url_for, make_response
from model import db
from routes import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moeda.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    # cria()

if __name__ == '__main__':
    app.run()