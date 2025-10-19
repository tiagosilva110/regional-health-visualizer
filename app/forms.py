from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, DateField
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
    cep = StringField('CEP', validators=[DataRequired()])
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
    cep = StringField('CEP (Only Numbers example: 13188888)', validators=[DataRequired()])
    birth = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
    sex = StringField('Sex (M,F or O)', validators=[DataRequired()])
    submit = SubmitField('Register')

class RegisterMedic(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    crm = StringField('Crm', validators=[DataRequired()])
    submit = SubmitField('Register')