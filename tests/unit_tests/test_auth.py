from src.services.auth import AuthService


def test_create_access_token():
    data = {"username": "test", "password": "<PASSWORD>"}
    jwt_token = AuthService().create_access_token(data)
    assert jwt_token
    assert isinstance(jwt_token, str)
