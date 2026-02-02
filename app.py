from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    year = datetime.now().year
    cities = ["Warszawa","Kraków", "Poznań"]
    admin = True
    return render_template(
        "index.html",
        rok=year,
        miasta=cities,
        admin=admin,
    )

@app.route("/kontakt")
def kontakt_page():
    phone = "4654685463"
    email = "firma@firma.pl"
    return render_template(
        "contact.html",
        adres_email=email,
        nr_telefonu=phone,
    )

@app.route("/wiadomosci/<title>")
def news_page(title: str):
    return f"Strona wiadomosci {title.capitalize()}"