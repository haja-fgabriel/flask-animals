from flask import Flask, render_template, session, request, redirect, abort, make_response
from flask.helpers import url_for
from flask_paginate import Pagination, get_page_parameter
import ipdb


app = Flask(__name__)

app.config.update(
    SECRET_KEY = "Zdwmyo1SN8Fc+ay6+l++6hggBFe5s2UQMprPLqaBlLNeKuOb"
)

import service
from datetime import date, datetime, timedelta, tzinfo

@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')
        animal = request.form.get('animal')
        if not username:
            return render_template(
                'welcome.html', 
                name=session.get('name'), 
                error='Please provide an username.'
            )
        service.confirm(username, animal)
        session['username'] = username
    
    name = session.get('username')
    searched_animals = None
    pagination = None
    if animal_name := request.args.get('animal-name'):
        page = request.args.get(get_page_parameter(), type=int, default=1)
        searched_animals = service.get_animals_by_name(name, animal_name, page)
        searched_animals_count = service.count_animals_by_name(name, animal_name)
        pagination = Pagination(page=page, total=searched_animals_count, per_page=10)

    animals = service.get_animals_for_username(name) if name else None
    return render_template(
        'welcome.html', 
        name=name, 
        animals=animals,
        searched_animals=searched_animals,
        pagination=pagination
    )

@app.route("/fetch-data")
def fetch_data():
    username = session.get('username')
    if not username or not service.get_user(username):
        abort(401)

    this_fetch = datetime.now().replace(tzinfo=None)
    last_fetch = session.get('last_fetch')
    if last_fetch and (seconds_elapsed := (this_fetch - last_fetch.replace(tzinfo=None)).seconds) < 60:
        return f'Please wait {60 - seconds_elapsed} seconds until fetching is available again<br><a href="javascript:window.history.back()">Go back</a>', 403
    session['last_fetch'] = this_fetch
        
    service.fetch_data(username)
    return redirect(url_for('welcome'))

@app.route("/img/<animal_id>")
def get_image(animal_id):
    username = session.get('username')
    if not username:
        abort(401)
    animal = service.get_animal(animal_id)
    if not animal: abort(404)
    if animal.user != username: abort(401)
    response = make_response(animal.image)
    response.headers['Content-Type'] = 'image/jpeg'
    return response
    
@app.route("/<username>/animals/<animal_id>", methods=["GET", "POST"])
def animals(username, animal_id):
    if request.method == 'GET':
        # TODO move your lazy ass and go to work!
        if not service.get_animal(animal_id):
            abort(404)
        return render_template('animal_page.html', animal_id=animal_id)
    elif request.method == 'POST':
        pass

# TODO finish JSON API
@app.route("/<username>/animals")
def get_all(username):
    pass

@app.route("/<username>/animals/<animal_id>", methods=["POST"])
def get_by_id(username, animal_id):
    pass