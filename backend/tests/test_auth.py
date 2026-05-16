import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.models.user import User


def test_login_success(client, db_session):
    # 创建测试用户
    user = User(
        username="testuser",
        password=hash_password("password123"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    # 测试登录
    response = client.post(
        "/api/v1/auth",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]
    assert "expires_in" in data["data"]


def test_login_invalid_credentials(client, db_session):
    response = client.post(
        "/api/v1/auth",
        json={"username": "nonexistent", "password": "wrong"},
    )
    assert response.status_code == 401


def test_get_current_user(client, db_session):
    # 创建测试用户
    user = User(
        username="testuser",
        password=hash_password("password123"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    # 登录获取 token
    login_response = client.post(
        "/api/v1/auth",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["data"]["token"]

    # 获取当前用户
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"
    assert data["data"]["nickname"] == "Test User"