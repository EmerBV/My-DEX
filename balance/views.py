from flask import render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from balance import app
from balance.forms import Validators
from balance.models import DBController, coins
from config import DATA_BASE, URL, URL_2, API_KEY
from datetime import datetime
import requests, sqlite3

dbroute = app.config.get(DATA_BASE)
dbcontroller = DBController(DATA_BASE)

@app.route("/", methods=["GET", "POST"])
def index():
    form = Validators()
    if request.method == "GET":
        return render_template("exchange.html", the_form=form)
    else:
        if form.validate():
            if form.data["convert"] == True:
                token_from = form.data["token_from"]
                token_to = form.data["token_to"]
                amount_from = form.data["amount_from"]
                answer = requests.get(URL.format(amount_from, token_from, token_to, API_KEY)).json()
                amount_to = answer["data"]["quote"][form.data["token_to"]]["price"]
                form["amount_to"].data = amount_to
                form["date"].data = str(datetime.now().date())
                form["time"].data = str(datetime.now().time())
                return render_template("exchange.html", the_form=form, calculation=amount_to, up=amount_from/amount_to)

            if form.data["buy"] == True:
                query = """INSERT INTO transactions (date, time, token_from, amount_from, token_to, amount_to) VALUES 
                        (:date, :time, :token_from, :amount_from, :token_to, :amount_to)"""
                try:
                    dbcontroller.changeSQL(query, form.data)
                except Exception as e:
                    print("Se ha producido un error:", Exception, e)
                    return render_template("exchange.html", the_form=form, calculation="Error en la conexión a la base de datos")           
                return redirect(url_for("index"))

            if form.data["buy"] == True and form["amount_to"].data == "":
                return render_template("exchange.html", the_form=form, calculation="Primero debes calcular")
        else:
            return render_template("exchange.html", the_form=form)

@app.route("/transactions")
def transactions():
    query = "SELECT id, date, time, token_from, amount_from, token_to, amount_to FROM transactions ORDER BY id"
    transactions = dbcontroller.querySQL(query)
    return render_template("transactions.html", items=transactions)

@app.route("/balance", methods=["GET", "POST"])
def status():
    form = Validators()
    if request.method == "GET":
        return render_template("balance.html", the_form=form)
    else:
        query = "SELECT SUM (amount_from) FROM transactions WHERE (token_from) == '{}';"
        froms = []
        total_from = []
        try:
            for coin in coins:
                dbcontroller.querySQL(query.format(coin))
                froms.extend(dbcontroller.querySQL(query.format(coin)))
            for i in froms:
                total_from.append(i["SUM (amount_from)"])
            total_quantities = dict(zip(coins, total_from))
            try:
                params = {
                "start":"1",
                "limit":"100",
                "convert":"EUR"
                }
                headers = {
                    "Accepts": "application/json",
                    "X-CMC_PRO_API_KEY": API_KEY,
                }
                req = requests.get(URL_2, headers=headers, params=params)
                dictionary = req.json()
                total_response = dictionary["data"]
            except:
                return render_template("balance.html", the_form=form, worth="Se ha producido un error por favor consulte con su administrador")
            symbols = []
            prices = []
            for i in total_response:
                symbols.append(i["symbol"])
                prices.append(i["quote"]["EUR"]["price"])
            price_coin = dict(zip(symbols, prices))
            stock = []
            for key in total_quantities:
                if key in price_coin and total_quantities.get(key) != None:
                    stock.append(total_quantities.get(key) * price_coin.get(key))
            worth = sum(stock)
            x = dbcontroller.querySQL("SELECT SUM (amount_to) FROM transactions WHERE (token_to) == 'EUR';")
            status = x[0]["SUM (amount_to)"]
            return render_template("balance.html", the_form=form, total_fiat=total_quantities["EUR"], worth=worth+status)
        except Exception as e:
            print("Se ha producido un error:", Exception, e)
            return render_template("balance.html", the_form=form, total_fiat="Error en la conexión a la base de datos", 
            worth="Error en la conexión a la base de datos")