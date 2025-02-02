import json
from pathlib import Path

DB_PATH = Path("app/data/products.json")

def load_data():
    """Carga los productos desde el archivo JSON."""
    if not DB_PATH.exists():
        DB_PATH.write_text("[]")  # Si no existe, crea un archivo vacío
    with open(DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(products):
    """Guarda los productos en el archivo JSON."""
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)
