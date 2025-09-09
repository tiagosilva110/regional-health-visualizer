from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login_um.html")

@app.route("/register")
def res():
    return render_template("register_um.html")
