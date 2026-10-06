import os
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.inventory import Inventory
from services.storage import StorageManager
from controllers.validation import Validation
from models.models import Product

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Stok Barang (OOP)")
        self.root.geometry("1000x650")
        # Padding di sekeliling window
        self.root.configure(padx=10, pady=10)

        # Inisialisasi logika OOP (Inventory, Storage)
        self.inventory = Inventory()
        
        # Menggunakan path absolut agar tidak error jika dijalankan dari direktori luar
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "products.json")
        
        self.storage_manager = StorageManager(data_path)
        self.load_products()

        # Variabel untuk menampung input user (StringVars)
        self.entry_product_id = tk.StringVar()
        self.entry_name = tk.StringVar()
        self.entry_category = tk.StringVar()
        self.entry_price = tk.StringVar()
        self.entry_stock = tk.StringVar()
        self.entry_minimum_stock = tk.StringVar()
        self.entry_search = tk.StringVar()

        # Membangun antarmuka
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Frame atas (Mencakup form input dan tombol aksi)
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=5)

        self.create_form_frame(top_frame)
        
        # Frame tengah untuk pencarian
        self.create_search_frame()

        # Frame bawah untuk tabel data
        self.create_table_frame()

        # Label total nilai di paling bawah
        self.total_value_label = tk.Label(self.root, text="Total Nilai Inventaris: Rp 0", font=("Arial", 12, "bold"))
        self.total_value_label.pack(anchor="e", pady=10)
        self.update_total_value_label()

    def create_form_frame(self, parent):
        """Membuat komponen input form di sebelah kiri frame atas."""
        form_frame = tk.LabelFrame(parent, text="Form Data Produk", padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        labels = ["Product ID", "Nama", "Kategori", "Harga", "Stok", "Minimum Stok"]
        variables = [self.entry_product_id, self.entry_name, self.entry_category, 
                     self.entry_price, self.entry_stock, self.entry_minimum_stock]

        # Membuat label dan input secara dinamis
        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
            tk.Entry(form_frame, textvariable=var, width=35).grid(row=i, column=1, pady=2, padx=10)

        # Tambahkan frame tombol di sebelah kanan form_frame
        self.create_button_frame(parent)

    def create_button_frame(self, parent):
        """Membuat deretan tombol aksi di sebelah kanan frame atas."""
        btn_frame = tk.LabelFrame(parent, text="Aksi", padx=10, pady=10)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

        tk.Button(btn_frame, text="Add Product", width=15, bg="#4CAF50", fg="white", 
                  command=self.add_product_handler).pack(pady=5)
        tk.Button(btn_frame, text="Update Product", width=15, bg="#2196F3", fg="white", 
                  command=self.update_product_handler).pack(pady=5)
        tk.Button(btn_frame, text="Delete Product", width=15, bg="#F44336", fg="white", 
                  command=self.delete_product_handler).pack(pady=5)
        tk.Button(btn_frame, text="Clear Form", width=15, bg="#9E9E9E", fg="white", 
                  command=self.clear_form).pack(pady=5)

    def create_search_frame(self):
        """Membuat kolom pencarian dan tombol filter stok rendah."""
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, pady=10)

        tk.Label(search_frame, text="Cari Produk:").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.entry_search, width=40).pack(side=tk.LEFT, padx=10)
        tk.Button(search_frame, text="Search", command=self.search_product_handler).pack(side=tk.LEFT, padx=2)
        tk.Button(search_frame, text="Reset", command=self.reset_search_handler).pack(side=tk.LEFT, padx=2)
        
        # Tombol notifikasi stok rendah ditaruh di sisi kanan
        tk.Button(search_frame, text="Cek Stok Rendah", bg="#FF9800", fg="white", 
                  command=self.show_low_stock_warning).pack(side=tk.RIGHT, padx=2)

    def create_table_frame(self):
        """Membuat tabel Treeview untuk menampilkan daftar produk."""
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Nama", "Kategori", "Harga", "Stok", "Min Stok", "Status", "Total")
        self.product_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Set teks heading
        for col in columns:
            self.product_table.heading(col, text=col)

        # Set lebar kolom
        self.product_table.column("ID", width=80, anchor="center")
        self.product_table.column("Nama", width=200, anchor="w")
        self.product_table.column("Kategori", width=120, anchor="w")
        self.product_table.column("Harga", width=100, anchor="e")
        self.product_table.column("Stok", width=60, anchor="center")
        self.product_table.column("Min Stok", width=60, anchor="center")
        self.product_table.column("Status", width=100, anchor="center")
        self.product_table.column("Total", width=120, anchor="e")

        # Pasang scrollbar vertikal
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.product_table.yview)
        self.product_table.configure(yscroll=scrollbar.set)

        self.product_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind klik baris tabel untuk mengisi form
        self.product_table.bind("<ButtonRelease-1>", self.fill_form_from_table)
        
        # Konfigurasi pewarnaan row Treeview (Polymorphism UI)
        self.product_table.tag_configure("low_stock", background="#ffcccc")
        self.product_table.tag_configure("available", background="#ffffff")

    # ==========================
    # EVENT HANDLERS
    # ==========================
    
    def add_product_handler(self):
        try:
            # 1. Validasi Input melalui class Validation
            Validation.validate_product_input(
                self.entry_product_id.get(), self.entry_name.get(), self.entry_category.get(),
                self.entry_price.get(), self.entry_stock.get(), self.entry_minimum_stock.get()
            )

            # 2. Pembuatan Object Product
            product = Product(
                self.entry_product_id.get(), self.entry_name.get(), self.entry_category.get(),
                self.entry_price.get(), self.entry_stock.get(), self.entry_minimum_stock.get()
            )

            # 3. Penambahan object ke Inventory
            self.inventory.add_product(product)
            
            # 4. Simpan ke JSON & perbarui tampilan
            self.save_products()
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
            
        except ValueError as e:
            # Exception Handling: Menangkap error validasi dan file exist
            messagebox.showerror("Error", str(e))

    def update_product_handler(self):
        try:
            prod_id = self.entry_product_id.get()
            if not prod_id:
                raise ValueError("Silakan pilih produk dari tabel terlebih dahulu.")

            # Validasi input kembali
            Validation.validate_product_input(
                prod_id, self.entry_name.get(), self.entry_category.get(),
                self.entry_price.get(), self.entry_stock.get(), self.entry_minimum_stock.get()
            )

            # Lakukan pembaruan
            success = self.inventory.update_product(
                prod_id, self.entry_name.get(), self.entry_category.get(),
                self.entry_price.get(), self.entry_stock.get(), self.entry_minimum_stock.get()
            )

            if success:
                self.save_products()
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Sukses", "Data produk berhasil diubah!")
            else:
                messagebox.showerror("Error", "Product ID tidak ditemukan di inventaris.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_product_handler(self):
        prod_id = self.entry_product_id.get()
        if not prod_id:
            messagebox.showwarning("Peringatan", "Pilih produk dari tabel terlebih dahulu.")
            return

        confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus produk ID '{prod_id}'?")
        if confirm:
            if self.inventory.remove_product(prod_id):
                self.save_products()
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Gagal menghapus produk.")

    def search_product_handler(self):
        keyword = self.entry_search.get()
        if not keyword:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian.")
            return
        
        results = self.inventory.search_products(keyword)
        self.refresh_table(results)

    def reset_search_handler(self):
        self.entry_search.set("")
        self.refresh_table()

    def clear_form(self):
        self.entry_product_id.set("")
        self.entry_name.set("")
        self.entry_category.set("")
        self.entry_price.set("")
        self.entry_stock.set("")
        self.entry_minimum_stock.set("")
        
    def fill_form_from_table(self, event):
        """Mengisi form input dengan data dari baris Treeview yang diklik."""
        selected_row = self.product_table.focus()
        if not selected_row:
            return
        
        data = self.product_table.item(selected_row, "values")
        if data:
            self.entry_product_id.set(data[0])
            self.entry_name.set(data[1])
            self.entry_category.set(data[2])
            
            # Hilangkan koma dari format uang untuk dimasukkan ke Entry
            price_clean = data[3].replace(",", "")
            self.entry_price.set(price_clean)
            
            self.entry_stock.set(data[4])
            self.entry_minimum_stock.set(data[5])

    # ==========================
    # LOGIKA UI TAMBAHAN
    # ==========================

    def refresh_table(self, products=None):
        """Memuat ulang semua item di Treeview sesuai dengan data."""
        # Bersihkan tabel lama
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        
        # Ambil produk jika tidak ada argumen spesifik (contoh saat bukan searching)
        target_products = products if products is not None else self.inventory.get_all_products()

        for p in target_products:
            # Gunakan behavior polimorfik atau method Product
            status = p.get_stock_status()
            tag = "low_stock" if p.is_low_stock() else "available"
            
            self.product_table.insert("", "end", values=(
                p.product_id, 
                p.name, 
                p.category, 
                f"{p.price:,.2f}", 
                p.stock, 
                p.minimum_stock, 
                status, 
                f"{p.get_total_value():,.2f}"
            ), tags=(tag,))
        
        self.update_total_value_label()

    def update_total_value_label(self):
        total = self.inventory.calculate_total_inventory_value()
        self.total_value_label.config(text=f"Total Nilai Inventaris: Rp {total:,.2f}")

    def show_low_stock_warning(self):
        """Mem-filter tabel hanya untuk produk yang perlu dire-stock."""
        low_stock_products = self.inventory.get_low_stock_products()
        if low_stock_products:
            self.refresh_table(low_stock_products)
            messagebox.showwarning("Peringatan Stok Rendah", 
                                   f"Terdapat {len(low_stock_products)} produk dengan stok rendah/habis.")
        else:
            self.refresh_table() # Kembali ke view normal
            messagebox.showinfo("Informasi Stok", "Semua stok produk dalam kondisi aman.")

    def save_products(self):
        """Delegasi tugas simpan ke StorageManager."""
        self.storage_manager.save_data(self.inventory.get_all_products())

    def load_products(self):
        """Delegasi tugas load ke StorageManager, lalu populate Inventory."""
        products = self.storage_manager.load_data()
        for p in products:
            self.inventory.add_product(p)
