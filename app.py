from flask import Flask, render_template, session, request, redirect
from flask.helpers import url_for
import ipdb


app = Flask(__name__)

app.config.update(
    SECRET_KEY = "Zdwmyo1SN8Fc+ay6+l++6hggBFe5s2UQMprPLqaBlLNeKuOb"
)

usernames = {}

import service
from datetime import date, datetime, timedelta, tzinfo

@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')
        animal = request.form.get('animal')
        if not username:
            return render_template('welcome.html', name=session.get('name'), error='Please provide an username.')
        try:
            ipdb.set_trace()
            service.confirm(username, animal)
        except Exception as e:
            app.logger.error(str(e))
            return render_template('welcome.html', error=str(e))
        session['name'] = username
        session['animal'] = animal
    return render_template('welcome.html', name=session.get('name'))

@app.route("/fetch-data")
def fetch_data():
    this_fetch = datetime.now().replace(tzinfo=None)
    last_fetch = session.get('last_fetch').replace(tzinfo=None)
    ipdb.set_trace()
    if last_fetch and (seconds_elapsed := (this_fetch - last_fetch).seconds) < 60:
        raise Exception(f'Please wait {60 - seconds_elapsed} seconds until fetching is available again')
    session['last_fetch'] = this_fetch
    # TODO fetch data
    return redirect(url_for('welcome'))

# TODO finish JSON API
@app.route("/<username>/animals")
def get_all(username):
    pass

@app.route("/<username>/animals/<animal_id>", methods=["POST"])
def get_by_id(username, animal_id):
    pass