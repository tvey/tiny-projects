import os

import dotenv
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

dotenv.load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
collection = mongo.db.get_collection(os.environ.get('COLLECTION'))


@app.route('/')
def index():
    todos = collection.find()
    count = len(list(todos.clone()))
    return render_template('index.html', todos=todos, count=count)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    collection.insert_one({'text': new_todo, 'is_done': False})
    return redirect(url_for('index'))


@app.route('/done/<pk>')
def mark_done(pk):
    collection.find_one_and_update(
        {'_id': ObjectId(pk)},
        {'$inc': {'count': 1}, '$set': {'is_done': True}},
    )
    return redirect(url_for('index'))


@app.route('/delete-done')
def delete_done():
    collection.delete_many({'is_done': True})
    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    collection.delete_many({})
    return redirect(url_for('index'))
