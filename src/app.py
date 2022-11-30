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
from models import db, User, Characters, Planets
#from models import Person

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

    # GET USERS data

@app.route('/users', methods=['GET'])
def handle_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

    # POST USERS data

@app.route('/users', methods=['POST'])
def create_user():

    request_body_user = request.get_json()
    
    user1 = User(username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(user1)
    db.session.commit()

    return jsonify(request_body_user), 200

    # PUT edit USERS data

@app.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):

    request_body_user = request.get_json()
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User not found", status_code=404)

    if "username" in request_body_user:
        user1.username = request_body_user["username"]

    db.session.commit()

    return jsonify(request_body_user), 200

    # DELETE USERS 

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User not found", status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify("ok"), 200

    # GET USER Favorites

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_favorites(user_id):

    response_characters = User.query.filter_by(id=user_id).first().favCharacters
    response_planets = User.query.filter_by(id=user_id).first().favPlanets
    Characters = list(map(lambda x: x.serialize(), response_characters))
    Planets = list(map(lambda x: x.serialize(), response_planets))

    return jsonify({
        "FavCharacters": Characters,
        "FavPlanets": Planets
    }), 200

    # POST FAVORITE CHARACTER

@app.route('/favorites/characters/<int:characters_id>', methods=['POST'])
def create_fav_character(characters_id):
    user_id = 2
    user = User.query.get(user_id)
    character = Characters.query.get(characters_id)
    favList = User.query.filter_by(id=user_id).first().favCharacters
    favList.append(character)
    db.session.commit()

    return jsonify({
        "FavCharacters": list(map(lambda x : x.serialize(), favList))
    }), 200

    #DELETE FAVORITE CHARACTER

@app.route('/favorites/characters/<int:characters_id>', methods=['DELETE'])
def delete_fav_character(characters_id):
    user_id = 2
    user = User.query.get(user_id)
    character = Characters.query.get(characters_id)
    favList = User.query.filter_by(id=user_id).first().favCharacters
    favList.remove(character)
    db.session.commit()

    return jsonify({
        "FavCharacters": list(map(lambda x : x.serialize(), favList))
    }), 200

    # POST FAVORITE PLANET

@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def create_fav_planet(planets_id):
    user_id = 2
    user = User.query.get(user_id)
    planet = Planets.query.get(planets_id)
    favList = User.query.filter_by(id=user_id).first().favPlanets
    favList.append(planet)
    db.session.commit()

    return jsonify({
        "FavPlanets": list(map(lambda x : x.serialize(), favList))
    }), 200

    #DELETE FAVORITE PLANET

@app.route('/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_fav_planet(planets_id):
    user_id = 2
    user = User.query.get(user_id)
    planet = Planets.query.get(planets_id)
    favList = User.query.filter_by(id=user_id).first().favPlanets
    favList.remove(planet)
    db.session.commit()

    return jsonify({
        "FavPlanets": list(map(lambda x : x.serialize(), favList))
    }), 200

    # GET CHARACTERS data

@app.route('/characters', methods=['GET'])
def handle_characters():

    get_characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), get_characters))

    return jsonify(all_characters), 200

    #POST CHARACTER data

@app.route('/characters', methods=['POST'])
def create_character():

    request_body_character = request.get_json()
    
    character1 = Characters(name=request_body_character["name"], birth_year=request_body_character["birth_year"], gender=request_body_character["gender"])
    db.session.add(character1)
    db.session.commit()

    return jsonify(request_body_character), 200
    #height=request_body_character["height"], skin_color=request_body_character["skin_color"], eye_color=request_body_character["eye_color"]

    #PUT edit CHARACTERS data

@app.route('/characters/<int:characters_id>', methods=['PUT'])
def edit_character(characters_id):

    request_body_character = request.get_json()
    
    character1 = Characters.query.get(characters_id)
    if character1 is None:
        raise APIException("Character not found", status_code=404)

    if "name" in request_body_character:
        character1.name = request_body_character["name"]

    db.session.commit()

    return jsonify(request_body_character), 200

    # DELETE CHARACTER

@app.route('/characters/<int:characters_id>', methods=['DELETE'])
def delete_character(characters_id):
    
    character1 = Characters.query.get(characters_id)
    if character1 is None:
        raise APIException("Character not found", status_code=404)
    db.session.delete(character1)
    db.session.commit()

    return jsonify("ok"), 200

    # GET CHARACTER Details

@app.route('/characters/<int:characters_id>', methods=['GET'])
def handle_characters_details(characters_id):
    character_detail = Characters.query.get(characters_id)
    all_details = character_detail.serialize()

    return jsonify(all_details), 200

    # GET PLANETS data

@app.route('/planets', methods=['GET'])
def handle_planets():

    get_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), get_planets))

    return jsonify(all_planets), 200

    #POST PLANETS data

@app.route('/planets', methods=['POST'])
def create_planet():

    request_body_planets = request.get_json()
    
    planet1 = Planets(name=request_body_planets["name"], population=request_body_planets["population"], )
    db.session.add(planet1)
    db.session.commit()

    return jsonify(request_body_planets), 200
     #rotation_period=request_body_planets["rotation_period"], surface_water=request_body_planets["surface_water"], gravity=request_body_planets["gravity"], climate=request_body_planets["climate"]

    # PUT edit PLANETS

@app.route('/planets/<int:planets_id>', methods=['PUT'])
def edit_planet(planets_id):

    request_body_planets = request.get_json()
    
    planets1 = Planets.query.get(planets_id)
    if planets1 is None:
        raise APIException("Planet not found", status_code=404)

    if "name" in request_body_planets:
        planets1.name = request_body_planets["name"]

    db.session.commit()

    return jsonify(request_body_planets), 200

    # DELETE PLANETS

@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    
    planets1 = Planets.query.get(planets_id)
    if planets1 is None:
        raise APIException("Planet not found", status_code=404)
    db.session.delete(planets1)
    db.session.commit()

    return jsonify("ok"), 200

    # GET PLANETS Details

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planets_details(planets_id):
    planet_detail = Planets.query.get(planets_id)
    all_details = planet_detail.serialize()

    return jsonify(all_details), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
