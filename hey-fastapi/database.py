from sqlmodel import Session, SQLModel, create_engine, select

from models import Thing

engine = create_engine('sqlite:///database.db', echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create(thing):
    with Session(engine) as session:
        session.add(thing)
        session.commit()
        session.refresh(thing)
        return thing


def select_one(thing_id):
    with Session(engine) as session:
        statement = select(Thing).where(Thing.id == thing_id)
        result = session.exec(statement)
        if result:
            return session.exec(statement).one()


def select_many():
    with Session(engine) as session:
        statement = select(Thing)
        return list(session.exec(statement))


def update(thing_id, updated_thing):
    with Session(engine) as session:
        statement = select(Thing).where(Thing.id == thing_id)
        results = session.exec(statement)
        thing = results.first()

        thing.name = updated_thing.name
        session.add(thing)
        session.commit()
        session.refresh(thing)
        return dict(thing)


def delete(thing_id):
    with Session(engine) as session:
        statement = select(Thing).where(Thing.id == thing_id)
        results = session.exec(statement)
        thing = results.one()
        session.delete(thing)
        session.commit()
        return True


if __name__ == '__main__':
    create_db_and_tables()
