from re import M
from jose import jwt
import pytest

from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test@email.com", "password": "pass123"})

    new_user = schemas.UserResponse(**res.json())

    print(new_user)

    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={
            "username": test_user['email'],
            "password": test_user['password']
        }
    )
    # validate login and oauth2
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id: str = payload.get("user_id")

    assert res.status_code == 200, "Invalid response from /login route"
    assert login_res.token_type == 'bearer', "Oauth2: incorret token type"
    assert id == test_user['id'], "User ID not matching on login"


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongfake@email.com", "password123", 403),
    ("fake@email.com", "wrongpassword", 403),
    (None, "wrongpassword", 422),
    ("wrongfake@email.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={
            "username": email,
            "password": password
        }
    )

    print(res.status_code)
    assert res.status_code == status_code
