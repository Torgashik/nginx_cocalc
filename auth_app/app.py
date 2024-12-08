from flask import Flask, request, session, render_template, redirect, url_for, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
USERNAME = "admin"
PASSWORD = "password"

@app.route('/auth_check')
def auth_check():
    """Проверка авторизационной сессии."""
    if 'logged_in' in session:
        return '', 200  # Вернуть HTTP 200, если пользователь авторизован
    return '', 401  # Вернуть HTTP 401, если пользователь не авторизован

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Маршрут для логина."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect('/cocalc')  # Редирект в CoCalc
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Выход из сессии."""
    session.pop('logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
