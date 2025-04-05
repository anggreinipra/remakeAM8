def test_create_account(client):
    # Buat user dulu
    client.post("/users", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "test123"
    })
    login = client.post("/users/login", json={
        "email": "user1@example.com",
        "password": "test123"
    })
    token = login.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/accounts", json={
        "account_type": "savings"
    }, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data["account_number"] is not None
