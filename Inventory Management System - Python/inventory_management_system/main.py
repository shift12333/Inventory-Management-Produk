import tkinter as tk
from views.app import InventoryApp

def main():
    root = tk.Tk()
    
    # Pengaturan gaya (Style) ttk agar lebih rapi dari default
    style = tk.ttk.Style(root)
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    
    # Inisialisasi Aplikasi utama (Controller/GUI)
    app = InventoryApp(root)
    
    # Memulai event loop Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
