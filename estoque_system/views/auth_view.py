import customtkinter as ctk
from tkinter import messagebox

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.login_callback = login_callback
        
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, width=400)
        main_frame.pack(pady=100, padx=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Login", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30), sticky="n")
        
        # Formulário
        self.username_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Usuário"
        )
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.password_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Senha", 
            show="*"
        )
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        login_button = ctk.CTkButton(
            main_frame, 
            text="Entrar", 
            command=self.on_login
        )
        login_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda e: self.on_login())

    def on_login(self):
        """Lida com a tentativa de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return
        
        if self.login_callback(username, password):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")
            self.password_entry.delete(0, "end")