"""
Тесты для POST /users, PUT /users/{id}, DELETE /users/{id}
"""
import pytest


class TestCreateUser:
    def test_create_user_status_code(self, session, base_url):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{base_url}/users", json=payload)
        assert response.status_code == 201

    def test_create_user_response_contains_submitted_data(self, session, base_url):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{base_url}/users", json=payload)
        body = response.json()

        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]

    def test_create_user_generates_id_and_createdAt(self, session, base_url):
        payload = {"name": "trinity", "job": "hacker"}
        response = session.post(f"{base_url}/users", json=payload)
        body = response.json()

        assert "id" in body
        assert "createdAt" in body

    def test_create_user_with_empty_body(self, session, base_url):
        response = session.post(f"{base_url}/users", json={})
        # API реально создаёт "пустого" пользователя — фиксируем текущее поведение
        assert response.status_code == 201


class TestUpdateUser:
    def test_update_user_put_status_code(self, session, base_url):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = session.put(f"{base_url}/users/2", json=payload)
        assert response.status_code == 200

    def test_update_user_put_returns_updated_fields(self, session, base_url):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = session.put(f"{base_url}/users/2", json=payload)
        body = response.json()

        assert body["job"] == "zion resident"
        assert "updatedAt" in body

    def test_update_user_patch_status_code(self, session, base_url):
        response = session.patch(f"{base_url}/users/2", json={"job": "captain"})
        assert response.status_code == 200


class TestDeleteUser:
    def test_delete_user_status_code(self, session, base_url):
        response = session.delete(f"{base_url}/users/2")
        assert response.status_code == 204

    def test_delete_user_returns_no_content(self, session, base_url):
        response = session.delete(f"{base_url}/users/2")
        assert response.text == ""
