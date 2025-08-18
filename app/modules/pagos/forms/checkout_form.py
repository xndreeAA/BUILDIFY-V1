from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class CheckoutForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')
    metodo_pago = SelectField('Método de pago', choices=[
        ('tarjeta', 'Tarjeta de crédito o débito'),
        ('pse', 'PSE'),
        ('efecty', 'Efecty')
    ], validators=[DataRequired()])

    numero_tarjeta = StringField('Número de tarjeta', validators=[DataRequired(), Length(min=13, max=19)])
    fecha_vencimiento = StringField('Fecha de vencimiento (MM/AA)', validators=[DataRequired()])
    codigo_seguridad = StringField('Código de seguridad', validators=[DataRequired(), Length(min=3, max=4)])
    nombre_tarjeta = StringField('Nombre en la tarjeta', validators=[DataRequired()])
    tipo_documento = StringField('Tipo de documento', validators=[DataRequired()])
    numero_documento = StringField('Número de documento', validators=[DataRequired()])
    
    submit = SubmitField('Pagar ahora')