from pickle import TRUE
from flask import Blueprint, redirect, render_template, request, url_for
import requests as r
from app.models import db, Pokedex

pokemon = Blueprint('pokemon', __name__, template_folder="pokemon_templates")

@pokemon.route('/pokemon', methods=["POST"])
def myPokemon():
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if data.status_code == 200:
        my_data = data.json()
        abilities = my_data['abilities']
        my_abilities = []
        for item in abilities:
            my_abilities.append((item['ability']['name']))
        my_img = my_data['sprites']['front_default']
        return render_template('pokemon.html', abilities=my_abilities,img_url=my_img, name=name)
    return redirect(url_for('home'))

@pokemon.route('/pokedex', methods = ["GET", "POST"])
def addPokedex():
    __table_args__ = {'extend_existing': TRUE}
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if data.status_code == 200:
        my_data = data.json()
        abilities = my_data['abilities']
        my_abilities = []
        for item in abilities:
            my_abilities.append((item['ability']['name']))
        image = my_data['sprites']['front_default']
        print(abilities)

        pokemon = Pokedex(name, image, " ".join(my_abilities))

        db.session.add(pokemon)
        db.session.commit()
        return render_template('pokedex.html', name = name, image = image, my_abilities=my_abilities)

@pokemon.route('/myPokemon')
def showCollection():
    collection = Pokedex.query.all()[::-1]
    return render_template('myPokemon.html',collection = collection)