from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

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