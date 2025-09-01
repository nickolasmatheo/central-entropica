import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_dificil_de_adivinhar'
app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'central_db'
app.config['DB_USER'] = 'central_user'
app.config['DB_PASS'] = 'admin' # A senha que você criou no Passo 1.3

bcrypt = Bcrypt(app)

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS']
    )
    return conn

# Rota de Login (Página Inicial)
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, usuario, senha FROM usuarios WHERE usuario = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and bcrypt.check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')

    return render_template('index.html')

# Rota de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verifica se o usuário já existe
        cur.execute('SELECT id FROM usuarios WHERE usuario = %s', (username,))
        if cur.fetchone():
            flash('Este nome de usuário já está em uso.', 'danger')
        else:
            cur.execute('INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)',
                        (username, hashed_password))
            conn.commit()
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        
        cur.close()
        conn.close()

    return render_template('cadastro.html')

# Rota da Home (Protegida)
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Rota de Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('login'))

# Função para criar a tabela de usuários (executar apenas uma vez)
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(80) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            criado_em TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # Cria a tabela no banco de dados se ela não existir
    init_db()
    # Inicia a aplicação
    app.run(debug=True)