from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


class Thing(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True)
    name: str


engine = create_engine('sqlite:///database.db', echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get('/')
def hello():
    return {'my repressed memories': 'bonjour'}


@app.post('/things', response_model=Thing)
async def create_thing(thing: Thing):
    if not thing.id:
        thing.id = uuid4()
    with Session(engine) as session:
        session.add(thing)
        session.commit()
        statement = select(Thing).where(Thing.id == thing.id)
        return dict(session.exec(statement).one())


@app.get('/things')
async def get_all_things():
    with Session(engine) as session:
        statement = select(Thing)
        return list(session.exec(statement))


# @app.get('/things/{thing_id}', response_model=Thing)
# async def get_thing(thing_id: int):
#     pass


# @app.put('/things/{thing_id}', response_model=Thing)
# async def update_thing(thing_id: int, thing: Thing):
#     pass


# @app.delete('things/{thing_id}')
# async def delete_thing(thing_id: int):
#     pass


if __name__ == '__main__':
    create_db_and_tables()
