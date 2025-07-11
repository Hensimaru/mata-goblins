import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos, compatível com PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
