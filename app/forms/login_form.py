from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    
    #Formulario de inicio de sesión utilizando Flask-WTF.
    #Incluye validaciones básicas para los campos requeridos.
    #  protección contra ataques CSRF
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
