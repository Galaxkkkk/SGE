from models.product_model import ProductModel
from views.report_view import ReportView

class ReportController:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.report_view = None
        self.show_reports()

    def show_reports(self):
        """Mostra os relatórios"""
        if self.report_view:
            self.report_view.destroy()
        
        low_stock = ProductModel.get_low_stock_products()
        self.report_view = ReportView(self.parent_frame, low_stock)
        self.report_view.pack(fill="both", expand=True)