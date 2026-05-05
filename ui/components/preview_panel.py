import customtkinter as ctk
from tkinter import ttk

class PreviewPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame para a tabela
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        
        # Estilo para o Treeview (mais moderno)
        style = ttk.Style()
        style.theme_use("default")
        
        # Cores para modo escuro (default)
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b",
                        rowheight=25,
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background="#333333", 
                        foreground="white", 
                        relief="flat",
                        font=ctk.CTkFont(size=12, weight="bold"))
        style.map("Treeview.Heading", background=[('active', '#444444')])
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        self.tree = ttk.Treeview(self.table_frame, show="headings")
        
        # Scrollbars customizadas (CustomTkinter não tem scrollbar nativa para Treeview, usamos a do ttk mas escondida/estilizada)
        self.vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

    def update_preview(self, df):
        # Limpar colunas e dados existentes
        self.tree.delete(*self.tree.get_children())
        
        if df is None or df.empty:
            self.tree["columns"] = ("Aviso",)
            self.tree.heading("Aviso", text="Informação")
            self.tree.insert("", "end", values=("Nenhum dado para exibir no momento.",))
            return
            
        # Configurar novas colunas
        colunas = list(df.columns)
        self.tree["columns"] = colunas
        
        for col in colunas:
            # Tentar estimar largura baseada no nome da coluna
            largura = max(100, len(str(col)) * 10)
            self.tree.heading(col, text=col)
            self.tree.column(col, width=largura, anchor="center")
            
        # Inserir dados
        for _, row in df.iterrows():
            # Converter todos os valores para string para evitar erros no Treeview
            valores = [str(val) if val is not None else "" for val in row]
            self.tree.insert("", "end", values=valores)
            
    def set_appearance_mode(self, mode):
        # Opcional: Ajustar cores do Treeview dinamicamente se o tema mudar
        style = ttk.Style()
        if mode.lower() == "light":
            style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
            style.configure("Treeview.Heading", background="#eeeeee", foreground="black")
        else:
            style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
            style.configure("Treeview.Heading", background="#333333", foreground="white")
