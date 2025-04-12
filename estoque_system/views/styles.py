import customtkinter as ctk

def configure_styles():
    """Configura estilos personalizados para os widgets"""
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)
    
    # Estilo para botões principais
    ctk.ThemeManager.theme["CTkButton"]["corner_radius"] = 6
    ctk.ThemeManager.theme["CTkButton"]["border_width"] = 1
    ctk.ThemeManager.theme["CTkButton"]["fg_color"] = "#2b5b84"
    ctk.ThemeManager.theme["CTkButton"]["hover_color"] = "#1e3d59"
    ctk.ThemeManager.theme["CTkButton"]["border_color"] = "#1e3d59"
    ctk.ThemeManager.theme["CTkButton"]["text_color"] = "#ffffff"
    
    # Estilo para botões secundários
    ctk.ThemeManager.theme["CTkButton"]["secondary_fg_color"] = "#3a3a3a"
    ctk.ThemeManager.theme["CTkButton"]["secondary_hover_color"] = "#2d2d2d"
    ctk.ThemeManager.theme["CTkButton"]["secondary_border_color"] = "#2d2d2d"
    
    # Estilo para entradas
    ctk.ThemeManager.theme["CTkEntry"]["corner_radius"] = 4
    ctk.ThemeManager.theme["CTkEntry"]["border_width"] = 1
    ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = "#343638"
    ctk.ThemeManager.theme["CTkEntry"]["border_color"] = "#565b5e"
    
    # Estilo para frames
    ctk.ThemeManager.theme["CTkFrame"]["corner_radius"] = 6
    ctk.ThemeManager.theme["CTkFrame"]["border_width"] = 1
    ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = "#2b2b2b"
    ctk.ThemeManager.theme["CTkFrame"]["border_color"] = "#3a3a3a"
    
    # Estilo para labels
    ctk.ThemeManager.theme["CTkLabel"]["text_color"] = "#ffffff"
    
    # Estilo para combobox
    ctk.ThemeManager.theme["CTkComboBox"]["corner_radius"] = 4
    ctk.ThemeManager.theme["CTkComboBox"]["border_width"] = 1
    ctk.ThemeManager.theme["CTkComboBox"]["fg_color"] = "#343638"
    ctk.ThemeManager.theme["CTkComboBox"]["border_color"] = "#565b5e"
    ctk.ThemeManager.theme["CTkComboBox"]["button_color"] = "#565b5e"
    ctk.ThemeManager.theme["CTkComboBox"]["button_hover_color"] = "#4a4f52"