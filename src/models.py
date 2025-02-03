from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy import ForeignKey
from enum import Enum

db = SQLAlchemy()

# Enumeración para definir los tipos de favoritos disponibles
class FavoriteType(Enum):
    PEOPLE = "people"
    PLANET = "planet"
    STARSHIP = "starship"

# Modelo de Usuario
@dataclass
class User(db.Model):
    __tablename__ = "users"

    # Los campos anotados se utilizarán para la serialización automática
    id: int
    email: str
    password: str
    is_active: bool

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    # Relación con los favoritos. Esto permite acceder a los favoritos de un usuario con "user.favorites"
    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Modelo de People (Personaje)
@dataclass
class People(db.Model):
    __tablename__ = "people"

    id: int
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(50))
    mass = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))

    def __repr__(self):
        return f'<People {self.name}>'

# Modelo de Planet
@dataclass
class Planet(db.Model):
    __tablename__ = "planets"

    id: int
    name: str
    climate: str
    terrain: str
    population: str
    diameter: str
    rotation_period: str
    orbital_period: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    population = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    rotation_period = db.Column(db.String(250))
    orbital_period = db.Column(db.String(250))

    def __repr__(self):
        return f'<Planet {self.name}>'

# Modelo de Starship
@dataclass
class Starship(db.Model):
    __tablename__ = "starships"

    id: int
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    crew: str
    passengers: str
    max_atmosphering_speed: str
    hyperdrive_rating: str
    starship_class: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    cost_in_credits = db.Column(db.String(50))
    length = db.Column(db.String(50))
    crew = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    max_atmosphering_speed = db.Column(db.String(50))
    hyperdrive_rating = db.Column(db.String(50))
    starship_class = db.Column(db.String(50))

    def __repr__(self):
        return f'<Starship {self.name}>'

# Modelo de Favorite para almacenar la relación entre usuario y entidad favorita
@dataclass
class Favorite(db.Model):
    __tablename__ = "favorites"

    id: int
    user_id: int
    favorite_type: str
    favorite_id: int  # ID de la entidad favorita (People, Planet o Starship)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Almacena el tipo de favorito utilizando el Enum FavoriteType
    favorite_type = db.Column(db.Enum(FavoriteType), nullable=False)
    # Este campo guarda el id de la entidad (personaje, planeta o nave)
    favorite_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # Al usar favorite_type.value se obtiene la cadena definida en el Enum
        return f'<Favorite User: {self.user_id}, Type: {self.favorite_type.value}, ID: {self.favorite_id}>'
