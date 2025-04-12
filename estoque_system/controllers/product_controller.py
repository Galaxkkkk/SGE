from models.product_model import ProductModel
from views.product_view import ProductView, AddProductView, EditProductView

class ProductController:
    def __init__(self, parent_frame, user):
        self.parent_frame = parent_frame
        self.user = user
        self.product_view = None
        self.show_product_list()

    def show_product_list(self):
        """Mostra a lista de produtos"""
        if self.product_view:
            self.product_view.destroy()
        
        products = ProductModel.get_all_products()
        self.product_view = ProductView(
            self.parent_frame,
            products,
            self.show_add_product,
            self.show_edit_product,
            self.delete_product
        )
        self.product_view.pack(fill="both", expand=True)

    def show_add_product(self):
        """Mostra o formulário para adicionar produto"""
        add_view = AddProductView(
            self.parent_frame,
            self.add_product,
            self.show_product_list
        )
        self.product_view.pack_forget()
        add_view.pack(fill="both", expand=True)

    def show_edit_product(self, product_id):
        """Mostra o formulário para editar produto"""
        products = ProductModel.get_all_products()
        product = next((p for p in products if p[0] == product_id), None)
        
        if product:
            edit_view = EditProductView(
                self.parent_frame,
                product,
                self.update_product,
                self.show_product_list
            )
            self.product_view.pack_forget()
            edit_view.pack(fill="both", expand=True)

    def add_product(self, product_data):
        """Adiciona um novo produto"""
        success = ProductModel.add_product(
            product_data['name'],
            product_data['description'],
            product_data['quantity'],
            product_data['min_quantity'],
            product_data['price'],
            product_data['category']
        )
        
        if success is not None:
            self.show_product_list()
            return True
        return False

    def update_product(self, product_id, product_data):
        """Atualiza um produto existente"""
        success = ProductModel.update_product(
            product_id,
            product_data['name'],
            product_data['description'],
            product_data['quantity'],
            product_data['min_quantity'],
            product_data['price'],
            product_data['category']
        )
        
        if success:
            self.show_product_list()
            return True
        return False

    def delete_product(self, product_id):
        """Remove um produto"""
        success = ProductModel.delete_product(product_id)
        if success:
            self.show_product_list()
        return success