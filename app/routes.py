from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
import sqlalchemy as sa
from app.models import UM, Pessoa, Medico, Diagnostico, Doenca
from urllib.parse import urlsplit
from app.forms import LoginForm, RegisterMedic, RegistrationForm, RegisterPerson, RegisterDiagnosis, RegisterDisease, DeletePersonById, SearchPersonByName, DeleteMedicByCRM, DeleteDiseaseById

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
            flash('Informações invalidas')
            return redirect(url_for('login'))
        login_user(user)
        next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Login', form=form)

@app.route("/registrar", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UM(name=form.username.data, state=form.state.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabens você agora está registrado!')
        return redirect(url_for('login'))

    return render_template("registrar.html", title="Registrar", form=form)

@login_required
@app.route("/pessoas", methods=['GET', 'POST'])
def viewpessoas():
    registerform = RegisterPerson()
    deleteform = DeletePersonById()
    searchform = SearchPersonByName()
    pessoas = db.session.scalars(sa.select(Pessoa).where(Pessoa.um_id == current_user.id))
    if registerform.validate_on_submit():
        person = Pessoa(name=registerform.name.data,state=registerform.state.data,birth=registerform.birth.data,sex=registerform.sex.data,um_id=current_user.id)
        db.session.add(person)
        db.session.commit()
        flash('Detectamos uma nova entrada de pessoa!')
        return redirect(url_for('viewpessoas'))
    
    if deleteform.validate_on_submit():
        pessoa = db.session.scalar(sa.select(Pessoa).where(Pessoa.id == deleteform.id.data))
        db.session.delete(pessoa)
        db.session.commit()
        flash('Detectamos uma remoção de pessoa!')
        return redirect(url_for('viewpessoas'))

    return render_template("pacient.html", title="Pacientes", registerform=registerform, deleteform = deleteform, searchform= searchform,data=pessoas)

@login_required
@app.route("/medico", methods=['GET', 'POST'])
def viewmedico():
    registerform = RegisterMedic()
    deleteform = DeleteMedicByCRM()
    medico = Medico.query.all()
    if registerform.validate_on_submit():
        medico = Medico(name=registerform.name.data, crm=registerform.crm.data, um_id=current_user.id)
        db.session.add(medico)
        db.session.commit()
        flash('Detectamos uma nova entrada de medico!')
        return redirect(url_for('viewmedico'))
    if deleteform.validate_on_submit():
        medico = db.session.scalar(sa.select(Medico).where(Medico.crm == deleteform.crm.data))
        db.session.delete(medico)
        db.session.commit()
        flash("Detectamos uma remoção de medico!")
        return redirect(url_for('viewmedico'))

    return render_template("medic.html", title="Register Medic", registerform=registerform, deleteform=deleteform, data=medico)

@login_required
@app.route("/doenca", methods=['GET', 'POST'])
def viewdoenca():
    registerform = RegisterDisease()
    deleteform = DeleteDiseaseById()
    doencas = Doenca.query.all()
    if registerform.validate_on_submit():
        doenca = Doenca(tipo=registerform.type.data)
        db.session.add(doenca)
        db.session.commit()
        flash('New disease enry!')
        return redirect(url_for('viewdisease'))
    if deleteform.validate_on_submit():
        doenca = Doenca(tipo=deleteform.type.data)
        db.session.add(doenca)
        db.session.commit()
        flash('New disease enry!')
        return redirect(url_for('viewdisease'))

    return render_template("disease.html", title="Consulta", registerform=registerform, deleteform=deleteform, data=doencas)

@login_required
@app.route("/diagnostico")
def viewdiagnostico():
    diagnosis = Diagnostico.query.all()
    registerform = RegisterDiagnosis()
    if registerform.validate_on_submit():
        doenca = Doenca(tipo=registerform.type.data)
        db.session.add(doenca)
        db.session.commit()
        flash('New disease enry!')
        return redirect(url_for('viewdisease'))
    return render_template("diagnosis.html", registerform= registerform,data=diagnosis, title="Hospital Data")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))