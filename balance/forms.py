from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.fields.core import DateField, StringField, TimeField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, NumberRange

options = [( None,"--Seleccione un token--"),("EUR","Euro"),("ETH","Ethereum"),("BTC","Bitcoin"),("ADA","Cardano"),("LTC","Litecoin"),("BNB","Binance Coin"),("AXS","Axie Infinity"),("TRX","TRON"),("XRP","XRP"),("USDT","Tether")]

class Validators(FlaskForm):
    date = StringField("Fecha de la transacción")
    time = StringField("Hora de la transacción")
    token_from = SelectField("Token de origen", choices=options)
    amount_from = FloatField("Introduzca un monto", validators=[DataRequired(message="Debe informar el monto"),
                                                NumberRange(message="Debe informar superior a 1", min=1)])
    token_to = SelectField("Token de destino",  choices=options)
    amount_to = HiddenField("Cantidad que recibe")
    convert = SubmitField("Calcular")
    buy = SubmitField("Intercambiar")
    calculate = SubmitField("Calcular")