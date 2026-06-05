import os
import smtplib
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
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

# --- INICIALIZAÇÃO DO BANCO DE DADOS (EXCEL) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, 'usuarios.xlsx')

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['Usuario', 'e-mail', 'senha', 'nome', 'idade'])
        df.to_excel(EXCEL_FILE, sheet_name='Sheet1', index=False, engine='openpyxl')

# Executa a criação do arquivo ao iniciar o servidor
init_excel()

# --- ROTA DE TESTE DE CONEXÃO ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Servidor M2R está ONLINE e funcionando perfeitamente!", "banco_de_dados": EXCEL_FILE}), 200

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

    # Lê a planilha atual
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1', engine='openpyxl')
        # Se a planilha existir mas estiver vazia ou sem cabeçalhos, recria a estrutura automaticamente
        if 'Usuario' not in df.columns or 'e-mail' not in df.columns:
            df = pd.DataFrame(columns=['Usuario', 'e-mail', 'senha', 'nome', 'idade'])
    except Exception:
        df = pd.DataFrame(columns=['Usuario', 'e-mail', 'senha', 'nome', 'idade'])

    # Valida se o nome de usuário ou e-mail já existem
    if usuario in df['Usuario'].values:
        return jsonify({"error": "Este usuário já está cadastrado."}), 400
        
    if email in df['e-mail'].values:
        return jsonify({"error": "Este e-mail já está cadastrado."}), 400

    # Adiciona o novo usuário na planilha Excel com a senha exata que foi digitada (texto plano)
    new_user = pd.DataFrame([{'Usuario': usuario, 'e-mail': email, 'senha': password, 'nome': nome, 'idade': idade}])
    df = pd.concat([df, new_user], ignore_index=True)
    
    try:
        if os.path.exists(EXCEL_FILE):
            with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
        else:
            df.to_excel(EXCEL_FILE, sheet_name='Sheet1', index=False, engine='openpyxl')
            
        return jsonify({"message": "Cadastro realizado com sucesso!", "token": "token_provisorio_123", "nome": nome}), 201
    except PermissionError:
        # Evita que o servidor trave se o Excel estiver aberto em outro programa
        return jsonify({"error": "Erro: Feche o arquivo Excel antes de cadastrar!"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro interno no Python: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Preencha todos os campos."}), 400

        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1', engine='openpyxl')
        except Exception:
            return jsonify({"error": "E-mail ou senha incorretos."}), 401
            
        if 'e-mail' not in df.columns or 'senha' not in df.columns:
            return jsonify({"error": "Banco de dados incompleto."}), 500

        # Lê os emails removendo espaços vazios indesejados caso tenham sido digitados no Excel
        user = df[df['e-mail'].astype(str).str.strip() == str(email).strip()]
        
        if not user.empty:
            user_data = user.iloc[0]
            senha_salva = str(user_data['senha'])
            nome_usuario = str(user_data.get('nome', 'Usuário'))
            
            try:
                # Tenta validar a senha criptografada (antiga) OU a senha em texto plano (nova/manual)
                if check_password_hash(senha_salva, password) or senha_salva == password:
                    return jsonify({"message": f"Bem-vindo(a), {nome_usuario}!", "token": "token_provisorio_123", "nome": nome_usuario}), 200
            except ValueError:
                # Se a função de criptografia der erro ao ler um texto normal, testa diretamente o texto plano
                if senha_salva == password:
                    return jsonify({"message": f"Bem-vindo(a), {nome_usuario}!", "token": "token_provisorio_123", "nome": nome_usuario}), 200

        return jsonify({"error": "E-mail ou senha incorretos."}), 401
    except Exception as e:
        # Se qualquer outra coisa der errado, avisa o site e não deixa o servidor cair
        return jsonify({"error": f"Erro interno no servidor Python: {str(e)}"}), 500

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
    app.run(debug=True, host='0.0.0.0', port=5001)