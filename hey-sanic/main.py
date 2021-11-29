import os

import dotenv
from bson import ObjectId
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json as json_response
from sanic_motor import BaseModel
from sanic_openapi import swagger_blueprint

dotenv.load_dotenv()

app = Sanic(__name__)

app.blueprint(swagger_blueprint)

app.config.update(
    {
        'MOTOR_URI': os.environ['MONGODB_URL'],
    }
)

BaseModel.init_app(app)


class Thing(BaseModel):
    __coll__ = 'things'


@app.route('/test', methods=['GET'])
async def test(request):
    """Say bonjour."""
    return json_response({'my repressed memories': 'bonjour'})


@app.route('/', methods=['GET'])
async def all_things(request):
    """Get a list of all things."""
    things = await Thing.find(as_raw=True)
    return json_response(things.objects)


@app.route('/', methods=['POST'])
async def add_thing(request):
    """Create a new thing."""
    thing = request.json
    thing['_id'] = str(ObjectId())
    new_thing = await Thing.insert_one(thing)
    new_thing_from_db = await Thing.find_one(
        {'_id': new_thing.inserted_id}, as_raw=True
    )
    return json_response(new_thing_from_db)


@app.route('/<thing_id>', methods=['GET'])
async def get_thing(request, thing_id):
    """Get a single object by id."""
    thing = await Thing.find_one({'_id': thing_id}, as_raw=True)
    if not thing:
        raise NotFound(f'Thing with id "{thing_id}" is not found.')
    return json_response(thing)


@app.route('/<thing_id>', methods=['PUT'])
async def update_thing(request, thing_id):
    """Update a thing."""
    await Thing.update_one({'_id': thing_id}, {'$set': request.json})
    edited_thing = await Thing.find_one({'_id': thing_id}, as_raw=True)
    if not edited_thing:
        raise NotFound(f'Thing with id "{thing_id}" is not found.')
    return json_response(edited_thing)


@app.route('/<thing_id>', methods=['DELETE'])
async def remove_thing(request, thing_id):
    """Delete a thing."""
    result = await Thing.delete_one({"_id": thing_id})
    if result.deleted_count == 1:
        return json_response({}, status=204)
    raise NotFound(f'Thing with id "{thing_id}" is not found.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, auto_reload=True)
