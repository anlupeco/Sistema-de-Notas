from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    codigo = StringField('Codigo', validators=[DataRequired()])
    nombre = PasswordField('Nombre', validators=[DataRequired()])

