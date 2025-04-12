import sqlite3
from pathlib import Path
import hashlib

DB_PATH = Path(__file__).parent / "database.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
    return conn

def insert_sample_products():
    """Insere produtos de exemplo no banco de dados"""
    sample_products = [
        # (nome, descrição, quantidade, quantidade_mínima, preço, categoria)
        ("Arroz Branco", "Arroz tipo 1, pacote 5kg", 50, 20, 22.90, "Grãos e Cereais"),
        ("Feijão Carioca", "Feijão carioca, pacote 1kg", 40, 15, 8.99, "Grãos e Cereais"),
        ("Açúcar Refinado", "Açúcar refinado, pacote 5kg", 30, 10, 15.50, "Mercearia"),
        ("Óleo de Soja", "Óleo de soja, garrafa 900ml", 60, 25, 7.49, "Mercearia"),
        ("Leite UHT", "Leite integral, caixa 1L", 100, 40, 4.29, "Laticínios"),
        ("Ovos", "Ovos brancos, cartela com 12", 80, 30, 12.90, "Laticínios"),
        ("Pão de Forma", "Pão de forma integral, pacote 500g", 45, 20, 9.99, "Padaria"),
        ("Café em Pó", "Café torrado e moído, pacote 500g", 35, 15, 18.90, "Mercearia"),
        ("Sabão em Pó", "Sabão em pó para roupas, 1kg", 25, 10, 14.99, "Limpeza"),
        ("Detergente", "Detergente líquido, 500ml", 55, 20, 2.49, "Limpeza"),
        ("Shampoo", "Shampoo para cabelos normais, 350ml", 40, 15, 16.90, "Higiene"),
        ("Escova de Dentes", "Escova de dentes macia", 65, 25, 5.99, "Higiene"),
        ("Desinfetante", "Desinfetante pinho, 1L", 30, 12, 6.90, "Limpeza"),
        ("Papel Higiênico", "Rolo duplo, pacote com 16", 70, 30, 24.99, "Higiene"),
        ("Macarrão Espaguete", "Macarrão espaguete, pacote 500g", 50, 20, 4.79, "Mercearia"),
        ("Molho de Tomate", "Molho de tomate tradicional, sachê 340g", 60, 25, 3.29, "Mercearia"),
        ("Farinha de Trigo", "Farinha de trigo, pacote 1kg", 40, 15, 5.49, "Mercearia"),
        ("Sal Refinado", "Sal refinado, pacote 1kg", 45, 20, 2.99, "Mercearia"),
        ("Creme Dental", "Creme dental com flúor, 90g", 75, 30, 3.99, "Higiene"),
        ("Sabonete", "Sabonete líquido, frasco 250ml", 50, 20, 6.49, "Higiene")
    ]
    
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Verifica se já existem produtos para não duplicar
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            
            if count == 0:
                for product in sample_products:
                    cursor.execute('''
                        INSERT INTO products (name, description, quantity, min_quantity, price, category)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', product)
                
                conn.commit()
                print(f"{len(sample_products)} produtos de exemplo foram cadastrados!")
            else:
                print("Banco já contém produtos. Nenhum produto de exemplo foi adicionado.")
        except sqlite3.Error as e:
            print(f"Erro ao inserir produtos de exemplo: {e}")
            conn.rollback()
        finally:
            conn.close()

def init_db():
    conn = create_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    is_admin INTEGER DEFAULT 0
                )
            ''')
            
            # Tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    quantity INTEGER NOT NULL,
                    min_quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Hash da senha admin (SHA-256 de "admin123")
            admin_password = hashlib.sha256("admin123".encode()).hexdigest()
            
            # Inserir usuário admin se não existir
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, full_name, is_admin)
                VALUES (?, ?, ?, ?)
            ''', ('admin', admin_password, 'Administrador', 1))
            
            conn.commit()
            print("Banco de dados inicializado com sucesso!")
            
            # Inserir produtos de exemplo após criar as tabelas
            insert_sample_products()
            
        except sqlite3.Error as e:
            print(f"Erro ao inicializar o banco: {e}")
            conn.rollback()
        finally:
            conn.close()

init_db()