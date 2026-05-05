"""
Painel "Sobre" com informações do desenvolvedor e botão de retorno.
"""
import customtkinter as ctk
import webbrowser
import os
from PIL import Image

class AboutPanel(ctk.CTkFrame):
    """Painel que exibe informações sobre o projeto e o desenvolvedor."""
    
    def __init__(self, master, on_back, **kwargs):
        # Transparente e sem bordas para evitar linhas fantasmas
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self.on_back = on_back
        
        self.grid_columnconfigure(0, weight=1)
        self._construir_interface()

    def _construir_interface(self):
        # Botão Voltar (Topo Esquerda)
        btn_back = ctk.CTkButton(
            self,
            text="⬅  Voltar ao Wizard",
            width=150,
            height=32,
            fg_color="transparent",
            border_width=1,
            text_color="gray70",
            command=self.on_back
        )
        btn_back.pack(anchor="nw", padx=20, pady=10)

        # Logo Image
        try:
            img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logo.png")
            orig_img = Image.open(img_path)
            
            # Cálculo de proporção para um destaque elegante (200px)
            target_width = 200
            w, h = orig_img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio)
            
            logo_img = ctk.CTkImage(
                light_image=orig_img,
                dark_image=orig_img,
                size=(target_width, target_height)
            )
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(20, 0))
        except Exception:
            pass

        # Título da Aplicação
        ctk.CTkLabel(
            self,
            text="Planilha Splitter",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            self,
            text="v1.0.0 Stable",
            text_color="#3b8ed0",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 40))
        
        # Card do Desenvolvedor (Design Minimalista)
        self.dev_card = ctk.CTkFrame(self, fg_color=("#e5e7eb", "#1c222d"), corner_radius=20, width=500)
        self.dev_card.pack(padx=100, pady=10, fill="x")
        
        # Nome e Bio
        ctk.CTkLabel(
            self.dev_card,
            text="Wesley A. Alves",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(30, 5))
        
        ctk.CTkLabel(
            self.dev_card,
            text="Web Dev FullStack | Open Source Contributor",
            text_color="gray",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            self.dev_card,
            text="📧 contato@wesleyalvesdev.com",
            text_color="#3b8ed0",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            self.dev_card,
            text="🌐 www.wesleyalvesdev.com",
            text_color="#3b8ed0",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(0, 25))
        
        # Botões de Link
        links_frame = ctk.CTkFrame(self.dev_card, fg_color="transparent")
        links_frame.pack(pady=(0, 35))
        
        btn_github = ctk.CTkButton(
            links_frame,
            text="GitHub Profile",
            width=140,
            height=35,
            fg_color="#3b8ed0",
            hover_color="#2d6ea3",
            command=lambda: webbrowser.open("https://github.com/devalvez")
        )
        btn_github.pack(side="left", padx=10)
        
        btn_site = ctk.CTkButton(
            links_frame,
            text="Website",
            width=140,
            height=35,
            fg_color="transparent",
            border_width=1,
            command=lambda: webbrowser.open("http://wesleyalvesdev.com")
        )
        btn_site.pack(side="left", padx=10)

        # Rodapé
        ctk.CTkLabel(
            self,
            text="Desenvolvido com foco em performance e usabilidade.\n© 2026 Planilha Splitter Project.",
            font=ctk.CTkFont(size=11),
            text_color="gray50"
        ).pack(side="bottom", pady=40)
