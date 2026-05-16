import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_hash_password():
    password = "test_password123"
    hashed = hash_password(password)
    assert hashed != password
    assert hashed.startswith("$2")


def test_verify_password():
    password = "test_password123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_create_and_decode_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None
    decoded = decode_access_token(token)
    assert decoded.get("sub") == "testuser"
