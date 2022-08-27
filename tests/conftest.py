""" Pytest Specific File
This file allows fixture to be available to all pytests.
You can create a seprate conftest.py under a specific module
to allow for futher inheritance of fixtures.
"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# used for actually talking to the database
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    """TEST DATABASE SESSION"""
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    """TEST FASTAPI CLIENT"""
    def override_get_db():
        """Dependency for using ORM"""
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# I want to run a function before a test -> USE FIXTURE


@pytest.fixture
def test_user(client):
    """CREATE TEST USER"""
    user_data = {
        "email": "fake@email.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = {'password': user_data['password'], **res.json()}

    return new_user
