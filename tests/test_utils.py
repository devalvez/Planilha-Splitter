import os
from utils.helpers import format_size, get_file_info
from utils.validators import validate_split_params

def test_format_size():
    assert format_size(0) == "0B"
    assert format_size(1024) == "1.0 KB"
    assert format_size(1024 * 1024) == "1.0 MB"

def test_get_file_info(sample_excel):
    info = get_file_info(sample_excel)
    assert info["name"] == "sample.xlsx"
    assert info["extension"] == ".xlsx"
    assert "size" in info

def test_get_file_info_nonexistent():
    assert get_file_info("nonexistent.file") is None

def test_validate_params_all_modes():
    # Rows
    assert len(validate_split_params({"mode": "rows", "rows_per_file": "abc"})) > 0
    assert len(validate_split_params({"mode": "rows", "rows_per_file": "0"})) > 0
    
    # Files
    assert len(validate_split_params({"mode": "files", "num_files": "0"})) > 0
    
    # Column
    assert len(validate_split_params({"mode": "column", "split_column": ""})) > 0
    
    # Manual
    assert len(validate_split_params({"mode": "manual", "manual_input": ""})) > 0
    assert len(validate_split_params({"mode": "manual", "manual_input": "123"})) > 0
    
    # Size
    assert len(validate_split_params({"mode": "size", "max_size_mb": "0"})) > 0
