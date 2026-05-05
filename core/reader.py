import pandas as pd
import os

class ExcelReader:
    def __init__(self, file_path, sep=','):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()
        self.sep = sep
        
    def get_sheets(self):
        if self.extension in ['.xlsx', '.xlsm', '.xls']:
            try:
                xl = pd.ExcelFile(self.file_path)
                return xl.sheet_names
            except Exception as e:
                print(f"Erro ao ler abas: {e}")
                return []
        elif self.extension == '.ods':
            try:
                # ODS requires odfpy
                xl = pd.ExcelFile(self.file_path, engine='odf')
                return xl.sheet_names
            except Exception as e:
                print(f"Erro ao ler abas ODS: {e}")
                return []
        elif self.extension == '.csv':
            return ["CSV File"]
        return []

    def get_preview(self, sheet_name=None, nrows=10, sep=None):
        try:
            if self.extension == '.csv':
                if sep:
                    return pd.read_csv(self.file_path, nrows=nrows, sep=sep)
                # Try common separators
                for sep in [',', ';', '\t']:
                    try:
                        df = pd.read_csv(self.file_path, nrows=nrows, sep=sep)
                        if len(df.columns) > 1:
                            return df
                    except:
                        continue
                return pd.read_csv(self.file_path, nrows=nrows)
            elif self.extension == '.ods':
                return pd.read_excel(self.file_path, sheet_name=sheet_name, nrows=nrows, engine='odf')
            else:
                return pd.read_excel(self.file_path, sheet_name=sheet_name, nrows=nrows)
        except Exception as e:
            print(f"Erro no preview: {e}")
            return None

    def get_total_rows(self, sheet_name=None):
        try:
            if self.extension == '.csv':
                # Efficient row count for CSV
                count = 0
                with open(self.file_path, 'rb') as f:
                    for line in f:
                        count += 1
                return count - 1 # exclude header
            elif self.extension in ['.xlsx', '.xlsm', '.xls', '.ods']:
                # For Excel, we might need to load the whole sheet or use a more efficient way
                # pandas doesn't have a direct "count rows" without reading
                # But for preview/info we can do a quick load of just one column
                df = pd.read_excel(self.file_path, sheet_name=sheet_name, usecols=[0])
                return len(df)
        except Exception as e:
            print(f"Erro ao contar linhas: {e}")
            return 0
        return 0
