from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index(db: Session = Depends(get_db)):
    thoughts = db.query(models.Thought).all()
    return {'thoughts': thoughts}
