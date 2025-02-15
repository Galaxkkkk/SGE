import sqlite3
from datetime import datetime
import hashlib

DATABASE = "estoque.db"


# Configurações do Banco de Dados SQL

def criar_tabela():
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL             
      )
    ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS  movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL, -- 'entrada' ou 'saida'
        quantidade INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
      )      
    ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS  usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        role TEXT NOT NULL -- 'admin', 'gerente', 'funcionario'       
      )
    ''')
    conn.commit()

def adicionar_produto():
  nome = input("Nome do produto: ")
  descricao = input("Descrição: ")
  preco = float(input("Preço: "))
  quantidade = int(input("Quantidade inicial: "))

  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('''
      INSERT INTO produtos (nome, descricao, preco, quantidade)
      VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade))
  print("Produto adicionado com sucesso!")

def listar_produtos():
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    if not produtos:
      print("Nenhum produto cadastrado")
      return
    
    print("\nLista  de Produtos:")
    for produto in produtos:
      print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço: R${produto[3]:.2f}, Estoque: {produto[4]}")

def registrar_movimentacao():
  listar_produtos()
  produto_id = int(input("ID do produto: "))
  tipo = input("Tipo (entrada/saida): ").lower()
  quantidade = int(input("Quantidade: "))

  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()

    # Atualiza o Estoque do Banco de Dados
    if tipo == 'entrada':
      cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE id = ?               
      ''', (quantidade, produto_id))
    
    elif tipo == 'saida':
      cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?               
      ''', (quantidade, produto_id))
    
    else:
      print("Tipo Inválido!")
      return
    
    # Registra a Movimentação do Banco de Dados
    cursor.execute('''
      INSERT INTO movimentacoes (produto_id, tipo, quantidade, data)
      VALUES (?, ?, ?, ?)
    ''', (produto_id, tipo, quantidade, datetime.now().strftime("%d/%m/%Y %H:%M")))
    conn.commit()
  print("Movimentação registrada com sucesso!")
  
def listar_estoque_baixo():
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE quantidade < 5')
    produtos = cursor.fetchall()
    
    if not produtos:
      print("Nenhum produto com estoque baixo.")
      return
    
    print("\nProdutos com estoque baixo: ")
    for produto in produtos:
      print(f"ID: {produto[0]}, Nome: {produto[1]}, Estoque: {produto[4]}")
      
def modificar_preco():
  listar_produtos()
  produto_id = int(input("Digite o ID do produto que deseja modificar: "))
  
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    
    if not produto:
      print("Produto não encontrado.")
      return
    
    nome, preco_atual = produto
    print(f"Preço atual de '{nome}': R${preco_atual:.2f}")
  
  while True:
    try:
        novo_preco = float(input("Digite o novo preço: "))
        if novo_preco <=0:
          print("O preço deve ser positivo. Tente Novamente.")
        else:
          break
    except ValueError:
      print("Preço inválido. Digite um Número.")
  
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('''
      UPDATE produtos
      SET preco = ?
      WHERE id = ?               
    ''', (novo_preco, produto_id))
    conn.commit()
    
  print(f"Preço de '{nome}' atualizado para R${novo_preco:.2f}.")

def hash_senha(senha):
  return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario():
  username = input("Escolha seu nome de Usuário: ")
  senha = input("Escolha uma senha: ")
  role = input("Escolha o nível de acesso (admin/gerente/funcionario): ").lower()
  senha_hash = hash_senha(senha)

  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    try:
      cursor.execute('''
        INSERT INTO usuarios (username, senha_hash, role)
        VALUES (?, ?, ?)
      ''', (username, senha_hash, role))
      conn.commit()
      print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
      print("Erro: Nome de usuário já existe.")

def fazer_login():
  username = input("Nome de Usário: ")
  senha = input("Senha: ")
  senha_hash = hash_senha(senha)

  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute('''
      SELECT id FROM usuarios
      WHERE username = ? AND senha_hash = ?
    ''', (username, senha_hash))
    usuario = cursor.fetchone()

    if usuario:
      print("Login Bem-sucedido!")
      return usuario[0]
    
    else:
      print("Usuário ou senha incorretos.")
      return None

def menu_principal(usuario_id):
  with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM usuarios WHERE id = ?", (usuario_id,))
    role = cursor.fetchone()[0]
  
  while True:
    print("\n--- Sistema de Gestão de Estoque ---")
    print("1. Listar Produtos")
    if role in ['admin', 'gerente']:
      print("2. Adicionar Produto")
      print("3. Registrar Movimentação")
      print("4. Modificar Preço do Produto")
    if role == ['admin']:
      print("5. Cadastrar Usuário")
    print("6. Sair")
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
      listar_produtos()
    elif opcao == "2" and role in ['admin', 'gerente']:
      adicionar_produto()
    elif opcao == "3" and role in ['admin', 'gerente']:
      registrar_movimentacao()
    elif opcao == "4" and role in ['admin', 'gerente']:
      modificar_preco()
    elif opcao == "5" and role in ['admin']:
      cadastrar_usuario()
    elif opcao == "6":
      print("Até Logo!")
      break
    else:
      print("Opção inválida ou não permitida para seu nível de acesso.")
  
      
def menu_autenticacao():
  while True:
    print("\n--- Autenticação ---")
    print("1. Fazer Login")
    print("2. Cadastrar Usuário")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")
  
    if opcao == "1":
      usuario_id = fazer_login()
      if usuario_id:
        menu_principal(usuario_id)
    elif opcao == "2":
      cadastrar_usuario()
    elif opcao == "3":
      print("Até Logo!")
      break
    else:
      print("Opção inválida. Tente novamente.")
  
def main():
  criar_tabela()
  menu_autenticacao()

if __name__ == "__main__":
  main()