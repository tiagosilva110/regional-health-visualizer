from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
import sqlalchemy as sa
from app.models import UM
from urllib.parse import urlsplit
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(UM).where(UM.name == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid data')
            return redirect(url_for('login'))
        login_user(user)
        next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Sign in', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UM(name=form.username.data, cep=form.cep.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, now you are registered!')
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)