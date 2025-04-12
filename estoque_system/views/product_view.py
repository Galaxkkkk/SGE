import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
import tkinter as tk

class ProductView(ctk.CTkFrame):
    def __init__(self, parent, products, add_callback, edit_callback, delete_callback):
        super().__init__(parent)
        self.add_callback = add_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        self.configure(fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Barra de ferramentas
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        toolbar.grid_columnconfigure(0, weight=1)
        
        add_btn = ctk.CTkButton(
            toolbar, 
            text="+ Adicionar Produto", 
            command=self.add_callback,
            width=150
        )
        add_btn.grid(row=0, column=0, sticky="w")
        
        # Tabela de produtos
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview para exibir os produtos
        self.tree = Treeview(
            table_frame,
            columns=("id", "name", "quantity", "min_quantity", "price", "category"),
            show="headings",
            selectmode="browse"
        )
        
        # Configurar colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nome")
        self.tree.heading("quantity", text="Quantidade")
        self.tree.heading("min_quantity", text="Mínimo")
        self.tree.heading("price", text="Preço")
        self.tree.heading("category", text="Categoria")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("quantity", width=80, anchor="center")
        self.tree.column("min_quantity", width=80, anchor="center")
        self.tree.column("price", width=100, anchor="center")
        self.tree.column("category", width=150)
        
        # Barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Preencher a tabela com os produtos
        self.update_products(products)
        
        # Botões de ação
        action_frame = ctk.CTkFrame(self)
        action_frame.grid(row=2, column=0, sticky="e", pady=(10, 0))
        
        edit_btn = ctk.CTkButton(
            action_frame, 
            text="Editar", 
            command=self.on_edit,
            width=100
        )
        edit_btn.grid(row=0, column=0, padx=5)
        
        delete_btn = ctk.CTkButton(
            action_frame, 
            text="Excluir", 
            command=self.on_delete,
            width=100,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        delete_btn.grid(row=0, column=1, padx=5)

    def update_products(self, products):
        """Atualiza a lista de produtos na tabela"""
        self.tree.delete(*self.tree.get_children())
        
        for product in products:
            # Formatar preço
            price = f"R$ {product[5]:.2f}"
            
            # Destacar produtos com estoque baixo
            tags = ()
            if product[3] < product[4]:
                tags = ("low_stock",)
            
            self.tree.insert(
                "", "end", 
                values=(product[0], product[1], product[3], product[4], price, product[6]),
                tags=tags
            )
        
        # Configurar estilo para itens com estoque baixo
        self.tree.tag_configure("low_stock", background="#2d1e1e")

    def get_selected_product(self):
        """Obtém o produto selecionado na tabela"""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0], "values")

    def on_edit(self):
        """Lida com a edição de produto"""
        product = self.get_selected_product()
        if product:
            self.edit_callback(int(product[0]))
        else:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")

    def on_delete(self):
        """Lida com a exclusão de produto"""
        product = self.get_selected_product()
        if product:
            if messagebox.askyesno(
                "Confirmar", 
                f"Tem certeza que deseja excluir o produto {product[1]}?"
            ):
                success = self.delete_callback(int(product[0]))
                if success:
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso")
        else:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir")

class AddProductView(ctk.CTkFrame):
    def __init__(self, parent, add_callback, cancel_callback):
        super().__init__(parent)
        self.add_callback = add_callback
        self.cancel_callback = cancel_callback
        
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(self, width=500)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(
            form_frame, 
            text="Adicionar Produto", 
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Nome:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ctk.CTkEntry(form_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Descrição:").grid(row=2, column=0, sticky="w", pady=5)
        self.desc_entry = ctk.CTkEntry(form_frame)
        self.desc_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Quantidade:").grid(row=3, column=0, sticky="w", pady=5)
        self.quantity_entry = ctk.CTkEntry(form_frame)
        self.quantity_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Quantidade Mínima:").grid(row=4, column=0, sticky="w", pady=5)
        self.min_quantity_entry = ctk.CTkEntry(form_frame)
        self.min_quantity_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Preço:").grid(row=5, column=0, sticky="w", pady=5)
        self.price_entry = ctk.CTkEntry(form_frame)
        self.price_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Categoria:").grid(row=6, column=0, sticky="w", pady=5)
        self.category_entry = ctk.CTkEntry(form_frame)
        self.category_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Botões
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame, 
            text="Salvar", 
            command=self.on_save,
            width=100
        )
        save_btn.grid(row=0, column=0, padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self.cancel_callback,
            width=100,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        cancel_btn.grid(row=0, column=1, padx=10)

    def on_save(self):
        """Lida com o salvamento do novo produto"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        min_quantity = self.min_quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()
        
        # Validação básica
        if not name or not quantity or not min_quantity or not price:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios")
            return
        
        try:
            quantity = int(quantity)
            min_quantity = int(min_quantity)
            price = float(price)
            
            if quantity < 0 or min_quantity < 0 or price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos para quantidade ou preço")
            return
        
        product_data = {
            'name': name,
            'description': description,
            'quantity': quantity,
            'min_quantity': min_quantity,
            'price': price,
            'category': category
        }
        
        if self.add_callback(product_data):
            self.cancel_callback()

class EditProductView(ctk.CTkFrame):
    def __init__(self, parent, product, update_callback, cancel_callback):
        super().__init__(parent)
        self.product_id = product[0]
        self.update_callback = update_callback
        self.cancel_callback = cancel_callback
        
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(self, width=500)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(
            form_frame, 
            text="Editar Produto", 
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Nome:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ctk.CTkEntry(form_frame)
        self.name_entry.insert(0, product[1])
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Descrição:").grid(row=2, column=0, sticky="w", pady=5)
        self.desc_entry = ctk.CTkEntry(form_frame)
        self.desc_entry.insert(0, product[2] if product[2] else "")
        self.desc_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Quantidade:").grid(row=3, column=0, sticky="w", pady=5)
        self.quantity_entry = ctk.CTkEntry(form_frame)
        self.quantity_entry.insert(0, str(product[3]))
        self.quantity_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Quantidade Mínima:").grid(row=4, column=0, sticky="w", pady=5)
        self.min_quantity_entry = ctk.CTkEntry(form_frame)
        self.min_quantity_entry.insert(0, str(product[4]))
        self.min_quantity_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Preço:").grid(row=5, column=0, sticky="w", pady=5)
        self.price_entry = ctk.CTkEntry(form_frame)
        self.price_entry.insert(0, str(product[5]))
        self.price_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Categoria:").grid(row=6, column=0, sticky="w", pady=5)
        self.category_entry = ctk.CTkEntry(form_frame)
        self.category_entry.insert(0, product[6] if product[6] else "")
        self.category_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Botões
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame, 
            text="Salvar", 
            command=self.on_save,
            width=100
        )
        save_btn.grid(row=0, column=0, padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self.cancel_callback,
            width=100,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        cancel_btn.grid(row=0, column=1, padx=10)

    def on_save(self):
        """Lida com a atualização do produto"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        min_quantity = self.min_quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()
        
        # Validação básica
        if not name or not quantity or not min_quantity or not price:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios")
            return
        
        try:
            quantity = int(quantity)
            min_quantity = int(min_quantity)
            price = float(price)
            
            if quantity < 0 or min_quantity < 0 or price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos para quantidade ou preço")
            return
        
        product_data = {
            'name': name,
            'description': description,
            'quantity': quantity,
            'min_quantity': min_quantity,
            'price': price,
            'category': category
        }
        
        if self.update_callback(self.product_id, product_data):
            self.cancel_callback()