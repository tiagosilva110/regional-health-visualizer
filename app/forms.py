from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, TextAreaField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from app import db
from app.models import UM
import sqlalchemy as sa


class LoginForm(FlaskForm):
    username = StringField('Medical Unit', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Medical Unit', validators=[DataRequired()])
    state = SelectField(
            'UF',
            choices=[('AC', 'AC'),  
                        ('AL', 'AL'),  
                        ('AP', 'AP'), 
                        ('AM', 'AM'),
                        ('BA', 'BA'), 
                        ('CE', 'CE'), 
                        ('DF', 'DF'), 
                        ('ES', 'ES'),
                        ('GO', 'GO'),  
                        ('MA', 'MA'), 
                        ('MT', 'MT'), 
                        ('MS', 'MS'), 
                        ('MG', 'MG'), 
                        ('PA', 'PA'), 
                        ('PB', 'PB'),  
                        ('PR', 'PR'), 
                        ('PE', 'PE'),
                        ('PI', 'PI'),
                        ('RJ', 'RJ'),
                        ('RN', 'RN'),  
                        ('RS', 'RS'),  
                        ('RO', 'RO'),  
                        ('RR', 'RR'),  
                        ('SC', 'SC'),  
                        ('SP', 'SP'),  
                        ('SE', 'SE'),  
                        ('TO', 'TO')],
            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(UM).where(UM.name == username.data))
        if user is not None:
            raise ValidationError('Please use a diffrent medical unit name')
        
class RegisterPerson(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    state = SelectField(
            'UF',
            choices=[('AC', 'AC'),  
                        ('AL', 'AL'),  
                        ('AP', 'AP'), 
                        ('AM', 'AM'),
                        ('BA', 'BA'), 
                        ('CE', 'CE'), 
                        ('DF', 'DF'), 
                        ('ES', 'ES'),
                        ('GO', 'GO'),  
                        ('MA', 'MA'), 
                        ('MT', 'MT'), 
                        ('MS', 'MS'), 
                        ('MG', 'MG'), 
                        ('PA', 'PA'), 
                        ('PB', 'PB'),  
                        ('PR', 'PR'), 
                        ('PE', 'PE'),
                        ('PI', 'PI'),
                        ('RJ', 'RJ'),
                        ('RN', 'RN'),  
                        ('RS', 'RS'),  
                        ('RO', 'RO'),  
                        ('RR', 'RR'),  
                        ('SC', 'SC'),  
                        ('SP', 'SP'),  
                        ('SE', 'SE'),  
                        ('TO', 'TO')],
            validators=[DataRequired()])
    birth = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
    sex = SelectField(
            'Sex',
            choices=[('M', 'M'),
                     ('F','F')  
                        ],
            validators=[DataRequired()])
    submit = SubmitField('Register')

class DeletePersonById(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    submit = SubmitField('Delete')

class RegisterMedic(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    crm = StringField('Crm', validators=[DataRequired()])
    submit = SubmitField('Register')


class DeleteMedicByCRM(FlaskForm):
    crm = StringField('crm', validators=[DataRequired()])
    submit = SubmitField('Delete')

class RegisterDiagnosis(FlaskForm):
    pessoa_id = StringField('id pessoa', validators=[DataRequired()])
    medico_crm = StringField('crm medico', validators=[DataRequired()])
    doenca = SelectField(
            'Selecione o diagnostico',
            choices=[
            ('alzheimer', 'alzheimer'),
            ('asma', 'asma'),
            ('dengue', 'dengue'),
            ('diabetes', 'diabetes'),
            ('hipertensao', 'hipertensao'),
            ('hiv', 'hiv'),
            ('parkinson', 'parkinson')
            ],

            validators=[DataRequired()])
    submit = SubmitField('Register')
