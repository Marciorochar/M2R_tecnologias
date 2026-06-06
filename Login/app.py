import os
import smtplib
import sqlite3
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
 
app = Flask(__name__)
# Permite o acesso localmente de qualquer porta durante o desenvolvimento
CORS(app)

# --- CONFIGURAÇÃO DE E-MAIL ---
# IMPORTANTE: Não coloque sua senha diretamente no código.
# Use variáveis de ambiente para segurança.
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # Ex: "seu_email@gmail.com"
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS') # Ex: "sua_senha_de_app"

# --- INICIALIZAÇÃO DO BANCO DE DADOS (SQLITE) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL,
            idade TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Executa a criação do banco de dados ao iniciar o servidor
init_db()

# --- ROTA DE TESTE DE CONEXÃO ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Servidor M2R está ONLINE e funcionando perfeitamente!", "banco_de_dados": DB_FILE}), 200

# --- SISTEMA DE LOGIN E CADASTRO ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    usuario = data.get('usuario')
    email = data.get('email')
    password = data.get('password')
    nome = data.get('name')
    idade = data.get('idade')

    if not usuario or not email or not password or not nome:
        return jsonify({"error": "Preencha todos os campos obrigatórios."}), 400
        
    if len(password) < 6:
        return jsonify({"error": "A senha deve ter no mínimo 6 caracteres."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Valida se o nome de usuário já existe
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            return jsonify({"error": "Este usuário já está cadastrado."}), 400
            
        # Valida se o e-mail já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Este e-mail já está cadastrado."}), 400

        # Criptografa a senha antes de salvar no banco de dados
        senha_criptografada = generate_password_hash(password)

        # Adiciona o novo usuário no banco SQL
        cursor.execute(
            "INSERT INTO usuarios (usuario, email, senha, nome, idade) VALUES (?, ?, ?, ?, ?)",
            (usuario, email, senha_criptografada, nome, idade)
        )
        conn.commit()
        return jsonify({"message": "Cadastro realizado com sucesso!", "token": "token_provisorio_123", "nome": nome}), 201
    except Exception as e:
        return jsonify({"error": f"Erro interno no Python: {str(e)}"}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Preencha todos os campos."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Lê o usuário pelo email, ignorando letras maiúsculas/minúsculas e espaços
        cursor.execute("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        user = cursor.fetchone()
        
        if user:
            senha_salva = str(user['senha']).strip()
            nome_usuario = str(user['nome'])
            
            senha_digitada = str(password).strip()

            try:
                # Tenta validar a senha criptografada
                if check_password_hash(senha_salva, senha_digitada):
                    return jsonify({"message": f"Bem-vindo(a), {nome_usuario}!", "token": "token_provisorio_123", "nome": nome_usuario}), 200
            except Exception:
                pass
        else:
            print(f"[DEBUG LOGIN] Tentativa de login falhou. E-mail '{email}' não encontrado.")

        return jsonify({"error": "E-mail ou senha incorretos."}), 401
    except Exception as e:
        # Se qualquer outra coisa der errado, avisa o site e não deixa o servidor cair
        return jsonify({"error": f"Erro interno no servidor Python: {str(e)}"}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    if not data or not all(k in data for k in ('name', 'email', 'message')):
        return jsonify({"error": "Dados incompletos."}), 400

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return jsonify({"error": "O servidor de e-mail não está configurado."}), 500

    # Cria o corpo do e-mail
    subject = f"Nova Mensagem do Portfólio de {data['name']}"
    body = f"""
    Você recebeu uma nova mensagem do seu site:

    Nome: {data['name']}
    Email: {data['email']}

    Mensagem:
    {data['message']}
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS # Envia o e-mail para você mesmo

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({"message": "E-mail enviado com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"error": "Falha ao enviar o e-mail."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)