import subprocess
import sys
import os

def run_tests():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(root_dir, "..", "venv", "bin", "python")
    
    if not os.path.exists(venv_python):
        # Tenta caminho do windows se o linux falhar (para portabilidade)
        venv_python = os.path.join(root_dir, "..", "venv", "Scripts", "python.exe")

    print(f"🧪 Usando ambiente: {venv_python}")
    
    # Instalar dependências necessárias para os testes
    try:
        subprocess.check_call([venv_python, "-m", "pip", "install", "pytest", "pytest-cov", "pytest-mock"])
    except:
        print("⚠️ Falha ao instalar pacotes de teste.")

    print("\n🚀 Executando testes com relatório de cobertura...\n")
    
    cmd = [
        venv_python,
        "-m",
        "pytest",
        "--cov=core",
        "--cov=utils",
        "--cov-report=term-missing",
        "tests/"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Testes concluídos!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Alguns testes falharam (Código {e.returncode})")
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_tests()
