"""
Passo 3 do Wizard: Local de Saída e Início.
"""
import customtkinter as ctk
from tkinter import filedialog
import os

class OutputPanel(ctk.CTkFrame):
    def __init__(self, master, on_start, on_back, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_start = on_start
        self.on_back = on_back
        
        self.out_path_var = ctk.StringVar()
        self.base_name_var = ctk.StringVar(value="split_resultado")
        self.format_var = ctk.StringVar(value=".xlsx")

        self._construir_interface()

    def _construir_interface(self):
        ctk.CTkLabel(
            self, 
            text="Onde deseja salvar os resultados?", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 30))

        self.box = ctk.CTkFrame(self, fg_color="#1c222d", corner_radius=15, border_width=1, border_color="#3b8ed0")
        self.box.pack(fill="both", expand=True, padx=20, pady=10)

        # Pasta de Saída
        ctk.CTkLabel(self.box, text="Pasta de Destino:", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        
        row_path = ctk.CTkFrame(self.box, fg_color="transparent")
        row_path.pack(pady=10, fill="x", padx=40)
        
        self.entry_path = ctk.CTkEntry(row_path, textvariable=self.out_path_var, placeholder_text="Selecione a pasta...")
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(row_path, text="Selecionar", width=100, command=self._selecionar_pasta).pack(side="right")

        # Nome Base e Formato
        ctk.CTkLabel(self.box, text="Nome base dos arquivos:", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        ctk.CTkEntry(self.box, textvariable=self.base_name_var, width=300).pack(pady=5)

        ctk.CTkLabel(self.box, text="Formato de saída:", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        ctk.CTkOptionMenu(self.box, values=[".xlsx", ".csv", ".ods"], variable=self.format_var).pack(pady=(5, 30))

        # Botões de Navegação
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(side="bottom", fill="x", pady=20, padx=20)

        ctk.CTkButton(self.nav_frame, text="⬅  Voltar", fg_color="gray30", command=self.on_back, width=150, height=45, text_color="#ffffff").pack(side="left")
        
        self.btn_start = ctk.CTkButton(
            self.nav_frame, 
            text="🚀  INICIAR SPLIT", 
            fg_color="#1a7a3c", 
            hover_color="#155e2f",
            text_color="#ffffff",
            font=ctk.CTkFont(weight="bold"),
            command=self.on_start, 
            width=200, 
            height=45
        )
        self.btn_start.pack(side="right")

    def _selecionar_pasta(self):
        folder = filedialog.askdirectory()
        if folder:
            self.out_path_var.set(folder)

    def get_params(self):
        return {
            "output_folder": self.out_path_var.get(),
            "base_name": self.base_name_var.get(),
            "output_format": self.format_var.get()
        }
