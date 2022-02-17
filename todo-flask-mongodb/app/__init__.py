import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_pymongo import PyMongo

from .routes import main

load_dotenv(find_dotenv())

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = f'mongodb+srv://{db_user}:{db_password}@cluster0.cuwmg.mongodb.net/{db_name}?retryWrites=true&w=majority'

    mongo.init_app(app)

    app.register_blueprint(main)

    return app
