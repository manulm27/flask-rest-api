"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app), 200

@app.route('/characters', methods=["GET"])
def get_all_people():
    all_characters = Characters.query.all()
    list_characters = list(map(lambda obj:obj.serialize(), all_characters))
    response_body ={
        'all_characters': list_characters
    }
    return jsonify(response_body), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_people(id):
    character = Characters.query.get(id).serialize()
    return jsonify({"character": character}), 200

@app.route('/planets', methods=["GET"])
def get_all_planets():
    all_planets = Planets.query.all()
    list_planets = list(map(lambda obj:obj.serialize(), all_planets))
    response_body ={
        'all_planets': list_planets
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.get(id).serialize()
    return jsonify({"planet": planet}), 200

@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        all_users = Users.query.all()
        list_users = list(map(lambda obj:obj.serialize(), all_users))
        response_body = {
            "users": list_users
            }
        return jsonify(response_body), 200
    else:
        body = request.get_json()
        new_user = ""
        for data_user in body:
            new_user = data_user
        model = Users()
        model.username = new_user['username']
        model.name = new_user['name']
        model.lastname = new_user['lastname']
        model.email = new_user['email']
        model.password = new_user['password']
        model.is_active = new_user['is_active']
        db.session.add(model)
        db.session.commit()

        return jsonify({"succes":"new user added"}), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id).serialize()
    return jsonify({"user": user}), 200

@app.route('/user/favorites/<int:id_user>', methods=['GET'])
def user_favorites(id_user):
    character = Users.query.filter_by(id=id_user).first().characters
    planet = Users.query.filter_by(id=id_user).first().planets
    user_favorites = []
    for first_data in character:
        user_favorites.append(first_data.serialize())
    for second_data in planet:
        user_favorites.append(second_data.serialize())
    response_body = {
        'obj_favorites': user_favorites
    }
    return jsonify(response_body), 200

@app.route('/favorites/character/user:<int:user_id>/character:<int:character_id>', methods=['POST'])
def add_fav_character(user_id, character_id):
    user = Users.query.get(user_id)
    character = Characters.query.get(character_id)
    user.characters.append(character)
    print(user.characters)
    db.session.commit()
    return jsonify({'succes': 'add character'})

@app.route('/favorites/planet/user:<int:user_id>/planet:<int:planet_id>', methods=['POST'])
def add_fav_planet(user_id, planet_id):
    user = Users.query.get(user_id)
    planet = Planets.query.get(planet_id)
    user.planets.append(planet)
    db.session.commit()
    return jsonify({'succes': 'add planet'})

@app.route('/favorite/character/user:<int:user_id>/character:<int:character_id>', methods=['DELETE'])
def del_fav_character(user_id, character_id):
    user = Users.query.get(user_id)
    character = Characters.query.get(character_id)
    user.characters.remove(character)
    db.session.commit()
    return jsonify({'succes': 'delete character'})

@app.route('/favorite/planet/user:<int:user_id>/planet:<int:planet_id>', methods=['DELETE'])
def del_fav_planet(user_id, planet_id):
    user = Users.query.get(user_id)
    planet = Planets.query.get(planet_id)
    user.planets.remove(planet)
    db.session.commit()
    return jsonify({'succes': 'delete planet'})

@app.route('/character/add', methods=['POST'])
def add_character():
    body = request.get_json()
    new_character = ""
    for data_character in body:
        new_character = data_character
    model = Characters()
    model.name = new_character['name']
    model.gender = new_character['gender']
    model.skin_color = new_character['skin_color']
    model.created = new_character['created']
    model.mass = new_character['mass']
    model.height = new_character['height']
    db.session.add(model)
    db.session.commit()

    return jsonify({'succes': 'add new character'})

@app.route('/character/update/<int:id>', methods=['PUT'])
def update_character(id):
    body = request.get_json()
    new_data = ""
    for data in body:
        new_data = data
    update_data = Characters.query.filter_by(id=id).update(new_data)
    db.session.commit()
    return jsonify({'succes': 'update character'})

@app.route('/character/del/<int:id>', methods=['DELETE'])
def del_character(id):
    character = Characters.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return jsonify({"succes": "delete character"})

@app.route('/planet/add', methods=['POST'])
def add_planet():
    body = request.get_json()
    new_planet = ""
    for data_planet in body:
        new_planet = data_planet
    model = Planets()
    model.name = new_planet['name']
    model.diameter = new_planet['diameter']
    model.rotation_period = new_planet['rotation_period']
    model.orbital_period = new_planet['orbital_period']
    model.terrain = new_planet['terrain']
    model.climate = new_planet['climate']
    db.session.add(model)
    db.session.commit()

    return jsonify({'succes': 'add new planet'})

@app.route('/planet/update/<int:id>', methods=['PUT'])
def update_planet(id):
    body = request.get_json()
    new_data = ""
    for data in body:
        new_data = data
    update_data = Planets.query.filter_by(id=id).update(new_data)
    return jsonify({'succes': 'update character'})

@app.route('/planet/del/<int:id>', methods=['DELETE'])
def del_planet(id):
    planet = Planets.query.get(id)
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"succes": "delete planet"})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
