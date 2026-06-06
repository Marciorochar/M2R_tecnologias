import os
import smtplib
import jwt
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from dotenv import load_dotenv

# Carrega variáveis locais (ignoradas no Render)
load_dotenv()
 
app = Flask(__name__)
# CONFIGURAÇÃO DE CORS (Cross-Origin Resource Sharing)
# Isso é crucial para que o seu frontend (rodando em uma porta como 5500)
# possa fazer requisições para o seu backend (rodando na porta 5001).
# Durante o desenvolvimento, deixamos o CORS aberto para evitar bloqueios do Live Server.
CORS(app)

# CHAVE SECRETA PARA JWT - ESSENCIAL PARA CRIPTOGRAFIA
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'm2r_super_secret_key_123')

# --- CONFIGURAÇÃO DE E-MAIL ---
# IMPORTANTE: Não coloque sua senha diretamente no código.
# Use variáveis de ambiente para segurança.
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # Ex: "seu_email@gmail.com"
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS') # Ex: "sua_senha_de_app"

# --- INICIALIZAÇÃO DO BANCO DE DADOS (POSTGRESQL) ---

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise Exception("Variável de ambiente DATABASE_URL não foi encontrada.")
    conn = psycopg2.connect(db_url, sslmode='require')
    return conn

def init_db():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS site (
                    id SERIAL PRIMARY KEY,
                    usuario TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    idade TEXT
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("[Sucesso] Banco de dados Postgres conectado!")
        except Exception as e:
            print(f"[Aviso] Erro ao conectar no Postgres durante inicialização: {e}")

# Executa a criação do banco de dados ao iniciar o servidor
init_db()

# --- ROTA DE TESTE DE CONEXÃO ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Backend da M2R Tecnologias funcionando."
    }), 200

@app.route("/healthz", methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route("/api/status", methods=['GET'])
def status():
    return jsonify({
        "api": "M2R Tecnologias",
        "status": "ativo"
    }), 200

# --- DECORADOR PARA PROTEGER ROTAS COM JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as e:
            return jsonify({'error': 'Token é inválido ou expirou!'}), 401
        
        return f(*args, **kwargs)
    return decorated

# --- ROTA DE VERIFICAÇÃO DE SESSÃO ---
@app.route('/verify', methods=['GET'])
@token_required
def verify():
    return jsonify({"message": "Token válido, acesso liberado."}), 200

# --- SISTEMA DE LOGIN E CADASTRO ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    usuario = data.get('usuario', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    nome = data.get('name', '').strip()
    idade = str(data.get('idade', '')).strip()

    if not usuario or not email or not password or not nome:
        return jsonify({"error": "Preencha todos os campos obrigatórios."}), 400
        
    if len(password) < 6:
        return jsonify({"error": "A senha deve ter no mínimo 6 caracteres."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Valida se o nome de usuário já existe
        cursor.execute("SELECT id FROM site WHERE usuario = %s", (usuario,))
        if cursor.fetchone():
            return jsonify({"error": "Este usuário já está cadastrado."}), 400
            
        # Valida se o e-mail já existe
        cursor.execute("SELECT id FROM site WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Este e-mail já está cadastrado."}), 400

        # Criptografa a senha antes de salvar no banco de dados
        senha_criptografada = generate_password_hash(password)

        # Adiciona o novo usuário no banco SQL
        cursor.execute(
            "INSERT INTO site (usuario, email, senha, nome, idade) VALUES (%s, %s, %s, %s, %s)",
            (usuario, email, senha_criptografada, nome, idade)
        )
        conn.commit()
        
        # Gera token JWT real após o cadastro
        token = jwt.encode({
            'usuario': usuario,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"message": "Cadastro realizado com sucesso!", "token": token, "nome": nome}), 201
    except Exception as e:
        return jsonify({"error": f"Erro interno no Python: {str(e)}"}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"error": "Preencha todos os campos."}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Lê o usuário pelo email, ignorando letras maiúsculas/minúsculas e espaços
        cursor.execute("SELECT * FROM site WHERE LOWER(email) = LOWER(%s)", (email.strip(),))
        user = cursor.fetchone()
        
        if user:
            senha_salva = str(user['senha']).strip()
            nome_usuario = str(user['nome'])
            
            senha_digitada = str(password).strip()

            # Validação Híbrida: Verifica o hash da senha OU o texto plano (para contas manuais do SQL)
            senha_correta = False
            try:
                senha_correta = check_password_hash(senha_salva, senha_digitada)
            except Exception:
                pass # Se não for um formato de criptografia válido (como um texto simples), segue adiante

            if senha_correta or senha_salva == senha_digitada:
                # Gera token JWT real
                token = jwt.encode({
                    'usuario': user['usuario'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, app.config['SECRET_KEY'], algorithm="HS256")
                
                return jsonify({"message": f"Bem-vindo(a), {nome_usuario}!", "token": token, "nome": nome_usuario}), 200
        else:
            print(f"\n[DEBUG LOGIN] E-mail '{email}' não existe no banco de dados!")
            cursor.execute("SELECT email FROM site")
            emails_db = [row['email'] for row in cursor.fetchall()]
            print(f"[DEBUG LOGIN] E-mails que estão lá: {emails_db}\n")

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