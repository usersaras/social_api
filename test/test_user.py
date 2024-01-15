from fastapi.testclient import TestClient
from app.main import app
from app.schema.user import CreatedUserResponse
from app.database import user, password, host, port, name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.database import get_db, Base

DB_URL = f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{name}_test"

engine = create_engine(DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Hello FastAPI!"
    assert res.status_code == 200


def test_create_user():
    res = client.post(
        "/user", json=({"email": "test5@test.co", "password": "Test@123"})
    )
    new_user = CreatedUserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.created_user.email == "test5@test.co"
