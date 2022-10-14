"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets
#from models import Person

os.environ['DB_CONNECTION_STRING'] = 'mysql+mysqlconnector://root@localhost/star_wars'

app = Flask(__name__)
app.url_map.strict_slashes = False

"""Database configuration (where it is located)"""
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
    return generate_sitemap(app)

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        users = Users.query.all()
        listUsers = list(map(lambda obj:obj.serialize(), users))
        print(listUsers)
        response_body = {
            "Users": listUsers
            }
        return jsonify(response_body), 200
    else:
        body = request.get_json()
        person = ""
        for user in body:
            person = user
        data = Users()
        data.id = person['id']
        data.username = person['username']
        data.name = person['name']
        data.lastname = person['lastname']
        data.email = person['email']
        data.password = person['password']
        data.is_active = person['is_active']
        db.session.add(data)
        db.session.commit()

        return jsonify({"succes":"new user added"}), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    users = Users.query.all()
    listUsers = list(map(lambda obj:obj.serialize(), users))
    print(type(users))
    for user in listUsers:
        if user['id'] == id:
            return jsonify({"User": user}), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    listCharacters = list(map(lambda obj:obj.serialize(), characters))
    response_body = {
        "Characters": listCharacters
        }
    return jsonify(response_body), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    characters = Characters.query.all()
    listCharacters = list(map(lambda obj:obj.serialize(), characters))
    for character in listCharacters:
        if character['id'] == id:
            return jsonify({"Character": character}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
