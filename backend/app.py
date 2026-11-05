import os
import re
from urllib.parse import urlsplit
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest
from werkzeug.middleware.proxy_fix import ProxyFix


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


def validate_app_environment(value):
    value = value.strip().lower()
    allowed = {"production", "dev", "development", "local", "test", "testing"}
    if value not in allowed:
        raise RuntimeError("APP_ENV possui um valor nao reconhecido.")
    return value


APP_ENV = validate_app_environment(
    os.getenv("APP_ENV", os.getenv("FLASK_ENV", "production"))
)
app.config["APP_ENV"] = APP_ENV
LOCAL_FRONTEND_URLS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
]


def validate_frontend_origin(value, environment):
    value = value.strip()
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise RuntimeError("FRONTEND_URL deve conter apenas uma origem HTTP(S) valida.")
    if environment == "production" and parsed.scheme != "https":
        raise RuntimeError("FRONTEND_URL deve usar HTTPS em producao.")
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_rate_limit_storage(value, environment):
    value = value.strip()
    if not value:
        raise RuntimeError("RATELIMIT_STORAGE_URI nao pode ser vazio.")
    if environment == "production" and urlsplit(value).scheme not in {"redis", "rediss"}:
        raise RuntimeError(
            "RATELIMIT_STORAGE_URI precisa ser compartilhado em producao; "
            "configure Redis com redis:// ou rediss://."
        )
    return value


def validate_proxy_hops(value):
    try:
        hops = int(value)
    except (TypeError, ValueError) as error:
        raise RuntimeError("TRUSTED_PROXY_HOPS deve ser um numero inteiro nao negativo.") from error
    if hops < 0:
        raise RuntimeError("TRUSTED_PROXY_HOPS deve ser um numero inteiro nao negativo.")
    return hops


FRONTEND_URL = validate_frontend_origin(
    os.getenv("FRONTEND_URL", "https://m2rtecnologias.vercel.app"), APP_ENV
)
RATELIMIT_STORAGE_URI = validate_rate_limit_storage(
    os.getenv("RATELIMIT_STORAGE_URI", "memory://"), APP_ENV
)
TRUSTED_PROXY_HOPS = validate_proxy_hops(os.getenv("TRUSTED_PROXY_HOPS", "0"))

if TRUSTED_PROXY_HOPS:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=TRUSTED_PROXY_HOPS)
app.config["TRUSTED_PROXY_HOPS"] = TRUSTED_PROXY_HOPS

allowed_origins = [FRONTEND_URL]
if APP_ENV in {"dev", "development", "local", "test", "testing"}:
    allowed_origins.extend(LOCAL_FRONTEND_URLS)

CORS(app, resources={
    r"/api/status": {
        "origins": allowed_origins,
        "methods": ["GET", "OPTIONS"],
    },
    r"/api/contato": {
        "origins": allowed_origins,
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    },
})

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=RATELIMIT_STORAGE_URI,
)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MAX_FIELD_LENGTHS = {
    "name": 120,
    "email": 254,
    "phone": 30,
    "message": 2000,
}


@app.after_request
def add_security_headers(response):
    response.headers["X-Request-ID"] = request.environ.get("m2r.request_id", "unknown")
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
    )
    response.headers["Cross-Origin-Resource-Policy"] = "same-site"
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    if app.config["APP_ENV"] == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
    return response


@app.before_request
def assign_request_id():
    request.environ["m2r.request_id"] = uuid4().hex


def clean_field(value, max_length):
    if not isinstance(value, str):
        raise ValueError("Os campos devem ser texto.")
    if len(value) > max_length:
        raise ValueError(f"Campo excede o limite de {max_length} caracteres.")
    return value.strip()


def has_header_break(value):
    return "\r" in value or "\n" in value


@app.errorhandler(429)
def ratelimit_handler(_error):
    return jsonify({"error": "Muitas tentativas. Aguarde um pouco antes de enviar outra mensagem."}), 429


@app.errorhandler(413)
def request_too_large_handler(_error):
    return jsonify({"error": "Requisicao muito grande."}), 413


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Backend institucional da M2R Tecnologias funcionando.",
    }), 200


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.get("/api/status")
@limiter.limit("60 per minute")
def status():
    return jsonify({
        "api": "M2R Tecnologias",
        "status": "ativo",
    }), 200


@app.post("/api/contato")
@limiter.limit("2 per hour")
def validate_contact():
    if not request.is_json:
        return jsonify({"error": "Use Content-Type application/json."}), 415
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Corpo JSON vazio ou malformado."}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "O corpo JSON deve ser um objeto."}), 400
    unexpected_fields = set(data) - set(MAX_FIELD_LENGTHS)
    if unexpected_fields:
        return jsonify({"error": "O corpo JSON possui campos nao permitidos."}), 400
    try:
        fields = {key: clean_field(data.get(key, ""), limit)
                  for key, limit in MAX_FIELD_LENGTHS.items()}
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    name, email, phone, message = (fields[key] for key in MAX_FIELD_LENGTHS)

    if not name or not email or not message:
        return jsonify({"error": "Preencha nome, e-mail e mensagem."}), 400

    if has_header_break(name) or has_header_break(email) or has_header_break(phone):
        return jsonify({"error": "Revise os dados informados e tente novamente."}), 400

    if not EMAIL_RE.match(email):
        return jsonify({"error": "Informe um e-mail valido."}), 400

    return jsonify({
        "message": "Contato validado. O envio e feito pelo cliente de e-mail do visitante.",
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=APP_ENV in {"dev", "development", "local"}, host="127.0.0.1", port=port)
