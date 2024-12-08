from flask import Flask, request, session, render_template, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.autoescape = False

PASSWORD = 'lms_user'
USERNAME = 'Q8s2YN34aB'

@app.route('/auth_check')
def auth_check():
    if 'logged_in' in session:
        return '', 200
    return '', 401

@app.before_request
def check_session():
    allow = request.path.startswith('/login') or request.path.startswith('/static') or request.path == '/auth_check'
    if 'logged_in' not in session and not allow:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect('/cocalc')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)