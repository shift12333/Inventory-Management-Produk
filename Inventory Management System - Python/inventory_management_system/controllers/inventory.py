from models.models import Product

class Inventory:
    def __init__(self):
        # Composition: Inventory menyimpan collection dari object Product
        self.products = []

    def add_product(self, product):
        if self.product_id_exists(product.product_id):
            raise ValueError(f"Product ID '{product.product_id}' sudah terdaftar.")
        self.products.append(product)

    def remove_product(self, product_id):
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def find_product(self, product_id):
        """Mengembalikan object Product jika ID cocok."""
        for product in self.products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def update_product(self, product_id, name, category, price, stock, minimum_stock):
        """Memperbarui informasi produk tertentu."""
        product = self.find_product(product_id)
        if product:
            product.update_product(name, category, price, stock, minimum_stock)
            return True
        return False

    def search_products(self, keyword):
        """Mencari berdasarkan ID, nama, atau kategori produk."""
        keyword = str(keyword).lower()
        result = []
        for p in self.products:
            if (keyword in p.product_id.lower() or 
                keyword in p.name.lower() or 
                keyword in p.category.lower()):
                result.append(p)
        return result

    def get_all_products(self):
        return self.products

    def get_low_stock_products(self):
        """Mengembalikan daftar produk yang berstatus stok rendah."""
        return [p for p in self.products if p.is_low_stock()]

    def calculate_total_inventory_value(self):
        """Mengakumulasi total aset dari semua produk."""
        total = 0.0
        for p in self.products:
            total += p.get_total_value()
        return total

    def product_id_exists(self, product_id):
        return self.find_product(product_id) is not None
