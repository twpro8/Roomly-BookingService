import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "username, email, password, status_code",
    [
        ("Cat Tester", "tester_cat@gmail.com", "love_chicken", 200),
        ("Car Yugo", "yugish@gmail.com", "not_reliable", 200),
        ("Pythons", "pypy@gmail.com", "cute_programming", 200),
        ("Carrot", "pypy@gmail.com", "strong_password", 401),  # has the same email
        ("Pythons", "malon@gmail.com", "yeah_juicy", 401),  # has the same username
    ],
)
async def test_auth_users(
    username: str, email: str, password: str, status_code: int, ac: AsyncClient
):
    # Register user
    response = await ac.post(
        "/users/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    if status_code == 200:
        assert response.status_code == status_code
        assert isinstance(response.json(), dict)
        assert response.json()["status"] == "ok"

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

    else:
        assert response.status_code == 409
        assert isinstance(response.json(), dict)

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
        assert not ac.cookies.get("access_token")

        # Get current user
        response = await ac.get("/users/profile")
        assert response.status_code == status_code
