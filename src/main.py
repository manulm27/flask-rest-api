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
    return generate_sitemap(app), 200

@app.route('/people', methods=["GET"])
def get_all_people():
    all_people = Characters.query.all()
    list_people = list(map(lambda obj:obj.serialize(), all_people))
    response_body ={
        'all_people': list_people
    }
    return jsonify(response_body), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people(id):
    all_people = Characters.query.all()
    data_people = list(map(lambda obj:obj.serialize(), characters))
    for people in data_people:
        if people['id'] == id:
            return jsonify({"people": people}), 200

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
    all_planets = Characters.query.all()
    data_planet = list(map(lambda obj:obj.serialize(), all_planets))
    for planet in data_planet:
        if planet['id'] == id:
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
        data = Users()
        data.id = new_user['id']
        data.username = new_user['username']
        data.name = new_user['name']
        data.lastname = new_user['lastname']
        data.email = new_user['email']
        data.password = new_user['password']
        data.is_active = new_user['is_active']
        db.session.add(data)
        db.session.commit()

        return jsonify({"succes":"new user added"}), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    all_users = Users.query.all()
    list_users = list(map(lambda obj:obj.serialize(), users))
    for user in list_users:
        if user['id'] == id:
            return jsonify({"user": user}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
