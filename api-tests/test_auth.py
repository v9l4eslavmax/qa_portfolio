"""
Тесты для POST /register и POST /login
"""


class TestRegister:
    def test_successful_registration(self, session, base_url):
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        response = session.post(f"{base_url}/register", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert "token" in body

    def test_registration_without_password_fails(self, session, base_url):
        payload = {"email": "sydney@fife"}
        response = session.post(f"{base_url}/register", json=payload)

        assert response.status_code == 400
        assert response.json()["error"] == "Missing password"


class TestLogin:
    def test_successful_login(self, session, base_url):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = session.post(f"{base_url}/login", json=payload)

        assert response.status_code == 200
        assert "token" in response.json()

    def test_login_without_password_fails(self, session, base_url):
        payload = {"email": "peter@klaven"}
        response = session.post(f"{base_url}/login", json=payload)

        assert response.status_code == 400
        assert response.json()["error"] == "Missing password"
