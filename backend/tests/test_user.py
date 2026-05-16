import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.models.user import User


def get_auth_headers(client: TestClient, db_session) -> dict:
    user = User(
        username="admin",
        password=hash_password("admin123"),
        nickname="Admin",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/v1/auth",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_response.json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_users(client, db_session):
    # 创建测试用户
    for i in range(3):
        user = User(
            username=f"user{i}",
            password=hash_password("password"),
            nickname=f"User {i}",
            status=1,
        )
        db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 3
    assert "$page" in data
    assert "total" in data


def test_create_user(client, db_session):
    headers = get_auth_headers(client, db_session)
    response = client.post(
        "/api/v1/users",
        json={
            "username": "newuser",
            "password": "newpass123",
            "nickname": "New User",
            "email": "new@example.com",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["username"] == "newuser"
    assert data["data"]["nickname"] == "New User"


def test_get_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.get(f"/api/v1/users/{user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"


def test_update_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.put(
        f"/api/v1/users/{user.id}",
        json={"nickname": "Updated Name"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["nickname"] == "Updated Name"


def test_delete_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.delete(f"/api/v1/users/{user.id}", headers=headers)
    assert response.status_code == 200
