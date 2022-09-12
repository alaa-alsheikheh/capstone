import os 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer,Date, Float, create_engine
import json
from datetime import date 
from config import database_parameter

database_path =os.environ.get('DATABASE_URL',
 "postgresql://{}:{}@{}/{}".format(
    database_parameter['database_name'], database_parameter["user_name"], database_parameter["password"], database_parameter["port"])
)

db = SQLAlchemy()
"""
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_create():#drop and create the database
    db.drop_all()
    db.create_all()
    db_record_init()

def db_record_init():#initialize database with some test records
    add_actor=(Actor
    (
        name="Jison",
        gender='Male',
        age=30
    ))

    add_movie=(Movie
    (
        title="Red",
        release_date=date.today()
    ))

    add_show=Show.insert().values(
        Movie_id = add_movie.id,
        Actor_id = add_actor.id,
        actor_fee = 800.00
    )
    add_actor.insert()
    add_movie.insert()
    db.session.execute(add_show) 
    db.session.commit()

# relationships between classes
Show =db.Table('Show', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float))

class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
        }

class Movie(db.Model):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    release_date = Column(Date)
    actors=db.relationship('Actor', secondary=Show,backref=db.backref('shows', lazy='joined'))

    def __init__(self, name, gender, age):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }