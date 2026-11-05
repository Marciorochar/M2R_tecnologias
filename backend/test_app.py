import os
import runpy
from pathlib import Path
from unittest.mock import patch

import pytest

os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("RATELIMIT_STORAGE_URI", "memory://")

from app import (
    app,
    clean_field,
    limiter,
    MAX_FIELD_LENGTHS,
    validate_frontend_origin,
    validate_app_environment,
    validate_proxy_hops,
    validate_rate_limit_storage,
)


@pytest.mark.parametrize('environment,debug', [('production', False), ('development', True), ('testing', False)])
def test_script_debug_respects_environment(monkeypatch, environment, debug):
    monkeypatch.setenv('APP_ENV', environment)
    monkeypatch.setenv(
        'RATELIMIT_STORAGE_URI',
        'rediss://localhost:6379/0' if environment == 'production' else 'memory://',
    )
    with patch('flask.Flask.run') as run:
        runpy.run_path(str(Path(__file__).with_name('app.py')), run_name='__main__')
    assert run.call_args.kwargs['debug'] is debug


def client():
    app.config.update(TESTING=True, RATELIMIT_ENABLED=False)
    limiter.reset()
    return app.test_client()


def test_healthz_returns_ok():
    response = client().get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    assert len(response.headers["X-Request-ID"]) == 32


def test_api_status_returns_service_status():
    response = client().get("/api/status")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ativo"


def test_security_headers_are_applied():
    response = client().get("/api/status")

    assert response.headers["Content-Security-Policy"] == (
        "default-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    )
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cross-Origin-Resource-Policy"] == "same-site"
    assert response.headers["Cache-Control"] == "no-store"
    assert "Strict-Transport-Security" not in response.headers


def test_hsts_is_applied_in_production():
    previous = app.config["APP_ENV"]
    app.config["APP_ENV"] = "production"
    try:
        response = client().get("/healthz")
        assert response.headers["Strict-Transport-Security"] == (
            "max-age=63072000; includeSubDomains; preload"
        )
    finally:
        app.config["APP_ENV"] = previous


def test_cors_allows_only_the_configured_origin():
    allowed = client().get(
        "/api/status", headers={"Origin": "https://m2rtecnologias.vercel.app"}
    )
    blocked = client().get(
        "/api/status", headers={"Origin": "https://evil.example"}
    )

    assert allowed.headers["Access-Control-Allow-Origin"] == (
        "https://m2rtecnologias.vercel.app"
    )
    assert "Access-Control-Allow-Origin" not in blocked.headers


def test_cors_preflight_is_limited_by_route():
    origin = "https://m2rtecnologias.vercel.app"
    status = client().options(
        "/api/status",
        headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
    )
    contact = client().options(
        "/api/contato",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )

    assert "GET" in status.headers["Access-Control-Allow-Methods"]
    assert "POST" not in status.headers["Access-Control-Allow-Methods"]
    assert "POST" in contact.headers["Access-Control-Allow-Methods"]
    assert "DELETE" not in contact.headers["Access-Control-Allow-Methods"]
    assert contact.headers["Access-Control-Allow-Headers"] == "Content-Type"


@pytest.mark.parametrize("origin", [
    "*",
    "javascript:alert(1)",
    "https://example.com/path",
    "https://user:password@example.com",
])
def test_frontend_origin_rejects_unsafe_values(origin):
    with pytest.raises(RuntimeError):
        validate_frontend_origin(origin, "production")


def test_frontend_origin_requires_https_in_production():
    with pytest.raises(RuntimeError):
        validate_frontend_origin("http://m2rtecnologias.vercel.app", "production")


def test_app_environment_rejects_unknown_values():
    with pytest.raises(RuntimeError):
        validate_app_environment("prod")


def test_memory_rate_limit_storage_is_rejected_in_production():
    with pytest.raises(RuntimeError):
        validate_rate_limit_storage("memory://", "production")


def test_non_redis_rate_limit_storage_is_rejected_in_production():
    with pytest.raises(RuntimeError):
        validate_rate_limit_storage("memcached://localhost:11211", "production")


def test_shared_rate_limit_storage_is_accepted_in_production():
    uri = "rediss://localhost:6379/0"
    assert validate_rate_limit_storage(uri, "production") == uri


@pytest.mark.parametrize("value,expected", [("0", 0), ("1", 1), (2, 2)])
def test_proxy_hops_accepts_non_negative_integers(value, expected):
    assert validate_proxy_hops(value) == expected


@pytest.mark.parametrize("value", ["-1", "one", "1.5", ""])
def test_proxy_hops_rejects_invalid_values(value):
    with pytest.raises(RuntimeError):
        validate_proxy_hops(value)


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


def test_contact_rejects_unexpected_fields():
    response = client().post("/api/contato", json={
        **VALID,
        "admin": True,
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "O corpo JSON possui campos nao permitidos."
    }


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
