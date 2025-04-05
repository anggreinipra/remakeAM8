def test_create_user(client):
    response = client.post("/users", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "secure123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "access_token" in data

def test_get_user_profile_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
