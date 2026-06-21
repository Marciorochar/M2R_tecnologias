import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://m2r-tecnologias.vercel.app")
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

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")


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
def send_contact():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify({"error": "Preencha nome, e-mail e mensagem."}), 400

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        app.logger.error("Configuracao de e-mail ausente.")
        return jsonify({"error": "O formulario de contato esta indisponivel no momento."}), 503

    subject = f"Nova mensagem do site M2R - {name}"
    body = f"""Voce recebeu uma nova mensagem pelo site institucional da M2R Tecnologias.

Nome: {name}
E-mail: {email}

Mensagem:
{message}
"""

    email_message = MIMEText(body)
    email_message["Subject"] = subject
    email_message["From"] = EMAIL_ADDRESS
    email_message["To"] = EMAIL_ADDRESS
    email_message["Reply-To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email_message)
    except Exception:
        app.logger.exception("Falha ao enviar mensagem de contato.")
        return jsonify({"error": "Nao foi possivel enviar sua mensagem. Tente novamente mais tarde."}), 500

    return jsonify({"message": "Mensagem enviada com sucesso. Retornaremos em breve."}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, host="127.0.0.1", port=port)
