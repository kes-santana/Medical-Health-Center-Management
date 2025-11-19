import json
import os

from Backend.Data_Access.date_manager import DateManager
from constants import Events



# TODO: arreglar rutas y revisar metodos
# PATH = "..\DataBase"

class Context:
    def __init__(self):
        pass
    # todo cuando desde otro scrpt le pasan un parametro se pasa el valor verdad?
    @staticmethod
    def get_repo(name_repo: str) -> DateManager:
        root = os.path.join(
            r"C:\Users\Kevin Emilio\Programación\Python\Projects\Medical-Health-Center-Management\Backend\DataBase",
            f"{name_repo}.json"
        )

        # Verifica si el archivo está vacío
        if os.path.getsize(root) == 0:
            print("⚠️ El archivo JSON está vacío.")
            return DateManager([], 0)  # o lo que tenga sentido como valor por defecto

        with open(root, "r", encoding="utf-8") as archivo:
            try:
                json_data: list = json.load(archivo)
            except json.JSONDecodeError:
                print("⚠️ El contenido del JSON no es válido.")
                return DateManager([], 0)

        if name_repo == Events:
            data = json_data[0] if len(json_data) > 0 else []
            actual_id = json_data[1] if len(json_data) > 1 else 0
            return DateManager(data, actual_id)
        
    
    # @staticmethod
    # def save_repo(repo: str, data: list):
    #     with open(f"{PATH}{repo}.json", "w", encoding="utf-8") as f:
    #         json.dump(data, f, indent=4, ensure_ascii=False)
    