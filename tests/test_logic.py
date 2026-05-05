import pytest
import os
import queue
import pandas as pd
from core.splitter import DataSplitter
from utils.validators import validate_split_params

def test_splitter_rows_mode(sample_excel, temp_dir):
    q = queue.Queue()
    params = {
        "input_file": sample_excel,
        "output_folder": str(temp_dir),
        "mode": "rows",
        "rows_per_file": 2,
        "base_name": "test_split",
        "output_format": ".xlsx"
    }
    splitter = DataSplitter(params, q)
    splitter.run()
    files = [f for f in os.listdir(temp_dir) if f.startswith("test_split")]
    assert len(files) == 5

def test_splitter_column_mode(sample_df, temp_dir):
    sample_df["Categoria"] = ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"]
    path = os.path.join(temp_dir, "cat_sample.xlsx")
    sample_df.to_excel(path, index=False)
    q = queue.Queue()
    params = {
        "input_file": path,
        "output_folder": str(temp_dir),
        "mode": "column",
        "split_column": "Categoria",
        "base_name": "split_cat",
        "output_format": ".xlsx"
    }
    splitter = DataSplitter(params, q)
    splitter.run()
    files = [f for f in os.listdir(temp_dir) if f.startswith("split_cat")]
    assert len(files) == 5

def test_splitter_preprocessing(sample_excel, temp_dir):
    df = pd.read_excel(sample_excel)
    df_dup = pd.concat([df, df])
    path = os.path.join(temp_dir, "dup_sample.xlsx")
    df_dup.to_excel(path, index=False)
    q = queue.Queue()
    params = {
        "input_file": path,
        "output_folder": str(temp_dir),
        "mode": "rows",
        "rows_per_file": 100,
        "remove_duplicates": True,
        "base_name": "clean_split",
        "output_format": ".xlsx"
    }
    splitter = DataSplitter(params, q)
    splitter.run()
    result_path = os.path.join(temp_dir, "clean_split_001.xlsx")
    assert os.path.exists(result_path)
    df_result = pd.read_excel(result_path)
    assert len(df_result) == 10

def test_splitter_manual_mode(sample_excel, temp_dir):
    q = queue.Queue()
    params = {
        "input_file": sample_excel,
        "output_folder": str(temp_dir),
        "mode": "manual",
        "manual_input": "1-3, 4-7, 8-fim",
        "base_name": "manual_split",
        "output_format": ".xlsx"
    }
    splitter = DataSplitter(params, q)
    splitter.run()
    files = [f for f in os.listdir(temp_dir) if f.startswith("manual_split")]
    assert len(files) == 3

def test_splitter_size_mode(sample_excel, temp_dir):
    q = queue.Queue()
    params = {
        "input_file": sample_excel,
        "output_folder": str(temp_dir),
        "mode": "size",
        "max_size_mb": 0.001,
        "base_name": "size_split",
        "output_format": ".xlsx"
    }
    splitter = DataSplitter(params, q)
    splitter.run()
    files = [f for f in os.listdir(temp_dir) if f.startswith("size_split")]
    assert len(files) >= 1

def test_splitter_cancellation(sample_excel, temp_dir):
    q = queue.Queue()
    params = {"input_file": sample_excel, "output_folder": str(temp_dir), "mode": "rows", "rows_per_file": 1}
    splitter = DataSplitter(params, q)
    splitter.stop()
    splitter.run()
    files = [f for f in os.listdir(temp_dir) if f.startswith("split_resultado")]
    assert len(files) == 0

def test_splitter_error_loading(temp_dir):
    q = queue.Queue()
    params = {"input_file": "nonexistent.xlsx", "output_folder": str(temp_dir), "mode": "rows"}
    splitter = DataSplitter(params, q)
    splitter.run()
    found = False
    while not q.empty():
        msg = q.get()
        if msg["type"] == "error":
            found = True
            break
    assert found

def test_splitter_pause_resume():
    q = queue.Queue()
    splitter = DataSplitter({}, q)
    assert not splitter.is_paused
    splitter.toggle_pause()
    assert splitter.is_paused
    splitter.toggle_pause()
    assert not splitter.is_paused

def test_splitter_output_size_calculation(temp_dir):
    path = os.path.join(temp_dir, "size_test_001.xlsx")
    with open(path, "w") as f: f.write("test")
    q = queue.Queue()
    splitter = DataSplitter({"output_folder": str(temp_dir), "base_name": "size_test"}, q)
    assert splitter._calcular_tamanho_saida() > 0

def test_splitter_column_not_found(sample_excel, temp_dir):
    q = queue.Queue()
    params = {"input_file": sample_excel, "output_folder": str(temp_dir), "mode": "column", "split_column": "MISSING"}
    splitter = DataSplitter(params, q)
    splitter.run()
    found = False
    while not q.empty():
        msg = q.get()
        if msg["type"] == "error": found = True
    assert found
