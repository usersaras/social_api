from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.environment_vars import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT

host = DB_HOST
name = DB_NAME
user = DB_USER
password = DB_PASSWORD
port = DB_PORT


DB_URL = f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{name}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
