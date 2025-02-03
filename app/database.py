import json
from pathlib import Path

DB_PATH = Path("app/data/products.json")


def load_data():
    """Carga los productos desde el archivo JSON y maneja errores si el formato es incorrecto."""
    if not DB_PATH.exists():
        DB_PATH.write_text("[]")  # Crea el archivo con una lista vacía si no existe

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):  # Asegurar que el JSON es una lista
                print("🚨 ERROR: El archivo JSON no contiene una lista válida.")
                return []
            return data
    except json.JSONDecodeError:
        print("🚨 ERROR: El archivo JSON está corrupto o vacío. Creando lista vacía.")
        return []
    except Exception as e:
        print(f"🚨 ERROR inesperado al cargar productos: {e}")
        return []


def save_data(products):
    """Guarda los productos en el archivo JSON."""
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)
