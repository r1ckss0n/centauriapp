import os, psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.congig['SECRET_KEY']= 'secret'
app.config['SQLACHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='users'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True)
    email=db.Column(db.String,unique=True)
    
    db.init_app()


@app.route('/')
def index():
    return 'Hello'