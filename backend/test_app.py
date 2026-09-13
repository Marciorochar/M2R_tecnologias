import pytest

from app import app, clean_field, limiter, MAX_FIELD_LENGTHS


def client():
    app.config.update(TESTING=True, RATELIMIT_ENABLED=False)
    limiter.reset()
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
    assert response.is_json


VALID = {"name": "Maria", "email": "maria@example.com", "message": "Uma linha\nOutra linha"}


@pytest.mark.parametrize("body", ['[1]', '"abc"', '1', 'null', 'true', '[]', '{', ''])
def test_contact_rejects_non_object_or_invalid_json(body):
    response = client().post("/api/contato", data=body, content_type="application/json")
    assert response.status_code == 400
    assert response.is_json and "error" in response.json


@pytest.mark.parametrize("content_type", ["text/plain", "application/x-www-form-urlencoded", None])
def test_contact_rejects_incompatible_content_type(content_type):
    response = client().post("/api/contato", data='{}', content_type=content_type)
    assert response.status_code == 415
    assert response.is_json


@pytest.mark.parametrize("field", MAX_FIELD_LENGTHS)
@pytest.mark.parametrize("value", [None, 1, True, [], {"x": 1}])
def test_contact_rejects_field_types(field, value):
    response = client().post("/api/contato", json={**VALID, field: value})
    assert response.status_code == 400
    assert response.is_json


@pytest.mark.parametrize("field,limit", MAX_FIELD_LENGTHS.items())
def test_contact_exact_and_exceeded_limits(field, limit):
    value = "x" * limit if field != "email" else "x" * (limit - 12) + "@example.com"
    response = client().post("/api/contato", json={**VALID, field: value})
    assert response.status_code == 200
    response = client().post("/api/contato", json={**VALID, field: value + "x"})
    assert response.status_code == 400
    assert response.is_json


def test_multiline_message_is_preserved_and_only_validated():
    assert clean_field(VALID["message"], 2000) == VALID["message"]
    response = client().post("/api/contato", json=VALID)
    assert response.status_code == 200
    assert "Contato validado" in response.json["message"]


@pytest.mark.parametrize("field", ["name", "email", "phone"])
def test_header_breaks_are_rejected(field):
    response = client().post("/api/contato", json={**VALID, field: "abc\nxyz"})
    assert response.status_code == 400


def test_rate_limit_returns_json():
    app.config.update(TESTING=True, RATELIMIT_ENABLED=True)
    limiter.reset()
    try:
        with app.test_client() as limited:
            assert limited.post("/api/contato", json=VALID).status_code == 200
            assert limited.post("/api/contato", json=VALID).status_code == 200
            response = limited.post("/api/contato", json=VALID)
            assert response.status_code == 429
            assert response.is_json
    finally:
        app.config["RATELIMIT_ENABLED"] = False
        limiter.reset()
