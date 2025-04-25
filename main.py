from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('uporabniki.json')
Uporabnik = Query()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    username = request.args.get('username', None)
    return render_template('index.html', username=username)


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Tukaj predpostavljam, da iščeš uporabnika v bazi (seveda moraš to prilagoditi)
        user = db.search(Uporabnik.uporabnisko_ime == username)
        if user and user[0]['geslo'] == password:
            # Tukaj več ne shranjujemo uporabniškega imena v sejo, ampak samo prenesemo podatke
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
        elif db.search(Uporabnik.uporabnisko_ime == username):  # PRAVILNO
            error = 'Uporabniško ime že obstaja.'
        else:
            db.insert({'uporabnisko_ime': username, 'geslo': password})
            session['uporabnisko_ime'] = username
            return redirect('/index.html')

    return render_template('index.html', error=error)


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



if __name__ == '__main__':
    app.run(debug=True)