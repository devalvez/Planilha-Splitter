import pytest
from unittest.mock import MagicMock, patch
import customtkinter as ctk
from ui.components.file_panel import FilePanel
from ui.components.split_panel import SplitPanel
from ui.components.output_panel import OutputPanel
from ui.components.progress_panel import ProgressPanel
from ui.app import PlanilhaSplitterApp

@pytest.fixture
def mock_ctk():
    with patch('customtkinter.CTkFrame', MagicMock()), \
         patch('customtkinter.CTkButton', MagicMock()), \
         patch('customtkinter.CTkLabel', MagicMock()), \
         patch('customtkinter.CTkEntry', MagicMock()), \
         patch('customtkinter.CTkOptionMenu', MagicMock()), \
         patch('customtkinter.CTkProgressBar', MagicMock()), \
         patch('customtkinter.CTkTextbox', MagicMock()), \
         patch('customtkinter.CTkScrollableFrame', MagicMock()):
        yield

def test_file_panel_logic(mocker):
    master = MagicMock()
    on_file_selected = MagicMock()
    on_next = MagicMock()
    
    # Mocking FilePanel construction to avoid UI issues
    mocker.patch('customtkinter.CTkFont', MagicMock())
    
    panel = FilePanel(master, on_file_selected, on_next)
    
    # Simular seleção de arquivo
    mocker.patch('tkinter.filedialog.askopenfilename', return_value="test.xlsx")
    mocker.patch('pandas.ExcelFile', return_value=MagicMock(sheet_names=["Sheet1"]))
    
    panel._selecionar_arquivo()
    assert panel.file_path_var.get() == "test.xlsx"
    assert panel.btn_next.configure.called_with(state="normal")

def test_split_panel_params():
    master = MagicMock()
    panel = SplitPanel(master, MagicMock(), MagicMock())
    panel.mode_var.set("Linhas por arquivo")
    panel.entry_value.insert(0, "500")
    
    params = panel.get_params()
    assert params["mode"] == "rows"
    assert params["rows_per_file"] == 500

def test_output_panel_params():
    master = MagicMock()
    panel = OutputPanel(master, MagicMock(), MagicMock())
    panel.out_path_var.set("/tmp")
    panel.base_name_var.set("output")
    panel.format_var.set(".csv")
    
    params = panel.get_params()
    assert params["output_folder"] == "/tmp"
    assert params["base_name"] == "output"
    assert params["output_format"] == ".csv"

def test_progress_panel_reset():
    master = MagicMock()
    on_reset = MagicMock()
    panel = ProgressPanel(master, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), on_reset)
    
    panel.exibir_resumo(10, 5.0, 1024)
    assert panel.btn_reset.pack.called
    
    panel.limpar()
    assert panel.btn_reset.pack_forget.called
    
    # Testar clique no reset
    panel.on_reset()
    on_reset.assert_called_once()

def test_app_wizard_navigation(mocker):
    # Mocking components to avoid full initialization
    mocker.patch('ui.app.FilePanel', MagicMock())
    mocker.patch('ui.app.SplitPanel', MagicMock())
    mocker.patch('ui.app.OutputPanel', MagicMock())
    mocker.patch('ui.app.ProgressPanel', MagicMock())
    mocker.patch('ui.app.AboutPanel', MagicMock())
    mocker.patch('ui.app.PlanilhaSplitterApp._centralizar_janela', MagicMock())
    mocker.patch('ui.app.PlanilhaSplitterApp._construir_stepper', MagicMock())
    
    app = PlanilhaSplitterApp()
    app.passo_atual = 0
    
    app.proximo_passo()
    assert app.passo_atual == 1
    
    app.passo_anterior()
    assert app.passo_atual == 0
    
    app.proximo_passo()
    app.proximo_passo()
    app._reset_wizard()
    assert app.passo_atual == 0
