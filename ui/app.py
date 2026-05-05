"""
Janela principal do Planilha Splitter com Header Global e Wizard.
"""
import os
import queue
import threading
import subprocess
import sys
import traceback

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from .components.file_panel import FilePanel
from .components.split_panel import SplitPanel
from .components.output_panel import OutputPanel
from .components.progress_panel import ProgressPanel
from .components.about_panel import AboutPanel
from core.splitter import DataSplitter
from core.reader import ExcelReader
from utils.validators import validate_split_params

class PlanilhaSplitterApp(ctk.CTk):
    TITULO = "Planilha Splitter v1.0.0"
    GEOMETRIA = "1100x750"
    COR_PRIMARIA = "#3b8ed0"
    COR_FUNDO = "#0b0e14"

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        self.title(self.TITULO)
        self.geometry(self.GEOMETRIA)
        self.minsize(1000, 750)
        self.configure(fg_color=self.COR_FUNDO)
        self._centralizar_janela()

        # Estado
        self.passo_atual = 0
        self.passo_antes_sobre = 0
        self.splitter = None
        self.progress_queue = queue.Queue()
        
        self._arquivo_atual = ""
        self._sheet_atual = ""
        self._colunas_atuais = []

        self._construir_interface()
        self._poll_queue()

    def _construir_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # Stepper
        self.grid_rowconfigure(2, weight=1) # Container Principal (Wizard)
        self.grid_rowconfigure(3, weight=0) # Footer

        # 1. Header Global (Topo)
        self.header_global = ctk.CTkFrame(self, fg_color="#10141b", height=70, corner_radius=0)
        self.header_global.grid(row=0, column=0, sticky="ew")
        self.header_global.grid_columnconfigure(1, weight=1)
        
        # Logo no Header
        try:
            img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png")
            orig_img = Image.open(img_path)
            
            # Cálculo de proporção para o Header
            target_width = 160
            w, h = orig_img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio)
            
            logo_img = ctk.CTkImage(
                light_image=orig_img,
                dark_image=orig_img,
                size=(target_width, target_height)
            )
            ctk.CTkLabel(self.header_global, image=logo_img, text="").grid(row=0, column=0, padx=20, pady=10)
        except:
            ctk.CTkLabel(self.header_global, text="Planilha Splitter", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20)

        # 2. Stepper Area
        self.stepper_area = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.stepper_area.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self._construir_stepper()

        # 3. Container de Conteúdo
        self.container = ctk.CTkFrame(self, fg_color="#14181f", corner_radius=15, border_width=1, border_color="#222831")
        self.container.grid(row=2, column=0, sticky="nsew", padx=30, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Painéis
        self.painel_arquivo = FilePanel(self.container, on_file_selected=self._ao_selecionar_arquivo, on_next=self.proximo_passo)
        self.painel_split = SplitPanel(self.container, on_next=self.proximo_passo, on_back=self.passo_anterior)
        self.painel_destino = OutputPanel(self.container, on_start=self._iniciar_split, on_back=self.passo_anterior)
        self.painel_progresso = ProgressPanel(
            self.container, on_start=self._iniciar_split, on_pause=self._pausar_split,
            on_cancel=self._cancelar_split, on_open_folder=self._abrir_pasta_saida, 
            on_back=self.passo_anterior, on_reset=self._reset_wizard
        )
        self.painel_sobre = AboutPanel(self.container, on_back=self._voltar_do_sobre)

        self._paineis_wizard = [self.painel_arquivo, self.painel_split, self.painel_destino, self.painel_progresso]

        # 4. Rodapé
        self.footer = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.footer.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 10))
        ctk.CTkLabel(self.footer, text="Planilha Splitter v1.0.0 Stable", font=ctk.CTkFont(size=11), text_color="gray").pack(side="left")
        ctk.CTkButton(self.footer, text="Sobre o Projeto", font=ctk.CTkFont(size=11, underline=True), 
                     fg_color="transparent", hover=False, text_color=self.COR_PRIMARIA, 
                     command=self._exibir_sobre).pack(side="right")

        self._atualizar_wizard()

    def _construir_stepper(self):
        self.stepper_frame = ctk.CTkFrame(self.stepper_area, fg_color="transparent")
        self.stepper_frame.pack(expand=True)
        self.step_indicators, self.step_labels = [], []
        steps = ["Seleção", "Configuração", "Destino", "Progresso"]
        for i, step in enumerate(steps):
            container = ctk.CTkFrame(self.stepper_frame, fg_color="transparent")
            container.grid(row=0, column=i*2, padx=15)
            ind = ctk.CTkLabel(container, text=str(i + 1), width=30, height=30, corner_radius=15, 
                               fg_color="gray30", text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            ind.pack()
            self.step_indicators.append(ind)
            lbl = ctk.CTkLabel(container, text=step, font=ctk.CTkFont(size=11), text_color="gray")
            lbl.pack(pady=(5, 0))
            self.step_labels.append(lbl)
            if i < len(steps) - 1:
                ctk.CTkFrame(self.stepper_frame, width=40, height=2, fg_color="gray20").grid(row=0, column=i*2+1, pady=(0, 20))

    def _atualizar_wizard(self):
        for i, painel in enumerate(self._paineis_wizard):
            if i == self.passo_atual: painel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            else: painel.grid_forget()
        self.painel_sobre.grid_forget()
        for i, (ind, lbl) in enumerate(zip(self.step_indicators, self.step_labels)):
            if i == self.passo_atual:
                ind.configure(fg_color=self.COR_PRIMARIA)
                lbl.configure(text_color="white", font=ctk.CTkFont(size=11, weight="bold"))
            elif i < self.passo_atual:
                ind.configure(fg_color="#1a7a3c")
                lbl.configure(text_color="#1a7a3c")
            else:
                ind.configure(fg_color="gray30")
                lbl.configure(text_color="gray")

    def proximo_passo(self):
        if self.passo_atual < len(self._paineis_wizard) - 1:
            self.passo_atual += 1
            self._atualizar_wizard()

    def passo_anterior(self):
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self._atualizar_wizard()

    def _reset_wizard(self):
        """Reinicia o wizard para o primeiro passo."""
        self.passo_atual = 0
        self._atualizar_wizard()

    def _exibir_sobre(self):
        self.passo_antes_sobre = self.passo_atual
        for p in self._paineis_wizard: p.grid_forget()
        self.painel_sobre.grid(row=0, column=0, sticky="nsew")

    def _voltar_do_sobre(self):
        self.passo_atual = self.passo_antes_sobre
        self._atualizar_wizard()

    def _ao_selecionar_arquivo(self, caminho: str, sheet: str):
        self._arquivo_atual, self._sheet_atual = caminho, sheet
        reader = ExcelReader(caminho)
        df_preview = reader.get_preview(sheet, nrows=10)
        if df_preview is not None:
            self._colunas_atuais = list(df_preview.columns)
            self.painel_split.set_columns(self._colunas_atuais)
        else: self._colunas_atuais = []

    def _coletar_params(self) -> dict:
        params = {}
        params.update(self.painel_split.get_params())
        params.update(self.painel_destino.get_params())
        params["input_file"], params["sheet_name"] = self.painel_arquivo.file_path_var.get(), self.painel_arquivo.sheet_var.get()
        return params

    def _iniciar_split(self):
        params = self._coletar_params()
        erros = validate_split_params(params)
        if erros:
            messagebox.showerror("Parâmetros Inválidos", "\n".join(f"• {e}" for e in erros))
            return
        self.passo_atual = 3
        self._atualizar_wizard()
        self.painel_progresso.limpar()
        self.painel_progresso.set_running(True)
        self.splitter = DataSplitter(params, self.progress_queue)
        threading.Thread(target=self.splitter.run, daemon=True).start()

    def _pausar_split(self):
        if self.splitter:
            self.splitter.toggle_pause()
            self.painel_progresso.update_pause_btn(self.splitter.is_paused)

    def _cancelar_split(self):
        if self.splitter:
            self.splitter.stop()
            self.painel_progresso.set_running(False)

    def _poll_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()
                tipo = msg.get("type")
                if tipo == "log": self.painel_progresso.add_log(msg["message"])
                elif tipo == "progress": self.painel_progresso.update_progress(msg["value"], msg.get("current", 0), msg.get("total", 0))
                elif tipo == "done":
                    self.painel_progresso.set_running(False)
                    self.painel_progresso.exibir_resumo(msg.get("files", 0), msg.get("time", 0), msg.get("size", 0))
                elif tipo == "error":
                    self.painel_progresso.set_running(False)
                    messagebox.showerror("Erro", msg.get("message", "Erro desconhecido."))
        except queue.Empty: pass
        finally: self.after(100, self._poll_queue)

    def _abrir_pasta_saida(self):
        pasta = self.painel_destino.out_path_var.get()
        if os.path.isdir(pasta):
            if sys.platform == "win32": os.startfile(pasta)
            else: subprocess.Popen(["xdg-open" if sys.platform == "linux" else "open", pasta])

    def _centralizar_janela(self):
        self.update_idletasks()
        w, h = 1100, 750
        x, y = (self.winfo_screenwidth() - w) // 2, (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

if __name__ == "__main__":
    app = PlanilhaSplitterApp()
    app.mainloop()
