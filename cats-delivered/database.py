import os

import dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

dotenv.load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    filename = Column(String, nullable=False, unique=True)


def save_image():
    pass


def get_image():
    pass
