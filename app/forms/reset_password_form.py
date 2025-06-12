#Formulario para nueva contraseña
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')
    ])
    submit = SubmitField('Restablecer contraseña')