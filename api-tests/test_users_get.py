"""
Тесты для GET /users и GET /users/{id}
Документация API: https://reqres.in/
"""
import pytest


class TestGetUsersList:
    def test_get_users_status_code(self, session, base_url):
        response = session.get(f"{base_url}/users?page=2")
        assert response.status_code == 200

    def test_get_users_response_structure(self, session, base_url):
        response = session.get(f"{base_url}/users?page=2")
        body = response.json()

        assert "data" in body
        assert "page" in body
        assert "total" in body
        assert isinstance(body["data"], list)

    def test_get_users_page_returns_correct_page_number(self, session, base_url):
        response = session.get(f"{base_url}/users?page=2")
        body = response.json()
        assert body["page"] == 2

    def test_get_users_each_user_has_required_fields(self, session, base_url):
        response = session.get(f"{base_url}/users?page=1")
        body = response.json()

        required_fields = {"id", "email", "first_name", "last_name", "avatar"}
        for user in body["data"]:
            assert required_fields.issubset(user.keys())

    def test_get_users_empty_page_returns_empty_list(self, session, base_url):
        response = session.get(f"{base_url}/users?page=999")
        body = response.json()
        assert body["data"] == []


class TestGetSingleUser:
    def test_get_existing_user_status_code(self, session, base_url):
        response = session.get(f"{base_url}/users/2")
        assert response.status_code == 200

    def test_get_existing_user_returns_correct_id(self, session, base_url):
        response = session.get(f"{base_url}/users/2")
        body = response.json()
        assert body["data"]["id"] == 2

    def test_get_nonexistent_user_returns_404(self, session, base_url):
        response = session.get(f"{base_url}/users/999")
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id", [1, 2, 3, 5, 12])
    def test_get_multiple_valid_users(self, session, base_url, user_id):
        response = session.get(f"{base_url}/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == user_id
