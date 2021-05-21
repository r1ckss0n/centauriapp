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

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False, unique=True)


@app.route('/')
def index():
    return render_template('home.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form.get("user")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2 and user:
            user = request.form.get("user")
            db.execute("INSERT INTO users (username, password) VALUES (:username, MD5(:password))",
                {"username": user, "password": password1})
            db.commit()
            return render_template("home.html", user = user)
        else:            
            return render_template("register.html", alert="Insert matching passwords, please")
    

    else:   
        return render_template("register.html")
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            user = request.form.get("user")
            password = request.form.get("password1")
            user = db.execute("SELECT username FROM users WHERE username = :username AND password = MD5(:password)",
                {"username": user, "password": password}).fetchone()
            return render_template("home.html", user = user.username)
        except:
            return render_template("home.html", user = "Unable to login")

    else:
        return render_template("login.html")