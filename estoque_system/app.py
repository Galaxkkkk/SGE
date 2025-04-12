import customtkinter as ctk
from controllers.auth_controller import AuthController
from views.styles import configure_styles

def main():
    # Configuração da aparência
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Configurar estilos personalizados
    configure_styles()
    
    # Criar a janela principal
    root = ctk.CTk()
    root.title("Sistema de Gerenciamento de Estoque")
    root.geometry("800x600")
    
    # Iniciar o controlador de autenticação
    auth_controller = AuthController(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()