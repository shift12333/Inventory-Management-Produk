class Validation:
    @staticmethod
    def validate_empty(value, field_name):
        """Memastikan input tidak kosong."""
        if not str(value).strip():
            raise ValueError(f"{field_name} tidak boleh kosong.")
        return str(value).strip()

    @staticmethod
    def validate_float(value, field_name):
        """Memastikan input berupa angka desimal dan tidak negatif."""
        try:
            val = float(value)
            if val < 0:
                raise ValueError(f"{field_name} tidak boleh bernilai negatif.")
            return val
        except ValueError as e:
            if "bernilai negatif" in str(e):
                raise
            raise ValueError(f"{field_name} harus berupa angka (contoh: 15000.50).")

    @staticmethod
    def validate_integer(value, field_name):
        """Memastikan input berupa bilangan bulat dan tidak negatif."""
        try:
            val = int(value)
            if val < 0:
                raise ValueError(f"{field_name} tidak boleh bernilai negatif.")
            return val
        except ValueError as e:
            if "bernilai negatif" in str(e):
                raise
            raise ValueError(f"{field_name} harus berupa angka bulat (contoh: 10).")

    @staticmethod
    def validate_product_input(product_id, name, category, price, stock, minimum_stock):
        """Memvalidasi semua isian form secara bersamaan."""
        Validation.validate_empty(product_id, "Product ID")
        Validation.validate_empty(name, "Nama produk")
        Validation.validate_empty(category, "Kategori")
        Validation.validate_float(price, "Harga")
        Validation.validate_integer(stock, "Stok")
        Validation.validate_integer(minimum_stock, "Minimum stok")
        return True
