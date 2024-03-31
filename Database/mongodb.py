from flask_pymongo import PyMongo

mongo = PyMongo()


def initialize_db(app):
    print("database connected")
    mongo.init_app(app)
