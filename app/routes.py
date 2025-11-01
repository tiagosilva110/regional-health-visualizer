from app import app
from flask import render_template, redirect, url_for, flash, request, Response
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from sqlalchemy import func
import sqlalchemy as sa
from datetime import datetime
from app.models import UM, Pessoa, Medico, Diagnostico
from urllib.parse import urlsplit
from app.forms import LoginForm, RegisterMedic, RegistrationForm, RegisterPerson, RegisterDiagnosis, DeletePersonById, DeleteMedicByCRM
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

@app.route('/')
@app.route('/index')
def index():
    resultados = (
        db.session.query(Pessoa.state, Diagnostico.doenca, func.count(Diagnostico.id))
        .join(Diagnostico, Pessoa.id == Diagnostico.pessoa_id)
        .group_by(Pessoa.state, Diagnostico.doenca)
        .all()
    )

    dados_por_estado = {}
    for estado, doenca, qtd in resultados:
        if estado not in dados_por_estado:
            dados_por_estado[estado] = {}
        dados_por_estado[estado][doenca] = qtd

    graficos = []
    for estado, dados in dados_por_estado.items():
        doencas = list(dados.keys())
        quantidades = list(dados.values())

        figura, eixo = plt.subplots(figsize=(6, 4))
        eixo.bar(doencas, quantidades, color='red')
        eixo.set_title(f'Diagnósticos em {estado}')
        eixo.set_xlabel('Tipo de Doença')
        eixo.set_ylabel('Quantidade')
        eixo.set_xticks(range(len(doencas)))
        eixo.set_xticklabels(doencas, rotation=30, ha='right')

        imagem_em_memoria = io.BytesIO()
        plt.tight_layout()
        plt.savefig(imagem_em_memoria, format='png')
        imagem_em_memoria.seek(0)
        imagem_base64 = base64.b64encode(imagem_em_memoria.getvalue()).decode('utf-8')
        plt.close(figura)

        graficos.append({"estado": estado, "imagem": imagem_base64})

    return render_template('index.html', graficos=graficos)

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

    return render_template("pacient.html", title="Pacientes", registerform=registerform, deleteform = deleteform,data=pessoas)

@login_required
@app.route("/medico", methods=['GET', 'POST'])
def viewmedico():
    registerform = RegisterMedic()
    deleteform = DeleteMedicByCRM()
    medico = db.session.scalars(sa.select(Medico).where(Medico.um_id == current_user.id))
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
@app.route("/diagnostico", methods=['GET','POST'])
def viewdiagnostico():
    dados = Diagnostico.query.all()
    registerform = RegisterDiagnosis()
    if registerform.validate_on_submit():
        diagnostico = Diagnostico(medico_crm=registerform.medico_crm.data,pessoa_id=registerform.pessoa_id.data, doenca=registerform.doenca.data, date=datetime.now())
        db.session.add(diagnostico)
        db.session.commit()
        flash('New disease enry!')
        return redirect(url_for('viewdiagnostico'))
    return render_template("diagnosis.html", registerform= registerform,data=dados, title="Hospital Data")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))