import pandas as pd
import os
import sys
import threading
from datetime import datetime
from .writer import ExcelWriter


def _log_timestamp(msg):
    return f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"


class DataSplitter:
    """
    Responsável por executar o split dos dados conforme os parâmetros fornecidos.
    Roda em thread separada e se comunica com a UI via queue.Queue.
    """

    def __init__(self, params, progress_queue):
        self.params = params
        self.queue = progress_queue
        self.stop_event = threading.Event()
        self.is_paused = False
        self.pause_event = threading.Event()
        self.pause_event.set()  # inicia desbloqueado

    # ──────────────────────────────────────────────
    # Comunicação com a UI
    # ──────────────────────────────────────────────
    def _log(self, mensagem: str):
        self.queue.put({"type": "log", "message": _log_timestamp(mensagem)})

    def _progresso(self, atual: int, total: int):
        percentual = (atual / total * 100) if total > 0 else 0
        self.queue.put({
            "type": "progress",
            "value": percentual,
            "current": atual,
            "total": total,
        })

    def _erro(self, mensagem: str):
        self.queue.put({"type": "error", "message": mensagem})

    def _finalizado(self, arquivos: int, tempo: float, tamanho_total: int):
        self.queue.put({
            "type": "done",
            "files": arquivos,
            "time": tempo,
            "size": tamanho_total,
        })

    # ──────────────────────────────────────────────
    # Ponto de entrada principal (roda em thread)
    # ──────────────────────────────────────────────
    def run(self):
        import time
        inicio = time.time()

        try:
            self._log("Iniciando processo de split…")
            df = self._carregar_dados()

            if df is None:
                return

            # Pré-processamento
            df = self._pre_processar(df)

            # Selecionar colunas específicas (se configurado)
            colunas_selecionadas = self.params.get("selected_columns")
            if colunas_selecionadas:
                colunas_validas = [c for c in colunas_selecionadas if c in df.columns]
                if colunas_validas:
                    df = df[colunas_validas]
                    self._log(f"Colunas selecionadas: {', '.join(colunas_validas)}")

            # Dispatcher de modo
            modo = self.params.get("mode", "rows")
            arquivos_gerados = 0

            if modo == "rows":
                arquivos_gerados = self._split_por_linhas(df)
            elif modo == "files":
                arquivos_gerados = self._split_por_quantidade(df)
            elif modo == "column":
                arquivos_gerados = self._split_por_coluna(df)
            elif modo == "manual":
                arquivos_gerados = self._split_manual(df)
            elif modo == "size":
                arquivos_gerados = self._split_por_tamanho(df)
            else:
                self._erro(f"Modo de split desconhecido: '{modo}'")
                return

            if not self.stop_event.is_set():
                duracao = round(time.time() - inicio, 2)
                tamanho = self._calcular_tamanho_saida()
                self._log(f"✅ Concluído! {arquivos_gerados} arquivo(s) gerado(s) em {duracao}s.")
                self._finalizado(arquivos_gerados, duracao, tamanho)

        except Exception as e:
            import traceback
            self._log(f"❌ ERRO CRÍTICO: {e}")
            self._log(traceback.format_exc())
            self._erro(str(e))

    # ──────────────────────────────────────────────
    # Carregamento de dados
    # ──────────────────────────────────────────────
    def _carregar_dados(self) -> pd.DataFrame | None:
        arquivo = self.params["input_file"]
        ext = os.path.splitext(arquivo)[1].lower()
        sheet = self.params.get("sheet_name")
        encoding = self.params.get("encoding", "utf-8")

        self._log(f"Lendo arquivo: {os.path.basename(arquivo)}")

        try:
            if ext == ".csv":
                sep = self.params.get("sep", ",")
                df = pd.read_csv(arquivo, sep=sep, encoding=encoding)
            elif ext == ".ods":
                df = pd.read_excel(arquivo, sheet_name=sheet, engine="odf")
            else:  # .xlsx / .xls / .xlsm
                df = pd.read_excel(arquivo, sheet_name=sheet)

            # Se retornar um dicionário (múltiplas abas), pega a primeira ou a selecionada
            if isinstance(df, dict):
                if sheet and sheet in df:
                    df = df[sheet]
                else:
                    # Pega a primeira aba disponível
                    primeira_aba = list(df.keys())[0]
                    df = df[primeira_aba]

            self._log(f"Arquivo carregado: {len(df):,} linhas × {len(df.columns)} colunas")
            return df

        except Exception as e:
            self._erro(f"Erro ao ler o arquivo: {e}")
            return None

    # ──────────────────────────────────────────────
    # Pré-processamento
    # ──────────────────────────────────────────────
    def _pre_processar(self, df: pd.DataFrame) -> pd.DataFrame:
        original = len(df)

        if self.params.get("remove_empty_rows"):
            df = df.dropna(how="all")
            self._log(f"Linhas em branco removidas: {original - len(df)}")

        if self.params.get("remove_duplicates"):
            antes = len(df)
            df = df.drop_duplicates()
            self._log(f"Duplicatas removidas: {antes - len(df)}")

        return df

    # ──────────────────────────────────────────────
    # Modos de split
    # ──────────────────────────────────────────────
    def _split_por_linhas(self, df: pd.DataFrame) -> int:
        linhas_por_arquivo = int(self.params["rows_per_file"])
        total = len(df)
        num_partes = max(1, (total + linhas_por_arquivo - 1) // linhas_por_arquivo)
        self._log(f"Modo: Por Linhas → {linhas_por_arquivo:,} linhas/arquivo → {num_partes} parte(s)")

        for i in range(num_partes):
            if self.stop_event.is_set():
                self._log("⚠️ Processo cancelado pelo usuário.")
                break
            self._aguardar_pausa()

            inicio = i * linhas_por_arquivo
            fim = min((i + 1) * linhas_por_arquivo, total)
            chunk = df.iloc[inicio:fim]

            nome = self._gerar_nome(i + 1)
            self._salvar_chunk(chunk, nome, i + 1)
            self._progresso(i + 1, num_partes)

        return num_partes

    def _split_por_quantidade(self, df: pd.DataFrame) -> int:
        num_arquivos = int(self.params["num_files"])
        total = len(df)
        linhas_por_arquivo = max(1, (total + num_arquivos - 1) // num_arquivos)
        self._log(f"Modo: Por Quantidade → {num_arquivos} arquivo(s) com ≈{linhas_por_arquivo:,} linhas cada")
        self.params["rows_per_file"] = linhas_por_arquivo
        return self._split_por_linhas(df)

    def _split_por_coluna(self, df: pd.DataFrame) -> int:
        coluna = self.params["split_column"]
        if coluna not in df.columns:
            self._erro(f"Coluna '{coluna}' não encontrada no DataFrame.")
            return 0

        valores = df[coluna].dropna().unique()
        total = len(valores)
        self._log(f"Modo: Por Coluna '{coluna}' → {total} valor(es) único(s)")

        contador = 0
        for i, val in enumerate(valores):
            if self.stop_event.is_set():
                self._log("⚠️ Processo cancelado.")
                break
            self._aguardar_pausa()

            chunk = df[df[coluna] == val].copy()
            # Sanitizar o valor para uso em nome de arquivo
            val_seguro = str(val).replace("/", "_").replace("\\", "_").replace(":", "-")
            nome = f"{self.params.get('prefix', '')}{self.params.get('base_name', 'split')}_{val_seguro}{self.params.get('suffix', '')}"
            self._salvar_chunk(chunk, nome, i + 1)
            self._progresso(i + 1, total)
            contador += 1

        return contador

    def _split_manual(self, df: pd.DataFrame) -> int:
        texto = self.params.get("manual_input", "")
        intervalos = self._parsear_intervalos(texto, len(df))

        if not intervalos:
            self._erro("Nenhum intervalo válido encontrado. Use o formato: 1-5000, 5001-fim")
            return 0

        self._log(f"Modo: Manual → {len(intervalos)} intervalo(s) definido(s)")
        total = len(intervalos)

        for i, (inicio, fim) in enumerate(intervalos):
            if self.stop_event.is_set():
                self._log("⚠️ Processo cancelado.")
                break
            self._aguardar_pausa()

            chunk = df.iloc[inicio:fim]
            nome = self._gerar_nome(i + 1)
            self._log(f"  Intervalo {i+1}: linhas {inicio+1}–{fim}")
            self._salvar_chunk(chunk, nome, i + 1)
            self._progresso(i + 1, total)

        return total

    def _split_por_tamanho(self, df: pd.DataFrame) -> int:
        """
        Estimativa de tamanho baseada na memória do DataFrame.
        Divide em partes respeitando o limite de MB por arquivo.
        """
        max_mb = float(self.params.get("max_size_mb", 10))
        max_bytes = max_mb * 1024 * 1024

        # Estimar bytes por linha
        tamanho_total = df.memory_usage(deep=True).sum()
        total_linhas = len(df)
        bytes_por_linha = tamanho_total / total_linhas if total_linhas > 0 else 1
        linhas_por_arquivo = max(1, int(max_bytes / bytes_por_linha))

        self._log(f"Modo: Por Tamanho → máx {max_mb} MB → ≈{linhas_por_arquivo:,} linhas/arquivo (estimado)")
        self.params["rows_per_file"] = linhas_por_arquivo
        return self._split_por_linhas(df)

    # ──────────────────────────────────────────────
    # Utilitários internos
    # ──────────────────────────────────────────────
    def _parsear_intervalos(self, texto: str, total_linhas: int):
        """
        Parseia string no formato '1-5000, 5001-fim' em lista de tuplas (start_idx, end_idx).
        Os índices são 0-based para uso com iloc.
        """
        intervalos = []
        partes = [p.strip() for p in texto.split(",") if p.strip()]

        for parte in partes:
            if "-" not in parte:
                continue
            # Separa no primeiro hífen, exceto se for sinal negativo
            segmentos = parte.split("-", 1)
            if len(segmentos) != 2:
                continue

            inicio_str, fim_str = segmentos[0].strip(), segmentos[1].strip()

            try:
                inicio = int(inicio_str) - 1  # converter 1-based → 0-based
            except ValueError:
                continue

            if fim_str.lower() in ("fim", "end", "last", ""):
                fim = total_linhas
            else:
                try:
                    fim = int(fim_str)
                except ValueError:
                    continue

            inicio = max(0, inicio)
            fim = min(total_linhas, fim)

            if inicio < fim:
                intervalos.append((inicio, fim))

        return intervalos

    def _gerar_nome(self, indice: int) -> str:
        base = self.params.get("base_name", "split_resultado")
        prefixo = self.params.get("prefix", "")
        sufixo = self.params.get("suffix", "")
        digitos = int(self.params.get("num_digits", 3))
        idx_str = str(indice).zfill(digitos)
        return f"{prefixo}{base}{sufixo}_{idx_str}"

    def _salvar_chunk(self, df: pd.DataFrame, nome_base: str, indice: int):
        pasta = self.params["output_folder"]
        formato = self.params.get("output_format", ".xlsx")
        sep = self.params.get("sep", ",")
        encoding = self.params.get("encoding", "utf-8")
        index = self.params.get("include_index", False)

        caminho = os.path.join(pasta, nome_base)
        self._log(f"  → Salvando parte {indice}: {nome_base}{formato}")

        sucesso = ExcelWriter.save(
            df, caminho,
            format=formato,
            sep=sep,
            encoding=encoding,
            index=index,
            smart_format=self.params.get("smart_format", False)
        )
        if not sucesso:
            self._log(f"  ⚠️  Falha ao salvar: {nome_base}{formato}")

    def _calcular_tamanho_saida(self) -> int:
        """Calcula o tamanho total dos arquivos gerados na pasta de saída."""
        pasta = self.params.get("output_folder", "")
        total = 0
        base = self.params.get("base_name", "split_resultado")
        try:
            for arquivo in os.listdir(pasta):
                if base in arquivo:
                    total += os.path.getsize(os.path.join(pasta, arquivo))
        except Exception:
            pass
        return total

    # ──────────────────────────────────────────────
    # Controle de fluxo
    # ──────────────────────────────────────────────
    def _aguardar_pausa(self):
        """Bloqueia a thread enquanto pausado."""
        self.pause_event.wait()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_event.clear()
            self._log("⏸ Processo pausado.")
        else:
            self.pause_event.set()
            self._log("▶ Processo retomado.")

    def stop(self):
        self.stop_event.set()
        self.pause_event.set()  # desbloqueia se estiver pausado
        self._log("⏹ Sinal de cancelamento enviado.")
