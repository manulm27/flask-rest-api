from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

fav_characters = db.Table('favorite_character',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('characters_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True)
    )

fav_planets = db.Table('favorite_planet',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    )

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    lastname  = db.Column(db.String(70), unique=False, nullable=False)
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
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    gender = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    # el metodo serialize convierte el objeto en un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "created": self.created,
            "mass": self.mass,
            "height": self.height
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)

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
        }




