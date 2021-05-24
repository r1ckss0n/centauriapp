import os, psycopg2
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# set up database
app.config['SECRET_KEY']= 'secret'
app.config['SQLACHEMY_DATABASE_URI']= os.getenv("postgres://fiirvywpgdszid:fba7828d068dcda35d863b9dcb694a94869db7e3ecef21debf9a1a5d1de2be8e@ec2-54-160-96-70.compute-1.amazonaws.com:5432/dahna9ajn565oa")

db=SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form.get("user")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2 and user:
            user = request.form.get("user")
            db.execute("INSERT INTO users (username, password) VALUES (:username, MD5(:password))",
                {"username": user, "emai": email, "password": password1})
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
            email = request.form.get("email")
            password = request.form.get("password1")
            user = db.execute("SELECT username FROM users WHERE email = :email AND password = MD5(:password)",
                {"email": email, "password": password}).fetchone()
            return render_template("home.html", email =email.email)
        except:
            return render_template("home.html", email = "Unable to login")

    else:
        return render_template("login.html")