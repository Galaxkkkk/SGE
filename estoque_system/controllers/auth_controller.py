import customtkinter as ctk
from models.user_model import UserModel
from views.auth_view import LoginView
from views.main_view import MainView

class AuthController:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.show_login_view()

    def show_login_view(self):
        """Mostra a tela de login"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.login_view = LoginView(self.root, self.authenticate)
        self.login_view.pack(fill=ctk.BOTH, expand=True)

    def authenticate(self, username, password):
        """Autentica o usuário"""
        self.current_user = UserModel.authenticate(username, password)
        
        if self.current_user:
            self.show_main_view()
            return True
        return False

    def show_main_view(self):
        """Mostra a tela principal após login bem-sucedido"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.main_view = MainView(
            self.root, 
            self.current_user,
            self.logout
        )
        self.main_view.pack(fill=ctk.BOTH, expand=True)

    def logout(self):
        """Realiza logout do usuário"""
        self.current_user = None
        self.show_login_view()