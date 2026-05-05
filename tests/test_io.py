import os
import pandas as pd
import pytest
from core.reader import ExcelReader
from core.writer import ExcelWriter

def test_reader_load_xlsx(sample_excel):
    reader = ExcelReader(sample_excel)
    df = reader.get_preview("Sheet1")
    assert df is not None
    assert "ID" in df.columns

def test_reader_load_csv(sample_csv):
    reader = ExcelReader(sample_csv)
    df = reader.get_preview()
    assert df is not None
    assert "Nome" in df.columns

def test_writer_save_standard(sample_df, temp_dir):
    path = os.path.join(temp_dir, "output.xlsx")
    success = ExcelWriter.save(sample_df, path)
    assert success is True
    assert os.path.exists(path)

def test_writer_save_smart_format(sample_df, temp_dir):
    path = os.path.join(temp_dir, "smart_output.xlsx")
    success = ExcelWriter.save(sample_df, path, smart_format=True)
    assert success is True
    assert os.path.exists(path)

def test_writer_save_smart_format_with_nan(temp_dir):
    # Testando o fix para o erro de float sem len()
    df = pd.DataFrame({
        "A": ["texto", float('nan'), "longo" * 10],
        "B": [1, 2, 3]
    })
    path = os.path.join(temp_dir, "smart_nan.xlsx")
    success = ExcelWriter.save(df, path, smart_format=True)
    assert success is True
    assert os.path.exists(path)

def test_writer_save_csv(sample_df, temp_dir):
    path = os.path.join(temp_dir, "output.csv")
    success = ExcelWriter.save(sample_df, path, format=".csv", sep=",")
    assert success is True
    assert os.path.exists(path)

def test_reader_error_handling():
    reader = ExcelReader("invalid_file.txt")
    assert reader.get_sheets() == []
    assert reader.get_preview() is None
    assert reader.get_total_rows() == 0

def test_writer_error_handling(sample_df):
    success = ExcelWriter.save(sample_df, "/nonexistent/path/file.xlsx")
    assert success is False

def test_reader_sheets_mocked(mocker):
    mock_xl = mocker.patch("pandas.ExcelFile")
    mock_xl.return_value.sheet_names = ["Sheet1", "Sheet2"]
    reader = ExcelReader("test.xlsx")
    assert reader.get_sheets() == ["Sheet1", "Sheet2"]
    reader_ods = ExcelReader("test.ods")
    assert reader_ods.get_sheets() == ["Sheet1", "Sheet2"]

def test_reader_preview_ods(mocker):
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame({"A": [1]})
    reader = ExcelReader("test.ods")
    df = reader.get_preview()
    assert df is not None
    assert "A" in df.columns

def test_reader_total_rows_excel(mocker):
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame({"A": range(50)})
    reader = ExcelReader("test.xlsx")
    assert reader.get_total_rows() == 50

def test_writer_save_ods(sample_df, temp_dir, mocker):
    mocker.patch("pandas.DataFrame.to_excel")
    path = os.path.join(temp_dir, "output.ods")
    success = ExcelWriter.save(sample_df, path, format=".ods")
    assert success is True
