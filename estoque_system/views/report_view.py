import customtkinter as ctk
from tkinter.ttk import Treeview

class ReportView(ctk.CTkFrame):
    def __init__(self, parent, low_stock_products):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Relatório de Estoque Baixo", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        # Tabela de produtos com estoque baixo
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.tree = Treeview(
            table_frame,
            columns=("id", "name", "quantity", "min_quantity", "difference"),
            show="headings",
            selectmode="browse"
        )
        
        # Configurar colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nome")
        self.tree.heading("quantity", text="Quantidade Atual")
        self.tree.heading("min_quantity", text="Quantidade Mínima")
        self.tree.heading("difference", text="Faltam")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("quantity", width=120, anchor="center")
        self.tree.column("min_quantity", width=120, anchor="center")
        self.tree.column("difference", width=80, anchor="center")
        
        # Barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Preencher a tabela com os produtos
        self.update_report(low_stock_products)
        
        # Estilo para itens com estoque baixo
        self.tree.tag_configure("low_stock", background="#2d1e1e")

    def update_report(self, products):
        """Atualiza o relatório com os produtos fornecidos"""
        self.tree.delete(*self.tree.get_children())
        
        for product in products:
            difference = product[2] - product[3]
            self.tree.insert(
                "", "end", 
                values=(product[0], product[1], product[2], product[3], abs(difference)),
                tags=("low_stock",)
            )