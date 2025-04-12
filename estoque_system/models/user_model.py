from models.database import create_connection
import hashlib

class UserModel:
    @staticmethod
    def authenticate(username, password):
        """Autentica um usuário"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                
                # Hash da senha (simples - em produção use algo mais seguro como bcrypt)
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                cursor.execute('''
                    SELECT id, username, full_name, is_admin 
                    FROM users 
                    WHERE username = ? AND password = ?
                ''', (username, hashed_password))
                
                user = cursor.fetchone()
                
                if user:
                    return {
                        'id': user[0],
                        'username': user[1],
                        'full_name': user[2],
                        'is_admin': bool(user[3])
                    }
                return None
            except Exception as e:
                print(f"Erro ao autenticar usuário: {e}")
                return None
            finally:
                conn.close()
        return None

    @staticmethod
    def get_all_users():
        """Obtém todos os usuários"""
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, full_name, is_admin FROM users')
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao obter usuários: {e}")
                return []
            finally:
                conn.close()
        return []