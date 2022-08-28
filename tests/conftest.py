""" Pytest Specific File
This file allows fixture to be available to all pytests.
You can create a seprate conftest.py under a specific module
to allow for futher inheritance of fixtures.
"""
from this import d
from venv import create
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


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
    # print("my database fixture ran")
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


@pytest.fixture
def test_user2(client):
    """CREATE TEST USER"""
    user_data = {
        "email": "fake2@email.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = {'password': user_data['password'], **res.json()}

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({
        'user_id': test_user['id']
    })


@pytest.fixture
def authorized_client(client, token):
    """working with authorized clients"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }
    ]

    # create posts for db
    posts = list(map(lambda post: models.Post(**post), posts_data))

    # add posts to the db
    session.add_all(posts)

    # commit changes to the DB
    session.commit()

    # get all Post entries
    session.query(models.Post).all()

    return posts
