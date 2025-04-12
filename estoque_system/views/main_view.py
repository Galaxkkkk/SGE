import customtkinter as ctk
from tkinter import messagebox
from views.product_view import ProductView
from views.report_view import ReportView

class MainView(ctk.CTkFrame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        
        self.configure(fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Barra de navegação superior
        self.create_navbar()
        
        # Frame de conteúdo
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Mostrar a view de produtos por padrão
        self.show_products_view()

    def create_navbar(self):
        """Cria a barra de navegação superior"""
        navbar = ctk.CTkFrame(self, height=50)
        navbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        navbar.grid_columnconfigure(0, weight=1)
        
        # Botões de navegação
        nav_buttons = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_buttons.grid(row=0, column=0, sticky="w")
        
        products_btn = ctk.CTkButton(
            nav_buttons, 
            text="Produtos", 
            command=self.show_products_view,
            width=100
        )
        products_btn.grid(row=0, column=0, padx=5)
        
        reports_btn = ctk.CTkButton(
            nav_buttons, 
            text="Relatórios", 
            command=self.show_reports_view,
            width=100
        )
        reports_btn.grid(row=0, column=1, padx=5)
        
        # Área do usuário e logout
        user_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        user_frame.grid(row=0, column=1, sticky="e")
        
        user_label = ctk.CTkLabel(
            user_frame, 
            text=f"Bem-vindo, {self.user['full_name']}"
        )
        user_label.grid(row=0, column=0, padx=10)
        
        logout_btn = ctk.CTkButton(
            user_frame, 
            text="Sair", 
            command=self.logout,
            width=80,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        logout_btn.grid(row=0, column=1)

    def show_products_view(self):
        """Mostra a view de produtos"""
        from controllers.product_controller import ProductController
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.product_controller = ProductController(self.content_frame, self.user)

    def show_reports_view(self):
        """Mostra a view de relatórios"""
        from controllers.report_controller import ReportController
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.report_controller = ReportController(self.content_frame)

    def logout(self):
        """Realiza logout"""
        self.logout_callback()