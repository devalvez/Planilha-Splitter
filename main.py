import os
import sys
import subprocess
import shutil

def is_venv():
    """Verifica se o script está rodando dentro de um ambiente virtual."""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def setup_environment():
    """Cria o venv e instala as dependências se necessário."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(root_dir, "..", "venv")
    requirements = os.path.join(root_dir, "requirements.txt")

    if not is_venv():
        print("🔧 Ambiente virtual não detectado. Preparando ambiente...")
        
        # Se o venv não existe, cria
        if not os.path.exists(venv_dir):
            print("📁 Criando ambiente virtual (venv)...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        
        # Define o caminho do python do venv
        if sys.platform == "win32":
            python_venv = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            python_venv = os.path.join(venv_dir, "bin", "python")

        print("🚀 Reiniciando aplicação dentro do ambiente virtual...")
        subprocess.check_call([python_venv, __file__])
        sys.exit()

    # Se já estamos no venv, garantimos as dependências
    print("📦 Verificando dependências do Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements])
    except Exception as e:
        print(f"⚠️ Erro ao instalar dependências: {e}")

if __name__ == "__main__":
    # Tenta importar o Tkinter primeiro (dependência do SISTEMA)
    try:
        import tkinter
    except ImportError:
        print("\n❌ ERRO CRÍTICO: Tkinter não encontrado no sistema.")
        print("O Tkinter é uma dependência do sistema operacional e não pode ser instalado via pip.")
        print("\nPor favor, execute o comando abaixo no seu terminal para corrigir:")
        if sys.platform.startswith("linux"):
            print("👉 sudo pacman -S tk  (Para Arch Linux)")
            print("👉 sudo apt-get install python3-tk  (Para Ubuntu/Debian)")
        sys.exit(1)

    # Tenta importar a aplicação. Se falhar, roda o setup.
    try:
        from ui.app import PlanilhaSplitterApp
    except ImportError:
        setup_environment()
        # Após o setup, tenta importar novamente
        from ui.app import PlanilhaSplitterApp

    # Inicia a aplicação
    print("✨ Iniciando Planilha Splitter...")
    app = PlanilhaSplitterApp()
    app.mainloop()
