from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test@email.com", "password": "pass123"})

    new_user = schemas.UserResponse(**res.json())

    print(new_user)

    assert res.status_code == 201


def test_login_user(client):
    res = client.post(
        "/login", data={"username": "test@email.com", "password": "pass123"})
    print(res.json())
    assert res.status_code == 200
