import pytest
from httpx import AsyncClient


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
        # Test case 12: Username with special characters
        ("User!@#", "specialchar@example.com", "password123", 422, None),
        # Test case 13: Email case-sensitivity check
        ("CaseSensitive", "Address1@Gmail.Com", "password123", 409, None),
        # Test case 14: Username too long (more than 150 characters)
        ("a" * 151, "validemail@example.com", "password123", 422, None),
        # Test case 15: Email too long (more than 255 characters)
        ("validusername", "a" * 246 + "@example.com", "password123", 422, None),
        # Test case 16: Empty username
        ("", "validemail@example.com", "password123", 422, None),
        # Test case 17: Empty email
        ("validusername", "", "password123", 422, None),
        # Test case 18: Empty password
        ("validusername", "validemail@example.com", "", 422, None),
        # Test case 19: All fields empty
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
        response = await ac.get("/users/profile")
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
        response = await ac.get("/users/profile")
        assert response.status_code == 401
