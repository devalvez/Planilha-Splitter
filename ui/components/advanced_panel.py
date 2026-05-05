import customtkinter as ctk

class AdvancedPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="⚙️ Opções Avançadas", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Filtering Section
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_filter = ctk.CTkLabel(self.filter_frame, text="Limpeza de Dados", font=ctk.CTkFont(weight="bold"))
        self.lbl_filter.pack(padx=10, pady=5, anchor="w")
        
        self.check_dupes = ctk.CTkCheckBox(self.filter_frame, text="Remover linhas duplicadas")
        self.check_dupes.pack(padx=10, pady=5, anchor="w")
        
        self.check_empty = ctk.CTkCheckBox(self.filter_frame, text="Remover linhas em branco")
        self.check_empty.pack(padx=10, pady=5, anchor="w")
        
        # Column Selection
        self.col_frame = ctk.CTkFrame(self)
        self.col_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_cols = ctk.CTkLabel(self.col_frame, text="Seleção de Colunas", font=ctk.CTkFont(weight="bold"))
        self.lbl_cols.pack(padx=10, pady=5, anchor="w")
        
        self.cols_scroll = ctk.CTkScrollableFrame(self.col_frame, height=150)
        self.cols_scroll.pack(padx=10, pady=5, fill="both", expand=True)
        self.col_checkboxes = {}

        # Performance Section
        self.perf_frame = ctk.CTkFrame(self)
        self.perf_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_perf = ctk.CTkLabel(self.perf_frame, text="Performance e Memória", font=ctk.CTkFont(weight="bold"))
        self.lbl_perf.pack(padx=10, pady=5, anchor="w")
        
        self.ram_label = ctk.CTkLabel(self.perf_frame, text="Limite de RAM estimado (MB): 1024")
        self.ram_label.pack(padx=10, pady=0, anchor="w")
        
        self.ram_slider = ctk.CTkSlider(self.perf_frame, from_=256, to=8192, command=self.update_ram_label)
        self.ram_slider.set(1024)
        self.ram_slider.pack(padx=10, pady=10, fill="x")
        
        self.check_parallel = ctk.CTkCheckBox(self.perf_frame, text="Processamento em paralelo (Beta)")
        self.check_parallel.pack(padx=10, pady=5, anchor="w")

    def update_ram_label(self, val):
        self.ram_label.configure(text=f"Limite de RAM estimado (MB): {int(val)}")

    def set_columns(self, columns):
        # Clear existing
        for cb in self.col_checkboxes.values():
            cb.destroy()
        self.col_checkboxes = {}
        
        for col in columns:
            cb = ctk.CTkCheckBox(self.cols_scroll, text=col)
            cb.select()
            cb.pack(padx=5, pady=2, anchor="w")
            self.col_checkboxes[col] = cb

    def get_advanced_params(self):
        selected_cols = [col for col, cb in self.col_checkboxes.items() if cb.get()]
        return {
            "remove_duplicates": self.check_dupes.get(),
            "remove_empty_rows": self.check_empty.get(),
            "selected_columns": selected_cols,
            "ram_limit": int(self.ram_slider.get()),
            "parallel": self.check_parallel.get()
        }
