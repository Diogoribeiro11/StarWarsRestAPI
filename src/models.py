from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##  create a Many to Many
FavoriteCharacters = db.Table("favCharacters",
     db.Column("users_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("characters_id", db.Integer, db.ForeignKey("characters.id"), primary_key=True)
)

FavoritePlanets = db.Table("favPlanets",
     db.Column("users_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("planets_id", db.Integer, db.ForeignKey("planets.id"), primary_key=True)
)

## CHARACTERS table

class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    birth_year = db.Column(db.String(100),  unique=False, nullable=False)
    gender = db.Column(db.String(100),  unique=False, nullable=False)
    # height = db.Column(db.String(100), unique=True, nullable=False)
    # skin_color = db.Column(db.String(100),  unique=True, nullable=False)
    # eye_color = db.Column(db.String(100),  unique=True, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            # "height":self.height,
            # "skin_color": self.hair_color,
            # "eye_color": self.eye
            
        }

## PLANETS table

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    population = db.Column(db.String(100), unique=False, nullable=False)
    # rotation_period = db.Column(db.String(100), unique=True, nullable=False)
    # surface_water = db.Column(db.String(100), unique=True, nullable=False)
    # gravity = db.Column(db.String(100), unique=True, nullable=False)
    # climate = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population":self.population,
            # "rotation_period": self.rotation_period,
            # "surface_water": self.surface_water,
            # "gravity": self.gravity,
            # "climate": self.climate,

        }

## USER table

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)
    favCharacters = db.relationship(Characters, secondary=FavoriteCharacters, lazy='subquery', backref=db.backref('usuarios', lazy=True))
    favPlanets = db.relationship(Planets, secondary=FavoritePlanets, lazy='subquery', backref=db.backref('usuarios', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favCharacters": self.get_fav_characters(),
            "favPlanets": self.get_fav_planets(),
            # do not serialize the password, its a security breach
        }

    def get_fav_characters(self):
        return list(map(lambda x : x.serialize(), self.favCharacters))

    def get_fav_planets(self):
        return list(map(lambda x : x.serialize(), self.favPlanets))
