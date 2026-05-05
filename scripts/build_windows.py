import os
import subprocess
import sys
import shutil

def create_executable():
    # 1. Configurações
    entry_point = "main.py"
    app_name = "PlanilhaSplitter"
    dist_path = "dist"
    build_path = "build"
    
    print(f"--- Iniciando Processo de Build para Windows ---")
    
    # 2. Instalar dependências necessárias para o build
    print("📦 Instalando dependências de build...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "customtkinter", "pandas", "openpyxl", "odfpy", "Pillow"])
    except Exception as e:
        print(f"⚠️ Erro ao instalar dependências: {e}")

    # 3. Comando PyInstaller
    # --onefile: Único executável
    # --windowed: Sem console
    # --collect-all: Garante que os temas do customtkinter sejam incluídos
    # --clean: Limpa o cache antes do build
    
    print(f"🏗️ Compilando {app_name}...")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--clean",
        "--collect-all", "customtkinter",
        "--name", app_name,
        entry_point
    ]

    # Se você tiver um ícone futuramente, adicione-o aqui:
    # if os.path.exists("assets/icon.ico"):
    #     cmd.extend(["--icon", "assets/icon.ico"])

    try:
        subprocess.check_call(cmd)
        print("\n" + "="*40)
        print(f"✅ EXECUTÁVEL GERADO COM SUCESSO!")
        print(f"📍 Localização: {os.path.abspath(os.path.join(dist_path, app_name + '.exe'))}")
        print("="*40)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a compilação: {e}")
    
    # 4. Limpeza opcional de arquivos temporários
    # shutil.rmtree(build_path, ignore_errors=True)
    # os.remove(f"{app_name}.spec")

if __name__ == "__main__":
    if sys.platform != "win32":
        print("⚠️ AVISO: Você não está no Windows.")
        print("Este script foi projetado para rodar no Windows para gerar um .exe.")
        print("Deseja tentar rodar mesmo assim? (s/n)")
        if input().lower() != 's':
            sys.exit()
            
    create_executable()
