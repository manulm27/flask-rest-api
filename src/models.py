from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

fav_characters = db.Table('favorite_character',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'),primary_key=True),
    db.Column('characters_id', db.Integer, db.ForeignKey('characters.id', primary_key=True))
    )

fav_planets = db.Table('favorite_planet',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    )

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(70), nullable=False)
    lastname  = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    characters = relationship('Characters', secondary=fav_characters)
    planets = relationship('Planets', secondary=fav_planets)

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    created = db.Column(db.String(250))
    mass = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __repr__(self):
        return '<Characters %r>' % self.name

    # el metodo serialize convierte el objeto en un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "birth_rear": self.birth_year,
            "created": self.created,
            "mass": self.mass,
            "height": self.height
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)
    created = db.Column(db.Integer)
    population = db.Column(db.Integer)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.name,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.rotation_period,
            "terrain": self.terrain,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "created": self.created,
            "population" : self.population
        }




