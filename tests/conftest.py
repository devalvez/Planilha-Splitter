import pytest
import pandas as pd
import os
import shutil

@pytest.fixture
def temp_dir(tmp_path):
    """Cria um diretório temporário para os testes."""
    d = tmp_path / "test_data"
    d.mkdir()
    return d

@pytest.fixture
def sample_df():
    """Cria um DataFrame de exemplo para os testes."""
    return pd.DataFrame({
        "ID": range(1, 11),
        "Nome": [f"Usuário {i}" for i in range(1, 11)],
        "Descricao": ["Curta"] * 9 + ["Esta é uma descrição propositalmente muito longa para testar a funcionalidade de mesclagem inteligente de colunas que deve ser limitada a 5 colunas no máximo."]
    })

@pytest.fixture
def sample_excel(temp_dir, sample_df):
    """Cria um arquivo Excel de exemplo."""
    path = os.path.join(temp_dir, "sample.xlsx")
    sample_df.to_excel(path, index=False)
    return path

@pytest.fixture
def sample_csv(temp_dir, sample_df):
    """Cria um arquivo CSV de exemplo."""
    path = os.path.join(temp_dir, "sample.csv")
    sample_df.to_csv(path, index=False, sep=";")
    return path
