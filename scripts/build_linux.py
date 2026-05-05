import os
import subprocess
import sys
import shutil

def create_linux_binary():
    # 1. Configurações
    entry_point = "main.py"
    app_name = "PlanilhaSplitter"
    dist_path = "dist"
    
    print(f"--- Iniciando Processo de Build para Linux ---")
    
    # 2. Instalar dependências
    print("📦 Instalando dependências de build...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "customtkinter", "pandas", "openpyxl", "odfpy", "Pillow"])
    except Exception as e:
        print(f"⚠️ Erro ao instalar dependências: {e}")

    # 3. Comando PyInstaller para Linux
    # --onefile: Único arquivo executável
    # --windowed: Para apps GUI
    
    print(f"🏗️ Compilando binário Linux...")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--collect-all", "customtkinter",
        "--name", app_name,
        entry_point
    ]

    try:
        subprocess.check_call(cmd)
        print("\n" + "="*40)
        print(f"✅ BINÁRIO LINUX GERADO COM SUCESSO!")
        print(f"📍 Localização: {os.path.abspath(os.path.join(dist_path, app_name))}")
        print("="*40)
        print("\n💡 DICA: Lembre-se de dar permissão de execução:")
        print(f"   chmod +x {app_name}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a compilação: {e}")

if __name__ == "__main__":
    if sys.platform != "linux":
        print("⚠️ AVISO: Você não está no Linux.")
        print("Deseja tentar rodar mesmo assim? (s/n)")
        if input().lower() != 's':
            sys.exit()
            
    create_linux_binary()
