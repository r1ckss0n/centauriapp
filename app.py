import os, psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# set up database
app.config['SECRET_KEY']= 'secret'
app.config['SQLACHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")

db=SQLAlchemy(app)




@app.route('/')
def index():
    return 'Hello'