from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status

from database import create, select_one, select_many, update, delete
from models import Thing

app = FastAPI()


@app.get('/')
def hello():
    return {'my repressed memories': 'bonjour'}


@app.post('/things', response_model=Thing, status_code=201)
async def create_thing(thing: Thing):
    return create(thing)


@app.get('/things')
async def get_all_things():
    return select_many()


@app.get('/things/{thing_id}', response_model=Thing)
async def get_thing(thing_id: int):
    thing = select_one(thing_id)
    if thing is None:
        raise HTTPException(404, 'Thing is not found.')
    return thing


@app.put('/things/{thing_id}', response_model=Thing)
async def update_thing(thing_id: int, thing_data: Thing):
    thing = update(thing_id, thing_data)
    if thing is None:
        raise HTTPException(404, 'Thing is not found.')
    return thing


@app.delete('/things/{thing_id}')
async def delete_thing(thing_id: int):
    deleted = delete(thing_id)
    if not deleted:
        raise HTTPException(404, 'Thing is not found.')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
