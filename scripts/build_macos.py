import os
import subprocess
import sys
import shutil

def create_macos_app():
    # 1. Configurações
    entry_point = "main.py"
    app_name = "PlanilhaSplitter"
    dist_path = "dist"
    
    print(f"--- Iniciando Processo de Build para MacOS ---")
    
    # 2. Instalar dependências
    print("📦 Instalando dependências de build...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "customtkinter", "pandas", "openpyxl", "odfpy", "Pillow"])
    except Exception as e:
        print(f"⚠️ Erro ao instalar dependências: {e}")

    # 3. Comando PyInstaller para MacOS
    # --onefile: Cria um binário único
    # --windowed: Cria um pacote .app (essencial para MacOS)
    # --argv-emulation: Melhora a compatibilidade de arrastar arquivos para o ícone
    
    print(f"🏗️ Compilando {app_name}.app...")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--argv-emulation",
        "--collect-all", "customtkinter",
        "--name", app_name,
        entry_point
    ]

    # Se você tiver um ícone .icns futuramente:
    # if os.path.exists("assets/icon.icns"):
    #     cmd.extend(["--icon", "assets/icon.icns"])

    try:
        subprocess.check_call(cmd)
        print("\n" + "="*40)
        print(f"✅ APP PARA MACOS GERADO COM SUCESSO!")
        print(f"📍 Localização: {os.path.abspath(os.path.join(dist_path, app_name + '.app'))}")
        print("="*40)
        print("\n💡 DICA: No MacOS, após baixar o app, pode ser necessário clicar com o botão direito")
        print("e selecionar 'Abrir' para contornar o aviso de desenvolvedor não identificado.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a compilação: {e}")

if __name__ == "__main__":
    if sys.platform != "darwin":
        print("⚠️ AVISO: Você não está no MacOS.")
        print("Este script foi projetado para rodar no MacOS para gerar um .app.")
        print("Deseja tentar rodar mesmo assim? (s/n)")
        if input().lower() != 's':
            sys.exit()
            
    create_macos_app()
