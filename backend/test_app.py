from app import app


def client():
    app.config.update(TESTING=True, RATELIMIT_ENABLED=False)
    return app.test_client()


def test_healthz_returns_ok():
    response = client().get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_status_returns_service_status():
    response = client().get("/api/status")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ativo"


def test_contact_accepts_valid_payload():
    response = client().post("/api/contato", json={
        "name": "Maria Silva",
        "email": "maria@example.com",
        "phone": "(22) 99999-0000",
        "message": "Gostaria de conversar sobre um site institucional.",
    }, environ_base={"REMOTE_ADDR": "127.0.0.10"})

    assert response.status_code == 200
    assert "message" in response.get_json()


def test_contact_rejects_missing_email():
    response = client().post("/api/contato", json={
        "name": "Maria Silva",
        "message": "Gostaria de conversar sobre um site institucional.",
    }, environ_base={"REMOTE_ADDR": "127.0.0.11"})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_contact_rejects_invalid_email():
    response = client().post("/api/contato", json={
        "name": "Maria Silva",
        "email": "email-invalido",
        "message": "Gostaria de conversar sobre um site institucional.",
    }, environ_base={"REMOTE_ADDR": "127.0.0.12"})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_contact_rejects_large_payload():
    response = client().post("/api/contato", json={
        "name": "Maria Silva",
        "email": "maria@example.com",
        "message": "x" * (20 * 1024),
    }, environ_base={"REMOTE_ADDR": "127.0.0.13"})

    assert response.status_code == 413
