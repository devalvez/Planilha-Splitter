"""
Passo 1 do Wizard: Seleção do arquivo de entrada.
"""
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

class FilePanel(ctk.CTkFrame):
    def __init__(self, master, on_file_selected, on_next, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_file_selected = on_file_selected
        self.on_next = on_next
        
        self.file_path_var = ctk.StringVar()
        self.sheet_var = ctk.StringVar()
        self.out_path_var = ctk.StringVar() # Mantemos aqui para compatibilidade de dados
        self.format_var = ctk.StringVar(value=".xlsx")

        self.grid_columnconfigure(0, weight=1)
        self._construir_interface()

    def _construir_interface(self):
        # Título do Passo
        ctk.CTkLabel(
            self, 
            text="Selecione o arquivo para processar", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            self, 
            text="Suporte para Excel (.xlsx, .xls), CSV e ODS", 
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 40))

        # Drop Zone / Select Area
        self.drop_frame = ctk.CTkFrame(self, fg_color="#1c222d", corner_radius=15, border_width=2, border_color="#3b8ed0")
        self.drop_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(self.drop_frame, text="📂", font=ctk.CTkFont(size=60)).pack(pady=(40, 10))
        
        self.btn_select = ctk.CTkButton(
            self.drop_frame,
            text="Procurar Arquivo",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#3b8ed0",
            hover_color="#2d6ea3",
            text_color="#ffffff",
            width=200,
            height=40,
            command=self._selecionar_arquivo
        )
        self.btn_select.pack(pady=10)

        self.lbl_file = ctk.CTkLabel(
            self.drop_frame, 
            text="Nenhum arquivo selecionado", 
            text_color="gray70",
            font=ctk.CTkFont(size=12)
        )
        self.lbl_file.pack(pady=(10, 40))

        # Seleção de Planilha
        self.sheet_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sheet_frame.pack(pady=20, fill="x", padx=20)
        
        self.lbl_sheet = ctk.CTkLabel(self.sheet_frame, text="Selecione a aba (Sheet):", font=ctk.CTkFont(weight="bold"))
        self.combo_sheets = ctk.CTkOptionMenu(self.sheet_frame, variable=self.sheet_var, values=[], dynamic_resizing=False, width=300)

        # Botão de Navegação
        self.btn_next = ctk.CTkButton(
            self,
            text="Próximo Passo  ➔",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#3b8ed0",
            text_color="#ffffff",
            state="disabled",
            height=45,
            width=200,
            command=self.on_next
        )
        self.btn_next.pack(side="bottom", pady=20)

    def _selecionar_arquivo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Arquivos de Planilha", "*.xlsx *.xls *.csv *.ods")]
        )
        if path:
            self.file_path_var.set(path)
            self.lbl_file.configure(text=os.path.basename(path), text_color="#52b2bf")
            
            # Verificar sheets
            if path.lower().endswith(('.xlsx', '.xls', '.ods')):
                try:
                    import pandas as pd
                    xl = pd.ExcelFile(path)
                    sheets = xl.sheet_names
                    self.combo_sheets.configure(values=sheets)
                    self.sheet_var.set(sheets[0])
                    self.lbl_sheet.pack(side="left", padx=10)
                    self.combo_sheets.pack(side="left")
                except:
                    pass
            else:
                self.lbl_sheet.pack_forget()
                self.combo_sheets.pack_forget()

            self.btn_next.configure(state="normal")
            self.on_file_selected(path, self.sheet_var.get())
