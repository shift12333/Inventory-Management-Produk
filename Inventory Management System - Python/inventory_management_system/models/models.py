class Product:
    def __init__(self, product_id, name, category, price, stock, minimum_stock):
        self._product_id = str(product_id)
        self._name = str(name)
        self._category = str(category)
        self._price = float(price)
        self._stock = int(stock)
        self._minimum_stock = int(minimum_stock)
    
    # Getter methods (Encapsulation)
    @property
    def product_id(self): return self._product_id
    
    @property
    def name(self): return self._name
    
    @property
    def category(self): return self._category
    
    @property
    def price(self): return self._price
    
    @property
    def stock(self): return self._stock
    
    @property
    def minimum_stock(self): return self._minimum_stock

    def update_product(self, name, category, price, stock, minimum_stock):
        self._name = str(name)
        self._category = str(category)
        self._price = float(price)
        self._stock = int(stock)
        self._minimum_stock = int(minimum_stock)

    def add_stock(self, quantity):
        if quantity > 0:
            self._stock += quantity

    def reduce_stock(self, quantity):
        if quantity > 0 and self._stock >= quantity:
            self._stock -= quantity

    def is_low_stock(self):
        """Mengecek apakah stok di bawah atau sama dengan minimum stok."""
        return self._stock <= self._minimum_stock

    def get_stock_status(self):
        """Mengembalikan status persediaan berdasarkan jumlah."""
        return "Low Stock" if self.is_low_stock() else "Available"

    def get_total_value(self):
        """Menghitung total nilai aset dari produk ini."""
        return self._price * self._stock

    def to_dict(self):
        """Mengonversi object menjadi dictionary untuk format JSON."""
        return {
            "type": "general",
            "product_id": self._product_id,
            "name": self._name,
            "category": self._category,
            "price": self._price,
            "stock": self._stock,
            "minimum_stock": self._minimum_stock
        }

    @classmethod
    def from_dict(cls, data):
        """Membuat instance object dari data dictionary."""
        return cls(
            data["product_id"],
            data["name"],
            data["category"],
            data["price"],
            data["stock"],
            data["minimum_stock"]
        )

# Inheritance (Pewarisan)
class ElectronicsProduct(Product):
    def __init__(self, product_id, name, category, price, stock, minimum_stock, warranty_period):
        # Memanggil constructor superclass
        super().__init__(product_id, name, category, price, stock, minimum_stock)
        self._warranty_period = int(warranty_period)

    @property
    def warranty_period(self): return self._warranty_period

    def get_warranty_info(self):
        return f"Garansi {self._warranty_period} bulan"

    # Polymorphism: Meng-override fungsi to_dict dari parent class
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "electronics"
        data["warranty_period"] = self._warranty_period
        return data

# Inheritance (Pewarisan)
class FoodProduct(Product):
    def __init__(self, product_id, name, category, price, stock, minimum_stock, expiry_date):
        super().__init__(product_id, name, category, price, stock, minimum_stock)
        self._expiry_date = str(expiry_date) # YYYY-MM-DD

    @property
    def expiry_date(self): return self._expiry_date

    def is_expired(self):
        # Pendekatan sederhana untuk mengecek expired,
        # Untuk kasus nyata biasanya menggunakan module datetime
        from datetime import datetime
        try:
            exp_date = datetime.strptime(self._expiry_date, "%Y-%m-%d")
            return datetime.now() > exp_date
        except ValueError:
            return False

    # Polymorphism: Meng-override fungsi to_dict dari parent class
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "food"
        data["expiry_date"] = self._expiry_date
        return data
