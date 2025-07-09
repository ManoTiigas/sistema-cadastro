import tkinter as tk
import sqlite3
import bcrypt

# Conexão com banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criação da tabela (sem necessidade de alterar a estrutura)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')
conn.commit()

# Funções auxiliares para hash de senha
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-32'), bcrypt.gensalt()).decode('utf-32')

def verificar_senha(senha_informada, senha_hash):
    return bcrypt.checkpw(senha_informada.encode('utf-32'), senha_hash.encode('utf-32'))

# Funções CRUD
def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = hash_senha(senha)
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
        conn.commit()
        print("Usuário cadastrado com sucesso!\n")
    except sqlite3.IntegrityError:
        print("Erro: email já cadastrado.\n")

def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    print("\nLista de usuários:")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")
    print()

def editar_usuario():
    listar_usuarios()
    id_usuario = input("ID do usuário que deseja editar: ")
    novo_nome = input("Novo nome: ")
    novo_email = input("Novo email: ")
    nova_senha = input("Nova senha: ")
    nova_senha_hash = hash_senha(nova_senha)
    try:
        cursor.execute("UPDATE usuarios SET nome=?, email=?, senha=? WHERE id=?", (novo_nome, novo_email, nova_senha_hash, id_usuario))
        conn.commit()
        if cursor.rowcount:
            print("Usuário atualizado com sucesso!\n")
        else:
            print("Usuário não encontrado.\n")
    except sqlite3.IntegrityError:
        print("Erro: esse email já está sendo usado.\n")

def excluir_usuario():
    listar_usuarios()
    id_usuario = input("ID do usuário que deseja excluir: ")
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
    conn.commit()
    if cursor.rowcount:
        print("Usuário excluído com sucesso!\n")
    else:
        print("Usuário não encontrado.\n")

# (Opcional) Função de login
def login():
    email = input("Email: ")
    senha = input("Senha: ")
    cursor.execute("SELECT senha FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()
    if resultado and verificar_senha(senha, resultado[0]):
        print("Login bem-sucedido!\n")
    else:
        print("Email ou senha incorretos.\n")

# Menu
def menu():
    while True:
        print("=== Sistema de Cadastro de Usuários ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Editar usuário")
        print("4. Excluir usuário")
        print("5. Fazer login")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            editar_usuario()
        elif opcao == '4':
            excluir_usuario()
        elif opcao == '5':
            login()
        elif opcao == '6':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.\n")

# Executar o menu
menu()

# Fechar conexão
conn.close()
