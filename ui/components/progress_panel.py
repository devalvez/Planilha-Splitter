"""
Passo 4 do Wizard: Progresso e Detalhes.
"""
import customtkinter as ctk
import time
from utils.helpers import format_size

class ProgressPanel(ctk.CTkFrame):
    def __init__(self, master, on_start, on_pause, on_cancel, on_open_folder, on_back, on_reset, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_start = on_start
        self.on_pause = on_pause
        self.on_cancel = on_cancel
        self.on_open_folder = on_open_folder
        self.on_back = on_back
        self.on_reset = on_reset
        
        self._construir_interface()

    def _construir_interface(self):
        # 1. Topo: Barra de Progresso em Destaque
        self.top_frame = ctk.CTkFrame(self, fg_color="#1c222d", corner_radius=15, border_width=1, border_color="#3b8ed0")
        self.top_frame.pack(fill="x", padx=40, pady=(20, 10))

        self.lbl_status = ctk.CTkLabel(self.top_frame, text="Aguardando início...", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_status.pack(pady=(20, 10))

        self.progress_bar = ctk.CTkProgressBar(self.top_frame, width=800, height=15, progress_color="#3b8ed0")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, padx=40)

        self.lbl_percent = ctk.CTkLabel(self.top_frame, text="0%", font=ctk.CTkFont(size=12))
        self.lbl_percent.pack(pady=(0, 20))

        # 2. Meio: Quadro de Detalhes e Logs
        self.details_frame = ctk.CTkFrame(self, fg_color="#14181f", corner_radius=15, border_width=1, border_color="#222831")
        self.details_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Grid interno para detalhes
        self.details_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.stat_files = self._create_stat(self.details_frame, "Arquivos Criados", "0", 0)
        self.stat_time = self._create_stat(self.details_frame, "Tempo Decorrido", "00:00", 1)
        self.stat_size = self._create_stat(self.details_frame, "Tamanho Total", "0 KB", 2)

        # Log de Atividades
        self.txt_log = ctk.CTkTextbox(self.details_frame, fg_color="#0b0e14", font=ctk.CTkFont(family="Consolas", size=11))
        self.txt_log.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        self.details_frame.grid_rowconfigure(1, weight=1)

        # 3. Rodapé: Controles
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=40, pady=20)

        self.btn_pause = ctk.CTkButton(self.controls_frame, text="⏸  Pausar", command=self.on_pause, fg_color="gray30", text_color="#ffffff", state="disabled")
        self.btn_pause.pack(side="left", padx=5)

        self.btn_cancel = ctk.CTkButton(self.controls_frame, text="🛑  Cancelar", command=self.on_cancel, fg_color="#922b21", text_color="#ffffff", state="disabled")
        self.btn_cancel.pack(side="left", padx=5)

        self.btn_open = ctk.CTkButton(self.controls_frame, text="📂  Abrir Pasta", command=self.on_open_folder, fg_color="#3b8ed0", text_color="#ffffff", state="disabled")
        self.btn_open.pack(side="right", padx=5)

        self.btn_reset = ctk.CTkButton(self.controls_frame, text="🔄  Splitar Outro Arquivo", command=self.on_reset, fg_color="#1a7a3c", text_color="#ffffff")
        self.btn_reset.pack_forget() # Esconder inicialmente
        
        self.btn_back = ctk.CTkButton(self.controls_frame, text="⬅  Voltar", command=self.on_back, fg_color="transparent", border_width=1)
        self.btn_back.pack(side="right", padx=5)

    def _create_stat(self, parent, label, value, col):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, pady=20)
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11), text_color="gray").pack()
        val_lbl = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=16, weight="bold"))
        val_lbl.pack()
        return val_lbl

    def add_log(self, msg):
        self.txt_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.txt_log.see("end")

    def update_progress(self, val, current, total):
        self.progress_bar.set(val / 100)
        self.lbl_percent.configure(text=f"{int(val)}% ({current}/{total})")
        if val > 0: self.lbl_status.configure(text="Processando...")

    def set_running(self, running):
        state = "normal" if running else "disabled"
        self.btn_pause.configure(state=state)
        self.btn_cancel.configure(state=state)
        self.btn_back.configure(state="disabled" if running else "normal")
        if running: self.lbl_status.configure(text="Iniciando motores...")

    def update_pause_btn(self, is_paused):
        self.btn_pause.configure(text="▶  Retomar" if is_paused else "⏸  Pausar")
        self.lbl_status.configure(text="Pausado" if is_paused else "Processando...")

    def exibir_resumo(self, arquivos, tempo, tamanho):
        self.lbl_status.configure(text="✨ Concluído com Sucesso!")
        self.stat_files.configure(text=str(arquivos))
        self.stat_time.configure(text=f"{tempo:.1f}s")
        self.stat_size.configure(text=format_size(tamanho))
        self.btn_open.configure(state="normal")
        self.btn_back.configure(state="normal")
        self.btn_reset.pack(side="right", padx=5) # Mostrar botão de reset

    def limpar(self):
        self.txt_log.delete("1.0", "end")
        self.progress_bar.set(0)
        self.lbl_percent.configure(text="0%")
        self.stat_files.configure(text="0")
        self.stat_time.configure(text="00:00")
        self.stat_size.configure(text="0 KB")
        self.btn_open.configure(state="disabled")
        self.btn_reset.pack_forget() # Esconder ao limpar
