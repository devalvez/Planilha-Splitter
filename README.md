# Planilha Splitter 📊

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=ffdd54)
![Design](https://img.shields.io/badge/Design-Premium_Dark-10141b?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

Uma aplicação robusta, moderna e intuitiva desenvolvida em Python para divisão de arquivos Excel (.xlsx, .xls, .xlsm), LibreOffice (.ods) e CSV extremamente extensos.

|              Nova Interface Premium              |              Fluxo Wizard (Passo a Passo)               |
| :----------------------------------------------: | :-----------------------------------------------------: |
| ![Dark Mode](dark_mode_preview.png) | ![Light Mode](light_mode_preview.png) |

## ✨ Recursos Principais

- **Experiência Wizard**: Fluxo guiado em 4 passos (Seleção ➔ Configuração ➔ Destino ➔ Processamento).
- **Design Premium Dark**: Interface moderna inspirada em padrões de alto nível (Insomniac Games Style).
- **Múltiplos Modos de Split**:
  - Por número de linhas.
  - Por quantidade total de arquivos.
  - Por valores únicos em uma coluna específica.
  - Por intervalo manual (ex: 1-5000, 5001-fim).
  - Por tamanho estimado de arquivo (MB).
- **Processamento de Alta Performance**:
  - Execução assíncrona para manter a interface responsiva.
  - Otimizado via Pandas para arquivos com milhões de linhas.
- **Opções Avançadas de Limpeza**:
  - Remoção automática de duplicatas e linhas em branco.
  - Seleção seletiva de colunas para o arquivo de saída.
  - Smart Merge para mesclagem inteligente de cabeçalhos.

## 🚀 Como Instalar

1. Certifique-se de ter o **Python 3.8+** instalado.
2. Clone este repositório ou baixe os arquivos.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute:
   ```bash
   python main.py
   ```

## 🏗️ Estrutura do Projeto

```text
planilha_splitter/
├── main.py                  # Ponto de entrada (Auto-setup venv)
├── ui/                      # Camada de Interface (CustomTkinter)
│   ├── app.py               # Orquestrador do Wizard
│   └── components/          # Painéis modulares (File, Split, Output, Progress)
├── core/                    # Lógica de Negócio (Pandas/Motores)
│   ├── reader.py            # Leitura otimizada
│   ├── writer.py            # Escrita com formatação inteligente
│   └── splitter.py          # Algoritmos de divisão
└── utils/                   # Validadores e Helpers
```

## 👨‍💻 Desenvolvido por

**Wesley A. Alves**  
Web Dev FullStack | Open Source Enthusiast  
📧 [contato@wesleyalvesdev.com](mailto:contato@wesleyalvesdev.com)  
🌐 [www.wesleyalvesdev.com](http://www.wesleyalvesdev.com)

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github&color=3b8ed0)](https://github.com/devalvez)
[![Website](https://img.shields.io/badge/Website-wesleyalvesdev.com-blue?style=flat&color=3b8ed0)](http://wesleyalvesdev.com)
[![Twitter](https://img.shields.io/badge/Twitter-@devalvez-1DA1F2?style=flat&logo=x&color=3b8ed0)](https://x.com/devalvez)

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
