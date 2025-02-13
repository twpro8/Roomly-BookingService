from typing import Any

import pytest
from httpx import AsyncClient
from pydantic import EmailStr


@pytest.mark.parametrize(
    "username, email, password, status_code, surprise",
    [
        # Test case 1: New user with unique username and email
        ("Johnny", "address1@gmail.com", "123456", 200, None),
        # Test case 2: Same username and email, attempting to register again
        ("Johnny", "address1@gmail.com", "qwerty", 409, None),
        # Test case 3: Same username, but different email
        ("Johnny", "address2@gmail.com", "abcdef", 409, None),
        # Test case 4: Same email, but different username
        ("Walter", "address1@gmail.com", "abcdef", 409, None),
        # Test case 5: Unique username and email, but includes unexpected parameter
        ("Mike", "unique1@gmail.com", "git123", 422, "Boooo!"),
        # Test case 6: All fields are unique, successful registration
        ("Walter", "address2@gmail.com", "abcdef", 200, None),
        # Test case 7: Another successful registration with unique fields
        ("Alice", "address3@gmail.com", "password123", 200, None),
        # Test case 8: User sends additional fields ("surprise"), should return 422
        ("John", "john@example.com", "password123", 422, "Surprise field present"),
        # Test case 9: Weak password validation
        ("Bob", "bob@example.com", "123", 422, None),
        # Test case 10: Invalid email format
        ("InvalidEmail", "invalid-email", "password123", 422, None),
        # Test case 11: Username too short
        ("A", "auser@example.com", "password123", 422, None),
        # Test case 12: Email case-sensitivity check
        ("CaseSensitive", "Address1@Gmail.Com", "password123", 409, None),
        # Test case 13: Username too long (more than 150 characters)
        ("a" * 151, "validemail@example.com", "password123", 422, None),
        # Test case 14: Email too long (more than 255 characters)
        ("validusername", "a" * 246 + "@example.com", "password123", 422, None),
        # Test case 15: Empty username
        ("", "validemail@example.com", "password123", 422, None),
        # Test case 16: Empty email
        ("validusername", "", "password123", 422, None),
        # Test case 17: Empty password
        ("validusername", "validemail@example.com", "", 422, None),
        # Test case 18: All fields empty
        ("", "", "", 422, None),
    ],
)
async def test_auth_users(
    ac: AsyncClient,
    db,
    status_code: int,
    username: str | None,
    email: str | None,
    password: str | None,
    surprise: str | None,
):
    request_json = {"username": username, "email": email, "password": password}
    if surprise:
        request_json["surprise"] = surprise

    response = await ac.post("/users/register", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert isinstance(response.json(), dict)
        assert response.json()["status"] == "ok"

        user = await db.users.get_one_or_none(username=username)
        assert user is not None
        assert user.email == email
        user_dict = user.model_dump()
        assert "surprise" not in user_dict.keys()
        assert "password" not in user_dict.keys()
        assert "hashed_password" not in user_dict.keys()

        # Log in user
        response = await ac.post(
            "/users/login",
            json={
                "username": username,
                "password": password,
            },
        )
        assert response.status_code == status_code
        assert isinstance(response.json(), dict)
        assert response.json()["status"] == "ok"
        assert response.json()["access_token"] == ac.cookies.get("access_token")

        # Get current user
        response = await ac.get("/users/me")
        assert response.status_code == status_code
        user = response.json()
        assert isinstance(user, dict)
        assert user["username"] == username
        assert user["email"] == email
        assert "id" in user.keys()
        assert "password" not in user
        assert "hashed_password" not in user

        # Log out user
        response = await ac.post("/users/logout")
        assert response.status_code == status_code
        assert isinstance(response.json(), dict)
        assert response.json()["status"] == "ok"
        assert not ac.cookies.get("access_token")

        # Get current user
        response = await ac.get("/users/me")
        assert response.status_code == 401


@pytest.mark.parametrize(
    "username, password, email, bio, status_code, surprise",
    [
        (None, None, None, "Hello! My name is Tester1!", 200, None),
        ("Justin", None, None, None, 200, None),
        (None, None, None, "Oh no! My name is not Tester1 anymore!", 200, None),
        ("Unique Boy", "123123123", "unique_boy@gmail.com", "Hello there!", 422, "Boooo!"),
        ("Unique Boy", "123123123", "unique_boy@gmail.com", "Hello there!", 200, None),
        (None, None, None, None, 422, None),
        ("a" * 20, None, None, None, 200, None),
        ("b" * 21, None, None, None, 422, None),
        (None, "c" * 50, None, None, 200, None),
        (None, "d" * 51, None, None, 422, None),
        (None, None, None, "e" * 100, 200, None),
        (None, None, None, "f" * 101, 422, None),
        (111, None, None, None, 422, None),
        ("12345", None, None, None, 200, None),
        ("1234", None, None, None, 422, None),
        (None, "123456", None, None, 200, None),
        (None, "12345", None, None, 422, None),
        (None, None, None, "12", 200, None),
        (None, None, None, "1", 422, None),
    ],
)
async def test_partly_edit_user(
    authed_ac: AsyncClient,
    username: str | None,
    password: str | None,
    email: EmailStr | None,
    bio: str | None,
    status_code: int,
    surprise: Any | None,
):
    request_json = {}
    if username:
        request_json["username"] = username
    if password:
        request_json["password"] = password
    if email:
        request_json["email"] = email
    if bio:
        request_json["bio"] = bio
    if surprise:
        request_json["surprise"] = surprise

    old_user = (await authed_ac.get("/users/me")).json()
    response = await authed_ac.patch("/users/me", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert old_user != response.json()
