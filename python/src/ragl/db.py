import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://ragl:ragl@localhost:5432/ragl",
)


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
