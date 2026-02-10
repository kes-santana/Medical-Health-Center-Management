from datetime import datetime
import os
import json
from pathlib import Path

from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.employee_repository import EmployeeRepository
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Data_Access.users_repository import UsersRepository
from constants import EVENTS, RESOURCES, EMPLOYEES, USERS

def get_user_info():
    root, size = validate_json_size(USERS)
    
    if size == 0:
        return ["admin"]*3
    json_data = validate_content(root)
    users_repo = UsersRepository.from_dict(json_data)
    users_repo.users_list 
    

def clean_resource_list(all_rec: list[str], my_rec: list[str]) -> list[str]:
    s_all_rec = set(all_rec)
    if len(my_rec) == 0:
        return all_rec
    if type(my_rec[0]) == str:
        my_rec = set(my_rec)
    else:
        my_rec = set([item[0] for item in my_rec])
    return list(s_all_rec - my_rec)

def load_resources_names() -> list[str]:
    root, size_equal_zero = validate_json_size(RESOURCES)
    
    if size_equal_zero:
        return []
    
    json_data = validate_content(root)
    resource_repo = ResourceRepository.from_dict(json_data)
    resources_names = []
    for r in resource_repo.resource_list.values():
        if r.count > 0:
            key_split = r.key.split(" ")
            rec_id = key_split.pop(0)
            resources_names.append(f"{rec_id} - {r.key.replace(rec_id, "")}")
    
    return resources_names

def load_employees_names() -> list[str]:
    
    root, size_equal_zero = validate_json_size(EMPLOYEES)
    
    if size_equal_zero:
        return []
    
    json_data = validate_content(root)
    employee_repo = EmployeeRepository.from_dict(json_data)
    employees_names = []
    for e in employee_repo.employee_list.values():
        employees_names.append(e.key)
    return employees_names

def search_id_by_name(resources_names: list[str]) -> list[int]:
    resources_id = []
    for name in resources_names:
        resources_id.append(int(name.split(" ")[0]))
    return resources_id

def validate_json_size(name_repo: str):
    # Carpeta actual donde está app.py (Frontend)
    base_dir = os.path.dirname(__file__) 
    # Subir un nivel (Proyecto) y entrar a Backend/DataBase 
    db_path = os.path.abspath(os.path.join(base_dir, "..", "Backend", "DataBase"))
    # Construir la ruta al archivo JSON 
    root = os.path.join(db_path, f"{name_repo}.json")
    return str(root), os.path.getsize(root) == 0


def validate_content(root: str) -> dict:
    json_data = {}
    with open(root, "r", encoding="utf-8") as archivo:
        try:
            json_data = json.load(archivo)
            return json_data
        except json.JSONDecodeError:
            raise Exception("El contenido del JSON no es válido.")