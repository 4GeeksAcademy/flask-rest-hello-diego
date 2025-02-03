import os
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Starship, Favorite, FavoriteType  

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Helper para simular el usuario actual (id=1)
def get_current_user():
    user = User.query.get(1)
    if not user:
        abort(404, description="No se encontró el usuario actual. Asegúrate de crearlo vía Flask-Admin u otro método.")
    return user

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ==============================
# Users Endpoints
# ==============================

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Aquí se devuelven los favoritos del usuario actual (simulado)
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user = get_current_user()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200

# ==============================
# People Endpoints
# ==============================

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# ==============================
# Planets Endpoints
# ==============================

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# ==============================
# Starships Endpoints
# ==============================

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([ship.serialize() for ship in starships]), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"error": "Starship not found"}), 404
    return jsonify(starship.serialize()), 200

# ==============================
# Favorites Endpoints
# ==============================

# --- POST Endpoints para agregar favoritos ---
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user = get_current_user()

    # Verificar planeta exista
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    # Verificar si ya existe el favorito para este usuario
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.PLANET,
        favorite_id=planet_id
    ).first()
    if existing:
        return jsonify({"error": "Favorite planet already added"}), 400

    favorite = Favorite(
        user_id=current_user.id,
        favorite_type=FavoriteType.PLANET,
        favorite_id=planet_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet added"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    current_user = get_current_user()

    # Verificar que el personaje existe
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.PEOPLE,
        favorite_id=people_id
    ).first()
    if existing:
        return jsonify({"error": "Favorite character already added"}), 400

    favorite = Favorite(
        user_id=current_user.id,
        favorite_type=FavoriteType.PEOPLE,
        favorite_id=people_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character added"}), 201

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id):
    current_user = get_current_user()

    # Verificar que la starship exista
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"error": "Starship not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.STARSHIP,
        favorite_id=starship_id
    ).first()
    if existing:
        return jsonify({"error": "Favorite starship already added"}), 400

    favorite = Favorite(
        user_id=current_user.id,
        favorite_type=FavoriteType.STARSHIP,
        favorite_id=starship_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite starship added"}), 201

# --- DELETE Endpoints para eliminar favoritos ---
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = get_current_user()
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.PLANET,
        favorite_id=planet_id
    ).first()
    if not favorite:
        return jsonify({"error": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet removed"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    current_user = get_current_user()
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.PEOPLE,
        favorite_id=people_id
    ).first()
    if not favorite:
        return jsonify({"error": "Favorite character not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character removed"}), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    current_user = get_current_user()
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=FavoriteType.STARSHIP,
        favorite_id=starship_id
    ).first()
    if not favorite:
        return jsonify({"error": "Favorite starship not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite starship removed"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
