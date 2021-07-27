from flask import Flask, render_template, session, request
import ipdb


app = Flask(__name__)

app.config.update(
    SECRET_KEY = "Zdwmyo1SN8Fc+ay6+l++6hggBFe5s2UQMprPLqaBlLNeKuOb"
)

usernames = {}

import service

@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == 'POST':
        if not request.form.get('username'):
            return render_template('welcome.html', error='Please provide an username.')
        try:
            service.login(request.form.get('username'), request.form.get('animal'))
        except Exception as e:
            return render_template('welcome.html', error=str(e))
        session['name'] = request.form.get('username')
    return render_template('welcome.html', name=session.get('name'))