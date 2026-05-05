import os

def validate_split_params(params):
    errors = []
    
    if not params.get("input_file"):
        errors.append("Arquivo de entrada não selecionado.")
    elif not os.path.exists(params["input_file"]):
        errors.append("Arquivo de entrada não encontrado.")
        
    if not params.get("output_folder"):
        errors.append("Pasta de saída não selecionada.")
        
    mode = params.get("mode")
    if mode == "rows":
        try:
            val = int(params.get("rows_per_file", 0))
            if val <= 0:
                errors.append("Número de linhas deve ser maior que zero.")
        except ValueError:
            errors.append("Número de linhas inválido.")
    elif mode == "files":
        try:
            val = int(params.get("num_files", 0))
            if val <= 0:
                errors.append("Número de arquivos deve ser maior que zero.")
        except ValueError:
            errors.append("Número de arquivos inválido.")
    elif mode == "column":
        if not params.get("split_column"):
            errors.append("Coluna de agrupamento não selecionada.")
    elif mode == "manual":
        val = params.get("manual_input", "").strip()
        if not val:
            errors.append("Intervalos manuais não definidos.")
        elif "-" not in val:
            errors.append("Formato de intervalo inválido (use ex: 1-5000).")
    elif mode == "size":
        try:
            val = float(params.get("max_size_mb", 0))
            if val <= 0:
                errors.append("Tamanho máximo deve ser maior que zero.")
        except ValueError:
            errors.append("Tamanho máximo inválido.")
            
    return errors


