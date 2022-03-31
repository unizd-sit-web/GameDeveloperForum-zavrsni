"""
    This module is used to share the pymongo object between the 
    flask app and the database controller module. 
"""

from flask import Flask
from flask_pymongo import PyMongo

# global shared var
mongo = PyMongo()

def create_app(config) -> Flask:
    """Creates a flask app and connects the global mongo instance to it"""
    app = Flask(__name__)
    for key in config:
        app.config[key] = config[key]
    mongo.init_app(app)
    return app
    