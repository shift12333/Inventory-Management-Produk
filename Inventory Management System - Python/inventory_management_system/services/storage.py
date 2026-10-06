import json
import os
from models.models import Product, ElectronicsProduct, FoodProduct

class StorageManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def save_data(self, products):
        """Menyimpan list object Product ke dalam file JSON."""
        try:
            data = [p.to_dict() for p in products]
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error menyimpan data: {e}")

    def load_data(self):
        """Membaca file JSON dan mengembalikan list object Product."""
        if not os.path.exists(self.file_name):
            # Buat file kosong jika belum ada
            self.save_data([])
            return []

        products = []
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    item_type = item.get("type", "general")
                    
                    if item_type == "electronics":
                        product = ElectronicsProduct(
                            item["product_id"], item["name"], item["category"],
                            item["price"], item["stock"], item["minimum_stock"],
                            item.get("warranty_period", 12)
                        )
                    elif item_type == "food":
                        product = FoodProduct(
                            item["product_id"], item["name"], item["category"],
                            item["price"], item["stock"], item["minimum_stock"],
                            item.get("expiry_date", "2099-12-31")
                        )
                    else:
                        product = Product.from_dict(item)
                        
                    products.append(product)
        except json.JSONDecodeError:
            print(f"Error: Format file JSON '{self.file_name}' rusak.")
            return []
        except Exception as e:
            print(f"Error memuat data: {e}")
            return []

        return products
