from models.database import create_connection
from datetime import datetime

class ProductModel:
    @staticmethod
    def get_all_products():
        """Obtém todos os produtos"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, description, quantity, min_quantity, price, category 
                    FROM products
                    ORDER BY name
                ''')
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao obter produtos: {e}")
                return []
            finally:
                conn.close()
        return []

    @staticmethod
    def add_product(name, description, quantity, min_quantity, price, category):
        """Adiciona um novo produto"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products (name, description, quantity, min_quantity, price, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, description, quantity, min_quantity, price, category))
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Erro ao adicionar produto: {e}")
                conn.rollback()
                return None
            finally:
                conn.close()
        return None

    @staticmethod
    def update_product(product_id, name, description, quantity, min_quantity, price, category):
        """Atualiza um produto existente"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE products 
                    SET name = ?, description = ?, quantity = ?, min_quantity = ?, price = ?, category = ?, updated_at = ?
                    WHERE id = ?
                ''', (name, description, quantity, min_quantity, price, category, datetime.now(), product_id))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Erro ao atualizar produto: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def delete_product(product_id):
        """Remove um produto"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Erro ao remover produto: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def get_low_stock_products():
        """Obtém produtos com estoque abaixo do mínimo"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, quantity, min_quantity 
                    FROM products 
                    WHERE quantity < min_quantity
                    ORDER BY (min_quantity - quantity) DESC
                ''')
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao obter produtos com estoque baixo: {e}")
                return []
            finally:
                conn.close()
        return []