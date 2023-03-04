from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import requests, json

from werkzeug.exceptions import abort

from pokestats.auth import login_required
from pokestats.db import get_db

bp = Blueprint('search', __name__)

p_types = [
     "bug",
     "dark",
     "dragon",
     "electric",
     "fairy",
     "fighting",
     "fire",
     "flying",
     "ghost",
     "grass",
     "ground",
     "ice",
     "normal",
     "poison",
     "psychic",
     "rock",
     "steel",
     "water"
]

def typeSearch(name):
    r = requests.get("https://pokeapi.co/api/v2/type/{}/".format(name))

    dat = json.loads(r.text)

    return dat

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    results = {}
    
    if request.method == 'POST':
        print("called")
        query = request.form['searchbar'].split()
        if query[0] in p_types:
            flash("type search")
            return redirect(url_for('results.type')) #typeSearch(query[0])
        else:
            flash("name search")


    return render_template('index.html')

