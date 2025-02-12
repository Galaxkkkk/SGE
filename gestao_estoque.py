import sqlite3
from datetime import datetime

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

def menu():
  print("\n--- Sistema de Gestão de Estoque ---")
  print("1. Adicionar Produto")
  print("2. Listar Produtos")
  print("3. Registrar Movimentação")
  print("4. Listar Estoque Baixo")
  print("5. Sair")
  return input("Escolha uma opção: ")

def main():
  criar_tabela()
  
  while True:
    opcao = menu()
    
    if opcao == "1":
      adicionar_produto()
    elif opcao == "2":
      listar_produtos()
    elif opcao == "3":
      registrar_movimentacao()
    elif opcao == "4":
      listar_estoque_baixo()
    elif opcao == "5":
      print("Até logo!")
      break
    
    else:
      print("Opção inválida. Tente Novamente.")
      
if __name__ == "__main__":
  main()