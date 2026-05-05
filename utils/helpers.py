import os
import math

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_file_info(file_path):
    if not os.path.exists(file_path):
        return None
    
    stats = os.stat(file_path)
    return {
        "name": os.path.basename(file_path),
        "size": format_size(stats.st_size),
        "extension": os.path.splitext(file_path)[1].lower()
    }
