from flask import Flask, Response
from flask import request, session
from flask import render_template, redirect, url_for, flash, send_file, jsonify
import os

from config import PASSWORD, USERNAME


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.autoescape = False


@app.before_request
def check_session():
    allow = request.path.startswith('/login') or request.path.startswith('/static')
    if 'logged_in' not in session and not allow:
        return render_template('login.html')


@app.route('/')
def index():
    if 'logged_in' not in session:
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('redirect_to_cocalc'))
    else:
        return render_template('login.html')

@app.route('/redirect_to_cocalc')
def redirect_to_cocalc():
    return redirect("https://lms.tech-lite.ru:8888")

@app.route('/check_auth')
def check_auth():
    if 'logged_in' in session:
        return Response(status=200)  # Успешная авторизация
    else:
        return Response(status=401)  # Не авторизован

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9090)