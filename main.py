from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

db_uporabniki = TinyDB('uporabniki.json')
Uporabnik = Query()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    username = request.args.get('username')
    return render_template('index.html', username=username)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db_uporabniki.search(Uporabnik.uporabnisko_ime == username)
        if user and user[0]['geslo'] == password:
            return redirect(f'/index.html?username={username}')
        else:
            error = 'Napačno uporabniško ime ali geslo.'

    return render_template('login.html', error=error)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            error = 'Gesli se ne ujemata.'
        elif db_uporabniki.search(Uporabnik.uporabnisko_ime == username):
            error = 'Uporabniško ime že obstaja.'
        else:
            db_uporabniki.insert({'uporabnisko_ime': username, 'geslo': password})
            session['uporabnisko_ime'] = username
            return redirect('/index.html')

    return render_template('index.html', error=error)

# Stran za različne vrste masaž
@app.route('/svedska.html')
def svedska_masaza():
    return render_template('svedska.html')

@app.route('/tajska.html')
def tajska_masaza():
    return render_template('tajska.html')

@app.route('/sportska.html')
def sportska_masaza():
    return render_template('sportska.html')

@app.route('/aromaterapevtska.html')
def aromaterapevtska_masaza():
    return render_template('aromaterapevtska.html')

@app.route("/rezervacija.html", methods=["GET", "POST"])
def rezervacija():
    # Preberi termine iz datoteke
    with open("termini.txt", "r", encoding="utf-8") as f:
        termini = [vrstica.strip() for vrstica in f if vrstica.strip()]

    sporocilo = None  # Sporočilo za prikaz po rezervaciji

    if request.method == "POST":
        ime = request.form["ime"]
        masaza = request.form["masaza"]
        izbrani_termin = request.form["termin"]

        # Shrani rezervacijo
        with open("prijave.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {ime} | {masaza} | {izbrani_termin}\n")

        # Odstrani izbran termin
        novi_termini = [t for t in termini if t != izbrani_termin]
        with open("termini.txt", "w", encoding="utf-8") as f:
            for t in novi_termini:
                f.write(t + "\n")

        # Nastavi potrditveno sporočilo
        sporocilo = f"Hvala, {ime}, uspešno si rezerviral(a) {masaza} masažo ob {izbrani_termin}."
        termini = novi_termini  # Osveži prikazane termine

    return render_template("rezervacija.html", termini=termini, sporocilo=sporocilo)
if __name__ == '__main__':
    app.run(debug=True)
