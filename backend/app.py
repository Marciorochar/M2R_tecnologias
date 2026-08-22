import os
import re

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://m2rtecnologias.vercel.app")
LOCAL_FRONTEND_URLS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
]
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_URL, *LOCAL_FRONTEND_URLS]}})

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MAX_FIELD_LENGTHS = {
    "name": 120,
    "email": 254,
    "phone": 30,
    "message": 2000,
}


def clean_field(value, max_length):
    return str(value or "").strip()[:max_length]


def has_header_break(value):
    return "\r" in value or "\n" in value


@app.errorhandler(429)
def ratelimit_handler(_error):
    return jsonify({"error": "Muitas tentativas. Aguarde um pouco antes de enviar outra mensagem."}), 429


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
def status():
    return jsonify({
        "api": "M2R Tecnologias",
        "status": "ativo",
    }), 200


@app.post("/api/contato")
@limiter.limit("2 per hour")
def validate_contact():
    data = request.get_json(silent=True) or {}
    name = clean_field(data.get("name"), MAX_FIELD_LENGTHS["name"])
    email = clean_field(data.get("email"), MAX_FIELD_LENGTHS["email"])
    phone = clean_field(data.get("phone"), MAX_FIELD_LENGTHS["phone"])
    message = clean_field(data.get("message"), MAX_FIELD_LENGTHS["message"])

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
    app.run(debug=True, host="127.0.0.1", port=port)
