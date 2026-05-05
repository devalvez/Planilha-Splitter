"""
Passo 2 do Wizard: Configurações de Split e Limpeza de Dados.
"""
import customtkinter as ctk

class SplitPanel(ctk.CTkFrame):
    def __init__(self, master, on_next, on_back, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_next = on_next
        self.on_back = on_back
        self.columns = []
        self.col_checkboxes = {}

        self._construir_interface()

    def _construir_interface(self):
        ctk.CTkLabel(
            self, 
            text="Configurações de Divisão", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 20))

        # Layout Principal: Esquerda (Regras) e Direita (Colunas/Limpeza)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=40)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # --- COLUNA ESQUERDA: Regras de Split ---
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="#1c222d", corner_radius=15, border_width=1, border_color="#3b8ed0")
        self.left_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        ctk.CTkLabel(self.left_frame, text="Regras de Divisão", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3b8ed0").pack(pady=15)

        ctk.CTkLabel(self.left_frame, text="Método:").pack(pady=(10, 0))
        self.mode_var = ctk.StringVar(value="Linhas por arquivo")
        self.combo_mode = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Linhas por arquivo", "Número total de arquivos", "Por coluna específica", "Intervalos manuais", "Tamanho máximo (MB)"],
            variable=self.mode_var,
            command=self._on_mode_change,
            width=220
        )
        self.combo_mode.pack(pady=10)

        self.lbl_value = ctk.CTkLabel(self.left_frame, text="Quantidade de linhas:")
        self.lbl_value.pack()
        self.entry_value = ctk.CTkEntry(self.left_frame, width=220, placeholder_text="Ex: 1000")
        self.entry_value.pack(pady=5)

        # Opções de Limpeza
        ctk.CTkLabel(self.left_frame, text="Limpeza de Dados", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray").pack(pady=(20, 5))
        self.check_smart = ctk.CTkCheckBox(self.left_frame, text="Smart Merge (Auto-mesclar)", border_color="#3b8ed0")
        self.check_smart.pack(pady=5, anchor="w", padx=40)
        
        self.check_dupes = ctk.CTkCheckBox(self.left_frame, text="Remover duplicatas", border_color="#3b8ed0")
        self.check_dupes.pack(pady=5, anchor="w", padx=40)
        
        self.check_empty = ctk.CTkCheckBox(self.left_frame, text="Remover linhas vazias", border_color="#3b8ed0")
        self.check_empty.pack(pady=5, anchor="w", padx=40)

        # --- COLUNA DIREITA: Seleção de Colunas ---
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="#1c222d", corner_radius=15, border_width=1, border_color="#222831")
        self.right_frame.grid(row=0, column=1, padx=10, sticky="nsew")

        ctk.CTkLabel(self.right_frame, text="Seleção de Colunas", font=ctk.CTkFont(size=16, weight="bold"), text_color="gray").pack(pady=15)
        
        self.cols_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent", height=250)
        self.cols_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_no_cols = ctk.CTkLabel(self.cols_scroll, text="Aguardando arquivo...", text_color="gray50")
        self.lbl_no_cols.pack(pady=50)

        # Botões de Navegação
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(side="bottom", fill="x", pady=(20, 10), padx=40)

        ctk.CTkButton(self.nav_frame, text="⬅  Voltar", fg_color="gray30", text_color="#ffffff", command=self.on_back, width=150, height=40).pack(side="left")
        ctk.CTkButton(self.nav_frame, text="Próximo Passo  ➔", fg_color="#3b8ed0", text_color="#ffffff", command=self.on_next, width=150, height=40).pack(side="right")

    def _on_mode_change(self, mode):
        labels = {
            "Linhas por arquivo": "Quantidade de linhas:",
            "Número total de arquivos": "Número de arquivos:",
            "Por coluna específica": "Selecione a coluna:",
            "Intervalos manuais": "Ex: 1-10, 11-50, 51-fim",
            "Tamanho máximo (MB)": "Tamanho em MB:"
        }
        self.lbl_value.configure(text=labels.get(mode, "Valor:"))
        
    def set_columns(self, cols):
        self.columns = cols
        self.lbl_no_cols.pack_forget()
        
        # Limpar checkboxes antigos
        for cb in self.col_checkboxes.values():
            cb.destroy()
        self.col_checkboxes = {}
        
        for col in cols:
            cb = ctk.CTkCheckBox(self.cols_scroll, text=col, border_color="#3b8ed0")
            cb.select()
            cb.pack(pady=2, anchor="w", padx=10)
            self.col_checkboxes[col] = cb

    def get_params(self):
        mode_map = {
            "Linhas por arquivo": "rows",
            "Número total de arquivos": "files",
            "Por coluna específica": "column",
            "Intervalos manuais": "manual",
            "Tamanho máximo (MB)": "size"
        }
        mode = mode_map[self.mode_var.get()]
        val = self.entry_value.get()
        
        # Colunas selecionadas
        selected_cols = [col for col, cb in self.col_checkboxes.items() if cb.get()]
        
        params = {
            "mode": mode,
            "smart_format": self.check_smart.get(),
            "remove_duplicates": self.check_dupes.get(),
            "remove_empty_rows": self.check_empty.get(),
            "selected_columns": selected_cols
        }
        
        if mode == "rows": params["rows_per_file"] = int(val) if val.isdigit() else 1000
        elif mode == "files": params["num_files"] = int(val) if val.isdigit() else 1
        elif mode == "column": params["split_column"] = val
        elif mode == "manual": params["manual_input"] = val
        elif mode == "size": params["max_size_mb"] = float(val) if val.replace('.','').isdigit() else 1.0
        
        return params
