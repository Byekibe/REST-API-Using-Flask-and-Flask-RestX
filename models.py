from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

basedir=os.path.dirname(os.path.realpath(__file__))

print(basedir)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(basedir, 'books.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self) -> str:
        return super().__repr__() 
